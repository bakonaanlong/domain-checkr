#GoDaddy Domain Availability Checker

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import List, Dict

import requests
from dotenv import load_dotenv
from os import getenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
GODADDY_API_URL = "https://api.ote-godaddy.com/v1/domains/available"
BATCH_SIZE = 80
DELAY_SECONDS = 5
DEFAULT_TLD = ".com"
OUTPUT_FILE = "available.json"


class DomainChecker:
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {
            "Authorization": f"sso-key {api_key}:{api_secret}",
            "Content-Type": "application/json"
        }
    
    def check_batch(self, domains: List[str]) -> List[Dict]:
        try:
            response = requests.post(
                GODADDY_API_URL,
                headers=self.headers,
                json=domains,
                params={"checkType": "FAST"},
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("domains", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []


def generate_combinations(length: int) -> List[str]:
    if length < 1:
        raise ValueError("Length must be at least 1")
    
    letters = "abcdefghijklmnopqrstuvwxyz"
    results = []
    
    def recurse(prefix: str, depth: int) -> None:
        if depth == length:
            results.append(prefix)
            return
        for char in letters:
            recurse(prefix + char, depth + 1)
    
    recurse("", 0)
    return results


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check domain availability using GoDaddy API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python domain_checker.py 3 --tlds .com,.io,.net"
    )
    parser.add_argument(
        "length",
        type=int,
        help="Number of letters in domain combinations (e.g., 3 for 'abc')"
    )
    parser.add_argument(
        "tlds",
        nargs="?",
        default=DEFAULT_TLD,
        help=f"Comma-separated TLDs (default: {DEFAULT_TLD})"
    )
    
    args = parser.parse_args()
    
    if args.length < 1:
        parser.error("Length must be at least 1")
    
    return args


def load_credentials() -> tuple[str, str]:
    load_dotenv()
    
    api_key = getenv("GODADDY_API_KEY")
    api_secret = getenv("GODADDY_API_SECRET")
    
    if not api_key or not api_secret:
        logger.error("Missing GoDaddy API credentials in .env file")
        sys.exit(1)
    
    return api_key, api_secret


def save_results(results: Dict[str, List[str]], output_path: Path) -> None:
    try:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {output_path}")
    except IOError as e:
        logger.error(f"Failed to save results: {e}")


def main() -> None:
    args = parse_arguments()
    api_key, api_secret = load_credentials()
    
    # Parse TLDs
    tlds = [tld.strip() for tld in args.tlds.split(",") if tld.strip()]
    
    # Generate combinations
    logger.info(f"Generating {args.length}-letter combinations for TLDs: {', '.join(tlds)}")
    try:
        combinations = generate_combinations(args.length)
    except ValueError as e:
        logger.error(f"Invalid length: {e}")
        sys.exit(1)
    
    logger.info(f"Generated {len(combinations):,} combinations")
    
    # Initialize checker
    checker = DomainChecker(api_key, api_secret)
    
    # Check domains for each TLD
    available_domains = {tld: [] for tld in tlds}
    
    for tld in tlds:
        logger.info(f"Checking {tld} domains...")
        
        for i in range(0, len(combinations), BATCH_SIZE):
            batch = [f"{combo}{tld}" for combo in combinations[i:i + BATCH_SIZE]]
            results = checker.check_batch(batch)
            
            for result in results:
                domain = result.get("domain")
                if result.get("available"):
                    available_domains[tld].append(domain)
                    logger.info(f"✓ Available: {domain}")
                else:
                    logger.debug(f"✗ Taken: {domain}")
            
            processed = min(i + BATCH_SIZE, len(combinations))
            logger.info(f"Progress: {processed}/{len(combinations)} for {tld}")
            
            # Rate limiting
            if i + BATCH_SIZE < len(combinations):
                time.sleep(DELAY_SECONDS)
    
    # Save results
    save_results(available_domains, Path(OUTPUT_FILE))
    
    # Summary
    total_available = sum(len(domains) for domains in available_domains.values())
    logger.info(f"Complete! Found {total_available} available domains")


if __name__ == "__main__":
    main()