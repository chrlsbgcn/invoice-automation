# Invoice Automation System

A comprehensive Python application for automating the extraction of structured data from PDF invoices. This system can handle multi-page PDFs and extract specific fields including billing information, invoice periods, company details, and plan line items.

## Features

- **Multi-page PDF Support**: Handles invoices spanning multiple pages
- **Robust Field Extraction**: Extracts all required fields with fallback parsing methods
- **Multiple Output Formats**: Supports CSV and Excel output
- **Batch Processing**: Process entire directories of PDF files
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Error Handling**: Graceful error handling with detailed error messages

## Extracted Fields

The system extracts the following fields from PDF invoices:

- **Billed To**: The first line after the label "Billed to:"
- **Invoice Period**: Date range (e.g., May 1 – May 31, 2025)
- **Invoice Issue Date**: Date when the invoice was issued
- **Company Name**: Name of the company being billed
- **Plan**: Service/product plan description
- **Qty**: Quantity per plan line
- **Unit Price**: Price per unit per plan line
- **Amount**: Total amount per plan line

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python main.py --help
   ```

## Usage

### Command Line Interface

The application provides a flexible command-line interface for processing PDF invoices.

#### Process a Single PDF File

```bash
# Process a single PDF and save as CSV (default)
python main.py invoice.pdf

# Process a single PDF and save as Excel
python main.py invoice.pdf --format excel
```

#### Process Multiple PDF Files

```bash
# Process all PDFs in a directory
python main.py --directory ./invoices/

# Process all PDFs in a directory and save as Excel
python main.py --directory ./invoices/ --format excel
```

#### Verbose Logging

```bash
# Enable detailed logging for debugging
python main.py invoice.pdf --verbose
```

### Programmatic Usage

You can also use the `InvoiceParser` class directly in your Python code:

```python
from invoice_parser import InvoiceParser

# Initialize parser
parser = InvoiceParser()

# Parse a PDF file
data = parser.parse_pdf("invoice.pdf")

# Save to CSV
parser.save_to_csv(data, "output.csv")

# Save to Excel
parser.save_to_excel(data, "output.xlsx")
```

## Output Format

The system generates structured output with one row per plan line. Each row contains:

| Column | Description | Example |
|--------|-------------|---------|
| Billed To | Customer name | John Doe |
| Invoice Period | Billing period | May 1 – May 31, 2025 |
| Invoice Issue Date | Invoice date | June 1, 2025 |
| Company Name | Company being billed | ACME Corp |
| Plan | Service description | Standard Plan, 100 users, Tier 2 |
| Qty | Quantity | 100 |
| Unit Price | Price per unit | $5.00 |
| Amount | Total amount | $500.00 |

## Supported PDF Formats

The system uses multiple PDF parsing libraries to handle various PDF formats:

- **pdfplumber**: Primary parser for better text extraction
- **PyMuPDF**: Fallback parser for complex PDFs

This dual approach ensures maximum compatibility with different PDF structures and layouts.

## Field Extraction Patterns

The system uses sophisticated regex patterns to extract fields:

### Billed To
- `Billed to: [customer name]`
- `Bill to: [customer name]`
- `Customer: [customer name]`
- `Client: [customer name]`

### Invoice Period
- `Invoice Period: [date range]`
- `Period: [date range]`
- `Billing Period: [date range]`
- Date range patterns: `May 1 – May 31, 2025`

### Invoice Issue Date
- `Invoice Date: [date]`
- `Issue Date: [date]`
- `Date: [date]`
- Various date formats: `June 1, 2025`, `06/01/2025`, `06-01-2025`

### Company Name
- `Company: [name]`
- `Business: [name]`
- `Organization: [name]`
- Common suffixes: Corp, Inc, LLC, Ltd, Company, Co.

### Plan Lines
The system identifies plan lines by looking for:
- Quantity patterns: `100 users`, `50 units`
- Price patterns: `$5.00`, `$1,250.00`
- Service keywords: `plan`, `service`, `product`, `subscription`

## Error Handling

The system includes comprehensive error handling:

- **File Validation**: Checks if PDF files exist and are readable
- **Parsing Fallbacks**: Uses multiple parsing methods if one fails
- **Field Extraction**: Gracefully handles missing or malformed fields
- **Output Validation**: Ensures data is properly formatted before saving

## Logging

The application provides detailed logging at different levels:

- **INFO**: General processing information
- **WARNING**: Non-critical issues (missing fields, etc.)
- **ERROR**: Critical errors that prevent processing
- **DEBUG**: Detailed debugging information (with `--verbose` flag)

## Troubleshooting

### Common Issues

1. **No data extracted**: 
   - Check if the PDF contains text (not just images)
   - Verify the PDF structure matches expected patterns
   - Try with `--verbose` flag for detailed debugging

2. **Missing fields**:
   - The system uses multiple patterns to find fields
   - Some fields might not be present in all invoices
   - Check the extracted data to see what was found

3. **Installation issues**:
   - Ensure Python 3.7+ is installed
   - Try upgrading pip: `pip install --upgrade pip`
   - Install dependencies individually if needed

### Getting Help

If you encounter issues:

1. Run with verbose logging: `python main.py invoice.pdf --verbose`
2. Check the log output for specific error messages
3. Verify your PDF file is not corrupted or password-protected
4. Ensure the PDF contains extractable text

## Performance

- **Single PDF**: Typically processes in 1-5 seconds
- **Batch Processing**: Processes multiple files sequentially
- **Memory Usage**: Minimal memory footprint, processes one file at a time
- **Output Size**: CSV files are typically small, Excel files may be larger

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions:
- Check the troubleshooting section above
- Review the logging output for specific error messages
- Ensure your PDF format is supported 