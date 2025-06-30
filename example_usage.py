#!/usr/bin/env python3
"""
Example usage of the Invoice Automation System
Demonstrates how to use the InvoiceParser class programmatically.
"""

from invoice_parser import InvoiceParser
import pandas as pd
import tempfile
import os

def example_single_pdf_processing():
    """Example of processing a single PDF file."""
    print("=== Single PDF Processing Example ===")
    
    # Initialize the parser
    parser = InvoiceParser()
    
    # Example: Process a PDF file (replace with actual path)
    pdf_path = "sample_invoice.pdf"  # Replace with your PDF file path
    
    if os.path.exists(pdf_path):
        # Parse the PDF
        print(f"Processing PDF: {pdf_path}")
        data = parser.parse_pdf(pdf_path)
        
        if data:
            print(f"Successfully extracted {len(data)} records")
            
            # Display the extracted data
            df = pd.DataFrame(data)
            print("\nExtracted Data:")
            print(df.to_string(index=False))
            
            # Save to CSV
            csv_path = "extracted_data.csv"
            if parser.save_to_csv(data, csv_path):
                print(f"\nData saved to CSV: {csv_path}")
            
            # Save to Excel
            excel_path = "extracted_data.xlsx"
            if parser.save_to_excel(data, excel_path):
                print(f"Data saved to Excel: {excel_path}")
        else:
            print("No data extracted from the PDF")
    else:
        print(f"PDF file not found: {pdf_path}")
        print("Please provide a valid PDF file path")

def example_batch_processing():
    """Example of batch processing multiple PDF files."""
    print("\n=== Batch Processing Example ===")
    
    # Initialize the parser
    parser = InvoiceParser()
    
    # Example: Process all PDFs in a directory
    input_directory = "./invoices/"  # Replace with your directory path
    
    if os.path.exists(input_directory):
        import glob
        
        # Find all PDF files
        pdf_files = glob.glob(os.path.join(input_directory, "*.pdf"))
        
        if pdf_files:
            print(f"Found {len(pdf_files)} PDF files to process")
            
            all_data = []
            
            # Process each PDF file
            for pdf_file in pdf_files:
                print(f"\nProcessing: {pdf_file}")
                data = parser.parse_pdf(pdf_file)
                
                if data:
                    all_data.extend(data)
                    print(f"  Extracted {len(data)} records")
                else:
                    print(f"  No data extracted")
            
            if all_data:
                # Save combined data
                combined_csv = "combined_extracted_data.csv"
                if parser.save_to_csv(all_data, combined_csv):
                    print(f"\nCombined data saved to: {combined_csv}")
                
                # Display summary
                df = pd.DataFrame(all_data)
                print(f"\nTotal records extracted: {len(all_data)}")
                print(f"Unique companies: {df['Company Name'].nunique()}")
                print(f"Date range: {df['Invoice Issue Date'].min()} to {df['Invoice Issue Date'].max()}")
        else:
            print(f"No PDF files found in {input_directory}")
    else:
        print(f"Directory not found: {input_directory}")

