#!/usr/bin/env python3
"""
Invoice Automation System
Main application script for processing PDF invoices and extracting structured data.
"""

import os
import sys
import argparse
import glob
from pathlib import Path
from invoice_parser import InvoiceParser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_single_pdf(pdf_path: str, output_format: str = 'csv', output_filename: str = None) -> bool:
    """
    Process a single PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_format (str): Output format ('csv' or 'excel')
        output_filename (str): Custom output filename (CSV or Excel) for single PDF processing
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate file exists
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return False
        
        # Initialize parser
        parser = InvoiceParser()
        
        # Parse PDF
        logger.info(f"Processing PDF: {pdf_path}")
        data = parser.parse_pdf(pdf_path)
        
        if not data:
            logger.warning(f"No data extracted from {pdf_path}")
            return False
        
        # Generate output filename
        if output_filename:
            output_path = output_filename
        else:
            pdf_name = Path(pdf_path).stem
            if output_format.lower() == 'excel':
                output_path = f"{pdf_name}_extracted.xlsx"
            else:
                output_path = f"{pdf_name}_extracted.csv"
        
        success = False
        if output_format.lower() == 'excel':
            success = parser.save_to_excel(data, output_path)
        else:
            success = parser.save_to_csv(data, output_path)
        
        if success:
            logger.info(f"Successfully processed {pdf_path}")
            logger.info(f"Extracted {len(data)} records")
            logger.info(f"Output saved to: {output_path}")
            return True
        else:
            logger.error(f"Failed to save output for {pdf_path}")
            return False
            
    except Exception as e:
        logger.error(f"Error processing {pdf_path}: {str(e)}")
        return False

def process_directory(input_dir: str, output_format: str = 'csv') -> dict:
    """
    Process all PDF files in a directory.
    
    Args:
        input_dir (str): Directory containing PDF files
        output_format (str): Output format ('csv' or 'excel')
        
    Returns:
        dict: Summary of processing results
    """
    results = {
        'total_files': 0,
        'successful': 0,
        'failed': 0,
        'failed_files': []
    }
    
    try:
        # Find all PDF files in directory
        pdf_pattern = os.path.join(input_dir, "*.pdf")
        pdf_files = glob.glob(pdf_pattern)
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {input_dir}")
            return results
        
        results['total_files'] = len(pdf_files)
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Process each PDF file
        for pdf_file in pdf_files:
            success = process_single_pdf(pdf_file, output_format)
            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1
                results['failed_files'].append(pdf_file)
        
        # Print summary
        logger.info(f"\nProcessing Summary:")
        logger.info(f"Total files: {results['total_files']}")
        logger.info(f"Successful: {results['successful']}")
        logger.info(f"Failed: {results['failed']}")
        
        if results['failed_files']:
            logger.info(f"Failed files:")
            for failed_file in results['failed_files']:
                logger.info(f"  - {failed_file}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error processing directory {input_dir}: {str(e)}")
        return results

def main():
    """Main function to handle command line arguments and execute processing."""
    parser = argparse.ArgumentParser(
        description="Invoice Automation System - Extract structured data from PDF invoices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single PDF file
  python main.py invoice.pdf
  
  # Process a single PDF and save as Excel
  python main.py invoice.pdf --format excel
  
  # Process all PDFs in a directory
  python main.py --directory ./invoices/
  
  # Process all PDFs in a directory and save as Excel
  python main.py --directory ./invoices/ --format excel
        """
    )
    
    parser.add_argument(
        'pdf_file',
        nargs='?',
        help='Path to a single PDF file to process'
    )
    
    parser.add_argument(
        '--directory', '-d',
        help='Directory containing PDF files to process'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['csv', 'excel'],
        default='csv',
        help='Output format (default: csv)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Custom output filename (CSV or Excel) for single PDF processing'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate arguments
    if not args.pdf_file and not args.directory:
        logger.error("Please provide either a PDF file or a directory to process")
        parser.print_help()
        sys.exit(1)
    
    if args.pdf_file and args.directory:
        logger.error("Please provide either a PDF file OR a directory, not both")
        parser.print_help()
        sys.exit(1)
    
    # Process based on input type
    if args.pdf_file:
        # Process single file
        output_filename = args.output if args.output else None
        success = process_single_pdf(args.pdf_file, args.format, output_filename)
        sys.exit(0 if success else 1)
    else:
        # Process directory
        results = process_directory(args.directory, args.format)
        sys.exit(0 if results['failed'] == 0 else 1)

if __name__ == "__main__":
    main() 