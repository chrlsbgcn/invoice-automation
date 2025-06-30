#!/usr/bin/env python3
"""
Test suite for the Invoice Automation System
Tests the InvoiceParser class functionality and field extraction.
"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from invoice_parser import InvoiceParser

class TestInvoiceParser(unittest.TestCase):
    """Test cases for the InvoiceParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = InvoiceParser()
        
        # Sample invoice text for testing
        self.sample_invoice_text = """
        INVOICE
        
        Billed to: John Doe
        123 Main Street
        Anytown, USA
        
        Company: ACME Corporation
        Invoice Period: May 1 – May 31, 2025
        Invoice Date: June 1, 2025
        
        DESCRIPTION                    QTY    UNIT PRICE    AMOUNT
        Standard Plan, 100 users      100    $5.00         $500.00
        Premium Plan, 50 users        50     $8.00         $400.00
        Basic Plan, 25 users          25     $3.00         $75.00
        
        TOTAL: $975.00
        """
        
        self.sample_invoice_text_alt = """
        INVOICE
        
        Customer: Jane Smith
        Business: Tech Solutions Inc.
        Period: April 1 - April 30, 2025
        Issue Date: May 1, 2025
        
        ITEM DESCRIPTION              QUANTITY   PRICE    TOTAL
        Cloud Storage Plan           200         $2.50    $500.00
        API Access Package           100         $1.00    $100.00
        Support Package              1           $50.00   $50.00
        """
    
    def test_extract_billed_to(self):
        """Test extraction of billed to information."""
        # Test standard pattern
        result = self.parser._extract_billed_to(self.sample_invoice_text)
        self.assertEqual(result, "John Doe")
        
        # Test alternative pattern
        result = self.parser._extract_billed_to(self.sample_invoice_text_alt)
        self.assertEqual(result, "Jane Smith")
        
        # Test with no match
        result = self.parser._extract_billed_to("No billed to information here")
        self.assertEqual(result, "")
    
    def test_extract_invoice_period(self):
        """Test extraction of invoice period."""
        # Test standard pattern
        result = self.parser._extract_invoice_period(self.sample_invoice_text)
        self.assertEqual(result, "May 1 – May 31, 2025")
        
        # Test alternative pattern
        result = self.parser._extract_invoice_period(self.sample_invoice_text_alt)
        self.assertEqual(result, "April 1 - April 30, 2025")
        
        # Test with no match
        result = self.parser._extract_invoice_period("No period information here")
        self.assertEqual(result, "")
    
    def test_extract_invoice_issue_date(self):
        """Test extraction of invoice issue date."""
        # Test standard pattern
        result = self.parser._extract_invoice_issue_date(self.sample_invoice_text)
        self.assertEqual(result, "June 1, 2025")
        
        # Test alternative pattern
        result = self.parser._extract_invoice_issue_date(self.sample_invoice_text_alt)
        self.assertEqual(result, "May 1, 2025")
        
        # Test with no match
        result = self.parser._extract_invoice_issue_date("No date information here")
        self.assertEqual(result, "")
    
    def test_extract_company_name(self):
        """Test extraction of company name."""
        # Test standard pattern
        result = self.parser._extract_company_name(self.sample_invoice_text)
        self.assertEqual(result, "ACME Corporation")
        
        # Test alternative pattern
        result = self.parser._extract_company_name(self.sample_invoice_text_alt)
        self.assertEqual(result, "Tech Solutions Inc.")
        
        # Test with no match
        result = self.parser._extract_company_name("No company information here")
        self.assertEqual(result, "")
    
    def test_extract_plan_lines(self):
        """Test extraction of plan lines."""
        # Test standard format
        result = self.parser._extract_plan_lines(self.sample_invoice_text)
        self.assertEqual(len(result), 3)
        
        # Check first plan line
        first_line = result[0]
        self.assertEqual(first_line['plan'], "Standard Plan, 100 users")
        self.assertEqual(first_line['qty'], "100")
        self.assertEqual(first_line['unit_price'], "$5.00")
        self.assertEqual(first_line['amount'], "$500.00")
        
        # Test alternative format
        result = self.parser._extract_plan_lines(self.sample_invoice_text_alt)
        self.assertEqual(len(result), 3)
        
        # Check first plan line from alternative format
        first_line = result[0]
        self.assertEqual(first_line['plan'], "Cloud Storage Plan")
        self.assertEqual(first_line['qty'], "200")
        self.assertEqual(first_line['unit_price'], "$2.50")
        self.assertEqual(first_line['amount'], "$500.00")
    
    def test_extract_fields_from_text(self):
        """Test complete field extraction from text."""
        result = self.parser._extract_fields_from_text(self.sample_invoice_text)
        
        self.assertEqual(len(result), 3)  # 3 plan lines
        
        # Check first result has all required fields
        first_result = result[0]
        expected_fields = [
            'Billed To', 'Invoice Period', 'Invoice Issue Date', 
            'Company Name', 'Plan', 'Qty', 'Unit Price', 'Amount'
        ]
        
        for field in expected_fields:
            self.assertIn(field, first_result)
        
        # Check specific values
        self.assertEqual(first_result['Billed To'], "John Doe")
        self.assertEqual(first_result['Invoice Period'], "May 1 – May 31, 2025")
        self.assertEqual(first_result['Invoice Issue Date'], "June 1, 2025")
        self.assertEqual(first_result['Company Name'], "ACME Corporation")
        self.assertEqual(first_result['Plan'], "Standard Plan, 100 users")
        self.assertEqual(first_result['Qty'], "100")
        self.assertEqual(first_result['Unit Price'], "$5.00")
        self.assertEqual(first_result['Amount'], "$500.00")
    
    def test_save_to_csv(self):
        """Test saving data to CSV file."""
        test_data = [
            {
                'Billed To': 'John Doe',
                'Invoice Period': 'May 1 – May 31, 2025',
                'Invoice Issue Date': 'June 1, 2025',
                'Company Name': 'ACME Corp',
                'Plan': 'Standard Plan',
                'Qty': '100',
                'Unit Price': '$5.00',
                'Amount': '$500.00'
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            result = self.parser.save_to_csv(test_data, temp_path)
            self.assertTrue(result)
            
            # Verify file was created and has content
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, 'r') as f:
                content = f.read()
                self.assertIn('John Doe', content)
                self.assertIn('Standard Plan', content)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_save_to_excel(self):
        """Test saving data to Excel file."""
        test_data = [
            {
                'Billed To': 'John Doe',
                'Invoice Period': 'May 1 – May 31, 2025',
                'Invoice Issue Date': 'June 1, 2025',
                'Company Name': 'ACME Corp',
                'Plan': 'Standard Plan',
                'Qty': '100',
                'Unit Price': '$5.00',
                'Amount': '$500.00'
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            result = self.parser.save_to_excel(test_data, temp_path)
            self.assertTrue(result)
            
            # Verify file was created
            self.assertTrue(os.path.exists(temp_path))
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    @patch('invoice_parser.pdfplumber.open')
    def test_parse_with_pdfplumber(self, mock_pdfplumber):
        """Test PDF parsing with pdfplumber."""
        # Mock pdfplumber response
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = self.sample_invoice_text
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
        
        result = self.parser._parse_with_pdfplumber("test.pdf")
        
        self.assertEqual(len(result), 3)  # Should extract 3 plan lines
        self.assertEqual(result[0]['Billed To'], "John Doe")
    
    @patch('invoice_parser.fitz.open')
    def test_parse_with_pymupdf(self, mock_fitz):
        """Test PDF parsing with PyMuPDF."""
        # Mock PyMuPDF response
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = self.sample_invoice_text
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz.return_value = mock_doc
        
        result = self.parser._parse_with_pymupdf("test.pdf")
        
        self.assertEqual(len(result), 3)  # Should extract 3 plan lines
        self.assertEqual(result[0]['Billed To'], "John Doe")
        
        # Verify document was closed
        mock_doc.close.assert_called_once()
    
    def test_extract_quantity_from_context(self):
        """Test quantity extraction from context."""
        lines = [
            "Some text",
            "100 users",
            "Plan description",
            "Another line"
        ]
        
        result = self.parser._extract_quantity_from_context(lines, 2)  # Around "Plan description"
        self.assertEqual(result, "100")
    
    def test_extract_price_from_context(self):
        """Test price extraction from context."""
        lines = [
            "Some text",
            "$5.00 per unit",
            "Plan description",
            "Another line"
        ]
        
        result = self.parser._extract_price_from_context(lines, 2)  # Around "Plan description"
        self.assertEqual(result, "$5.00")
    
    def test_extract_amount_from_context(self):
        """Test amount extraction from context."""
        lines = [
            "Some text",
            "Plan description",
            "Total: $500.00",
            "Another line"
        ]
        
        result = self.parser._extract_amount_from_context(lines, 1)  # Around "Plan description"
        self.assertEqual(result, "$500.00")
    
    def test_empty_text_handling(self):
        """Test handling of empty or invalid text."""
        result = self.parser._extract_fields_from_text("")
        self.assertEqual(result, [])
        
        result = self.parser._extract_fields_from_text("   \n\n   ")
        self.assertEqual(result, [])
    
    def test_malformed_data_handling(self):
        """Test handling of malformed or incomplete data."""
        malformed_text = """
        INVOICE
        
        Billed to: John Doe
        Company: ACME Corp
        
        No plan lines or pricing information
        """
        
        result = self.parser._extract_fields_from_text(malformed_text)
        self.assertEqual(len(result), 0)  # Should handle gracefully
    
    def test_case_insensitive_extraction(self):
        """Test that extraction is case insensitive."""
        text = """
        INVOICE
        
        BILLED TO: John Doe
        COMPANY: ACME Corp
        INVOICE PERIOD: May 1 – May 31, 2025
        INVOICE DATE: June 1, 2025
        """
        
        result = self.parser._extract_fields_from_text(text)
        # Should still extract fields even with uppercase labels
        self.assertIsInstance(result, list)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2) 