def example_data_analysis():
    """Example of analyzing extracted data."""
    print("\n=== Data Analysis Example ===")
    
    # Sample extracted data for demonstration
    sample_data = [
        {
            'Billed To': 'John Doe',
            'Invoice Period': 'May 1 – May 31, 2025',
            'Invoice Issue Date': 'June 1, 2025',
            'Company Name': 'ACME Corp',
            'Plan': 'Standard Plan, 100 users, Tier 2',
            'Qty': '100',
            'Unit Price': '$5.00',
            'Amount': '$500.00'
        },
        {
            'Billed To': 'John Doe',
            'Invoice Period': 'May 1 – May 31, 2025',
            'Invoice Issue Date': 'June 1, 2025',
            'Company Name': 'ACME Corp',
            'Plan': 'Premium Plan, 50 users, Tier 1',
            'Qty': '50',
            'Unit Price': '$8.00',
            'Amount': '$400.00'
        },
        {
            'Billed To': 'Jane Smith',
            'Invoice Period': 'April 1 – April 30, 2025',
            'Invoice Issue Date': 'May 1, 2025',
            'Company Name': 'Tech Solutions Inc.',
            'Plan': 'Cloud Storage Plan',
            'Qty': '200',
            'Unit Price': '$2.50',
            'Amount': '$500.00'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Basic analysis
    print("Data Summary:")
    print(f"Total records: {len(df)}")
    print(f"Unique customers: {df['Billed To'].nunique()}")
    print(f"Unique companies: {df['Company Name'].nunique()}")
    
    # Convert amount to numeric for calculations
    df['Amount_Numeric'] = df['Amount'].str.replace('$', '').str.replace(',', '').astype(float)
    df['Qty_Numeric'] = df['Qty'].astype(int)
    
    print(f"\nFinancial Summary:")
    print(f"Total revenue: ${df['Amount_Numeric'].sum():,.2f}")
    print(f"Average amount per line: ${df['Amount_Numeric'].mean():.2f}")
    print(f"Total quantity: {df['Qty_Numeric'].sum():,}")
    
    # Group by company
    print(f"\nRevenue by Company:")
    company_revenue = df.groupby('Company Name')['Amount_Numeric'].sum()
    for company, revenue in company_revenue.items():
        print(f"  {company}: ${revenue:,.2f}")
    
    # Save analysis results
    analysis_csv = "analysis_results.csv"
    df.to_csv(analysis_csv, index=False)
    print(f"\nAnalysis results saved to: {analysis_csv}")

def example_custom_processing():
    """Example of custom processing and filtering."""
    print("\n=== Custom Processing Example ===")
    
    # Initialize parser
    parser = InvoiceParser()
    
    # Example: Process PDF and apply custom filters
    pdf_path = "sample_invoice.pdf"  # Replace with actual path
    
    if os.path.exists(pdf_path):
        data = parser.parse_pdf(pdf_path)
        
        if data:
            df = pd.DataFrame(data)
            
            # Custom filtering example
            print("Original data shape:", df.shape)
            
            # Filter by date range
            # Convert date strings to datetime for filtering
            df['Invoice Issue Date'] = pd.to_datetime(df['Invoice Issue Date'], errors='coerce')
            
            # Filter for recent invoices (example: last 30 days)
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=30)
            recent_invoices = df[df['Invoice Issue Date'] >= cutoff_date]
            
            print(f"Recent invoices (last 30 days): {len(recent_invoices)}")
            
            # Filter by amount threshold
            df['Amount_Numeric'] = df['Amount'].str.replace('$', '').str.replace(',', '').astype(float)
            high_value_invoices = df[df['Amount_Numeric'] > 1000]
            
            print(f"High value invoices (>$1000): {len(high_value_invoices)}")
            
            # Save filtered results
            if len(recent_invoices) > 0:
                parser.save_to_csv(recent_invoices.to_dict('records'), "recent_invoices.csv")
                print("Recent invoices saved to: recent_invoices.csv")
            
            if len(high_value_invoices) > 0:
                parser.save_to_csv(high_value_invoices.to_dict('records'), "high_value_invoices.csv")
                print("High value invoices saved to: high_value_invoices.csv")
        else:
            print("No data extracted for custom processing")
    else:
        print(f"PDF file not found: {pdf_path}")

def example_error_handling():
    """Example of error handling and validation."""
    print("\n=== Error Handling Example ===")
    
    parser = InvoiceParser()
    
    # Test with non-existent file
    print("Testing with non-existent file...")
    data = parser.parse_pdf("non_existent_file.pdf")
    print(f"Result: {len(data) if data else 0} records extracted")
    
    # Test with empty data
    print("\nTesting with empty data...")
    empty_data = []
    success = parser.save_to_csv(empty_data, "empty_test.csv")
    print(f"Save empty data result: {success}")
    
    # Test with malformed data
    print("\nTesting with malformed data...")
    malformed_data = [{'Billed To': 'Test'}]  # Missing required fields
    success = parser.save_to_csv(malformed_data, "malformed_test.csv")
    print(f"Save malformed data result: {success}")

def main():
    """Main function to run all examples."""
    print("Invoice Automation System - Example Usage")
    print("=" * 50)
    
    # Run examples
    example_single_pdf_processing()
    example_batch_processing()
    example_data_analysis()
    example_custom_processing()
    example_error_handling()
    
    print("\n" + "=" * 50)
    print("Example usage completed!")
    print("\nTo use with your own PDFs:")
    print("1. Replace file paths in the examples with your actual PDF files")
    print("2. Run: python example_usage.py")
    print("3. Check the generated output files")

if __name__ == "__main__":
    main() 