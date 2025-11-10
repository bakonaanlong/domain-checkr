# GoDaddy Domain Availability Checking script

A Python script that checks the availability of domain names using the GoDaddy API. It generates all possible letter combinations of a specified length and checks their availability across multiple TLDs (Top-Level Domains) eg. .com, .io, .org.

## Features

-  Generate all possible letter combinations (a-z) of any length
-  Check multiple TLDs simultaneously (.com, .io, .org, etc.)
-  Batch processing to optimize API calls
-  Export results to JSON format
-  Rate limiting to respect API constraints

## Prerequisites

- Python 3.7 or higher
- GoDaddy API credentials (API Key and Secret) 
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/godaddy-domain-checkr.git
   cd godaddy-domain-checkr
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**
   
   Create a `.env` file in the project root directory:
   ```bash
   touch .env
   ```

4. **Add your GoDaddy API credentials**
   
   Open the `.env` file and add your credentials:
   ```
   GODADDY_API_KEY=your_api_key_here
   GODADDY_API_SECRET=your_api_secret_here
   ```

## Getting GoDaddy API Credentials

1. Go to [GoDaddy Developer Portal](https://developer.godaddy.com/)
2. Sign in with your GoDaddy account
3. Navigate to "API Keys" section
4. Click "Create New API Key"
5. Choose **OTE (Test Environment)** for testing or **Production** for live checks
6. Copy your API Key and Secret to your `.env` file

> ⚠️ **Note**: This script uses the OTE (test) endpoint by default. For production use, change the API URL in the code to https://api.godaddy.com/v1/domains/available.

## Usage

### Basic Usage

Check 3-letter domains with .com TLD:
```bash
python lookup.py 3
```

### Specify TLDs

Check 3-letter domains with multiple TLDs:
```bash
python lookup.py 3 .com,.io,.dev
```

Check 4-letter domains:
```bash
python lookup.py 4 .com
```

### Command Line Arguments

```bash
python lookup.py <number_of_letters> [tlds]
```

- `<number_of_letters>`: Required. Length of domain names to generate (e.g., 3 for "abc")
- `[tlds]`: Optional. Comma-separated list of TLDs to check (default: `.com`)

## Output

The script generates an `available.json` file with the following structure:

```json
{
  ".com": [
    "xyz.com",
    "abc.com"
  ],
  ".io": [
    "def.io",
    "ghi.io"
  ]
}
```

### Console Output

During execution, you'll see real-time status updates:

```
 Config: 3-letter combos | TLDs: .com, .io
 17,576 possible combinations

 Checking .com domains...
 Progress: 2240/17576 for .com
```

## Configuration

You can modify these constants in the script:

- `BATCH_SIZE`: Number of domains to check per API call (default: 80)
- `DELAY_SECONDS`: Delay between batches in seconds (default: 5)

## Performance Considerations

- **3-letter combinations**: 17,576 domains (a-z³)
- **4-letter combinations**: 456,976 domains (a-z⁴)
- **5-letter combinations**: 11,881,376 domains (a-z⁵)


## Troubleshooting

### Missing API Credentials
```
 Missing GoDaddy API credentials in .env file
```
**Solution**: Ensure your `.env` file exists and contains valid credentials.

### API Rate Limiting
```
 API Error: Rate limit exceeded
```
**Solution**: Increase the `DELAY_SECONDS` value in the script or reduce `BATCH_SIZE`.

### Invalid Number of Letters
```
 Invalid number of letters. Example: python lookup.py -3 .com,.io
```
**Solution**: Provide a valid positive integer as the first argument.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This script is provided as-is for educational and legitimate business purposes. Always comply with GoDaddy's Terms of Service and API usage policies. The author is not responsible for any misuse of this tool.

