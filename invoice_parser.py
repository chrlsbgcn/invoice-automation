import re
import pandas as pd
import pdfplumber
import fitz  # PyMuPDF
from datetime import datetime
from dateutil import parser as date_parser
from typing import List, Dict, Optional, Tuple
import logging
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InvoiceParser:
    """
    A comprehensive invoice parser that extracts structured data from PDF invoices.
    Handles multi-page PDFs and extracts specific fields as requested.
    Now includes OCR support for scanned/image-based PDFs.
    """
    
    def __init__(self, tesseract_path: str = None):
        self.extracted_data = []
        
        # Configure Tesseract path if provided
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            # Try common Windows installation paths
            common_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Users\charl\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
            ]
            for path in common_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    logger.info(f"Found Tesseract at: {path}")
                    break
        
    def parse_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Parse a PDF invoice and extract structured data from all pages.
        Now includes OCR fallback for scanned/image-based PDFs.
        """
        try:
            logger.info(f"Starting to parse PDF: {pdf_path}")
            # Try pdfplumber first for better text extraction
            data = self._parse_with_pdfplumber(pdf_path)
            if data:
                return self._post_process_data(data)
            # Fallback to PyMuPDF if pdfplumber fails
            logger.info("Falling back to PyMuPDF")
            data = self._parse_with_pymupdf(pdf_path)
            if data:
                return self._post_process_data(data)
            # Final fallback: OCR for scanned/image-based PDFs
            logger.info("No text found, attempting OCR extraction")
            data = self._parse_with_ocr(pdf_path)
            if data:
                return self._post_process_data(data)
            return []
        except Exception as e:
            logger.error(f"Error parsing PDF {pdf_path}: {str(e)}")
            return []
    
    def _parse_with_ocr(self, pdf_path: str) -> List[Dict]:
        """
        Parse PDF using OCR for scanned/image-based PDFs, page by page.
        """
        try:
            doc = fitz.open(pdf_path)
            all_data = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                logger.info(f"Processing page {page_num + 1} with OCR")
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                img_cv = self._preprocess_image_for_ocr(img_cv)
                try:
                    page_text = pytesseract.image_to_string(img_cv, config='--psm 6')
                    if page_text.strip():
                        print(f"\n=== PAGE {page_num + 1} OCR TEXT ===")
                        print(page_text)
                        print("=" * 50)
                        page_data = self._extract_fields_from_text(page_text)
                        if page_data:
                            all_data.extend(page_data)
                    else:
                        logger.warning(f"No text extracted from page {page_num + 1}")
                except Exception as e:
                    logger.error(f"OCR failed for page {page_num + 1}: {str(e)}")
            doc.close()
            if all_data:
                return all_data
            else:
                logger.warning("No text extracted with OCR")
                return []
        except Exception as e:
            logger.error(f"OCR parsing failed: {str(e)}")
            return []
    
    def _preprocess_image_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image to improve OCR accuracy.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Preprocessed image
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding to get binary image
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Apply morphological operations to remove noise
            kernel = np.ones((1, 1), np.uint8)
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            # Apply slight blur to smooth edges
            binary = cv2.GaussianBlur(binary, (1, 1), 0)
            
            return binary
            
        except Exception as e:
            logger.warning(f"Image preprocessing failed: {str(e)}")
            return image
    
    def _parse_with_pdfplumber(self, pdf_path: str) -> List[Dict]:
        """Parse PDF using pdfplumber for better text extraction, page by page."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                all_data = []
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        print(f"\n=== PAGE {page_num + 1} PDFPLUMBER TEXT ===")
                        print(text)
                        print("=" * 50)
                        page_data = self._extract_fields_from_text(text)
                        if page_data:
                            all_data.extend(page_data)
                if all_data:
                    return all_data
                else:
                    return []
        except Exception as e:
            logger.warning(f"pdfplumber failed: {str(e)}")
            return []
    
    def _parse_with_pymupdf(self, pdf_path: str) -> List[Dict]:
        """Parse PDF using PyMuPDF as fallback, page by page."""
        try:
            doc = fitz.open(pdf_path)
            all_data = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if text:
                    print(f"\n=== PAGE {page_num + 1} PYMUPDF TEXT ===")
                    print(text)
                    print("=" * 50)
                    page_data = self._extract_fields_from_text(text)
                    if page_data:
                        all_data.extend(page_data)
            doc.close()
            if all_data:
                return all_data
            else:
                return []
        except Exception as e:
            logger.error(f"PyMuPDF failed: {str(e)}")
            return []
    
    def _extract_fields_from_text(self, text: str) -> list:
        import re
        lines = [line.strip() for line in text.splitlines()]
        data = []

        # Extract Billed To: only the part before 'Invoice Period' or other fields
        billed_to = ''
        for i, line in enumerate(lines):
            if re.search(r'billed to[:]*', line, re.IGNORECASE):
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    # Remove anything after 'Invoice Period', 'Issue date', or 'Payment terms'
                    split_line = re.split(r'Invoice Period|Issue date|Payment terms|Invoice number|,', next_line, flags=re.IGNORECASE)[0]
                    billed_to = split_line.strip()
                break

        # Extract Invoice Period
        invoice_period = ''
        for i, line in enumerate(lines):
            if re.search(r'invoice period[:]*', line, re.IGNORECASE):
                period_match = re.search(r'(\d{2}/\d{2}/\d{4}[-–]\d{2}/\d{2}/\d{4})', line)
                if period_match:
                    invoice_period = period_match.group(1)
                elif i + 1 < len(lines):
                    period_match = re.search(r'(\d{2}/\d{2}/\d{4}[-–]\d{2}/\d{2}/\d{4})', lines[i + 1])
                    if period_match:
                        invoice_period = period_match.group(1)
                break

        # Extract Issue Date
        invoice_date = ''
        for i, line in enumerate(lines):
            if re.search(r'issue date[:]*', line, re.IGNORECASE):
                date_match = re.search(r'([A-Z]{3}\s+\d{1,2},\s+\d{4})', line)
                if date_match:
                    invoice_date = date_match.group(1)
                elif i + 1 < len(lines):
                    date_match = re.search(r'([A-Z]{3}\s+\d{1,2},\s+\d{4})', lines[i + 1])
                    if date_match:
                        invoice_date = date_match.group(1)
                break

        # Find the table header
        table_start = -1
        for i, line in enumerate(lines):
            if re.search(r'company.*plan.*qty.*price.*amount', line.replace(' ', '').lower()):
                table_start = i
                break
        if table_start == -1:
            for i, line in enumerate(lines):
                if re.search(r'company|plan|qty|unit.*price|amount', line, re.IGNORECASE):
                    table_start = i
                    break
        if table_start == -1:
            return []

        # Parse table rows with improved logic
        last_company = ''
        current_company_lines = []
        
        for i in range(table_start + 1, len(lines)):
            row = lines[i].strip()
            
            # Skip summary lines
            if re.search(r'subtotal|total|amount due|hst|gst|summary|page', row, re.IGNORECASE):
                break
            if not row:
                continue
                
            # Handle 20% off discount lines
            if re.search(r'\b20% off\b', row, re.IGNORECASE):
                plan = '20% off'
                amount_match = re.search(r'(-?\$?\d+[.,]?\d*)$', row)
                amount = amount_match.group(1) if amount_match else ''
                
                # Use the last complete company name
                company_name = last_company
                if current_company_lines:
                    company_name = ' '.join(current_company_lines).strip()
                
                data.append({
                    'Billed To': billed_to if billed_to else '',
                    'Invoice Period': invoice_period,
                    'Invoice Issue Date': invoice_date,
                    'Company Name': company_name,
                    'Plan': plan,
                    'Qty': '',
                    'Unit Price': '',
                    'Amount': amount
                })
                continue
            
            # Check if this line contains plan information
            plan_keywords = [
                'Base Plan', 'Ultimate Plan', '$0 Per Usage Fee Plan', 'Premium Plan', 'Standard Plan'
            ]
            
            found_plan = False
            plan_found = None
            
            for keyword in plan_keywords:
                if keyword in row:
                    plan_found = keyword
                    found_plan = True
                    break
            
            if found_plan:
                # This is a complete row with company, plan, and pricing
                idx = row.find(plan_found)
                company_part = row[:idx].strip()
                
                # Combine with any previous company lines
                if current_company_lines:
                    company_name = ' '.join(current_company_lines + [company_part]).strip()
                    current_company_lines = []
                else:
                    company_name = company_part
                
                last_company = company_name
                
                # Extract pricing information
                after_plan = row[idx+len(plan_found):].strip()
                nums = re.findall(r'(-?\$?\d+[.,]?\d*)', after_plan)
                
                qty = ''
                unit_price = ''
                amount = ''
                
                if len(nums) >= 3:
                    qty, unit_price, amount = nums[0], nums[1], nums[2]
                elif len(nums) == 2:
                    qty, unit_price = nums[0], nums[1]
                elif len(nums) == 1:
                    qty = nums[0]
                
                data.append({
                    'Billed To': billed_to if billed_to else '',
                    'Invoice Period': invoice_period,
                    'Invoice Issue Date': invoice_date,
                    'Company Name': company_name,
                    'Plan': plan_found,
                    'Qty': qty,
                    'Unit Price': unit_price,
                    'Amount': amount
                })
                
            else:
                # This might be a continuation of a company name or a separate entry
                # Check if it looks like a company name continuation
                if not re.search(r'\$|\d+\.\d+|\d+,\d+', row):  # No pricing info
                    # Likely a company name continuation
                    current_company_lines.append(row)
                else:
                    # Try to parse as a regular row
                    parts = re.split(r'\s{2,}|\t+', row)
                    if len(parts) < 2:
                        parts = row.split()
                    
                    if len(parts) >= 5:
                        company = parts[0].strip()
                        plan = parts[1].strip()
                        qty = parts[2].strip()
                        unit_price = parts[3].strip()
                        amount = parts[4].strip()
                        
                        # Combine with any previous company lines
                        if current_company_lines:
                            company = ' '.join(current_company_lines + [company]).strip()
                            current_company_lines = []
                        
                        last_company = company
                        
                        data.append({
                            'Billed To': billed_to if billed_to else '',
                            'Invoice Period': invoice_period,
                            'Invoice Issue Date': invoice_date,
                            'Company Name': company,
                            'Plan': plan,
                            'Qty': qty,
                            'Unit Price': unit_price,
                            'Amount': amount
                        })
                    elif len(parts) >= 3:
                        # Handle cases with fewer columns
                        company = parts[0].strip()
                        plan = parts[1].strip()
                        qty = parts[2].strip() if len(parts) > 2 else ''
                        
                        # Combine with any previous company lines
                        if current_company_lines:
                            company = ' '.join(current_company_lines + [company]).strip()
                            current_company_lines = []
                        
                        last_company = company
                        
                        data.append({
                            'Billed To': billed_to if billed_to else '',
                            'Invoice Period': invoice_period,
                            'Invoice Issue Date': invoice_date,
                            'Company Name': company,
                            'Plan': plan,
                            'Qty': qty,
                            'Unit Price': '',
                            'Amount': ''
                        })
        
        return data
    
    def _post_process_data(self, data: List[Dict]) -> List[Dict]:
        """
        Post-process extracted data to fill missing values and clean up inconsistencies.
        """
        if not data:
            return data
            
        # Find the first non-empty values for header fields
        first_billed_to = ''
        first_invoice_period = ''
        first_invoice_date = ''
        
        for record in data:
            if not first_billed_to and record.get('Billed To'):
                first_billed_to = record['Billed To']
            if not first_invoice_period and record.get('Invoice Period'):
                first_invoice_period = record['Invoice Period']
            if not first_invoice_date and record.get('Invoice Issue Date'):
                first_invoice_date = record['Invoice Issue Date']
            if first_billed_to and first_invoice_period and first_invoice_date:
                break
        
        # Fill missing header values
        processed_data = []
        for record in data:
            processed_record = record.copy()
            
            # Fill missing header fields
            if not processed_record.get('Billed To') and first_billed_to:
                processed_record['Billed To'] = first_billed_to
            if not processed_record.get('Invoice Period') and first_invoice_period:
                processed_record['Invoice Period'] = first_invoice_period
            if not processed_record.get('Invoice Issue Date') and first_invoice_date:
                processed_record['Invoice Issue Date'] = first_invoice_date
            
            # Clean up company names
            if processed_record.get('Company Name'):
                company = processed_record['Company Name'].strip()
                # Remove common OCR artifacts
                company = re.sub(r'\s+', ' ', company)  # Normalize whitespace
                company = re.sub(r'[^\w\s&.,()-]', '', company)  # Remove special chars except common ones
                processed_record['Company Name'] = company
            
            # Only include records with meaningful data
            if (processed_record.get('Company Name') and 
                processed_record.get('Plan') and 
                processed_record['Company Name'].strip() and 
                processed_record['Plan'].strip()):
                processed_data.append(processed_record)
        
        return processed_data
    
    def save_to_csv(self, data: List[Dict], output_path: str) -> bool:
        """
        Save extracted data to CSV file.
        
        Args:
            data (List[Dict]): Extracted data
            output_path (str): Output file path
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)
            logger.info(f"Data saved to CSV: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            return False
    
    def save_to_excel(self, data: List[Dict], output_path: str) -> bool:
        """
        Save extracted data to Excel file.
        
        Args:
            data (List[Dict]): Extracted data
            output_path (str): Output file path
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            df = pd.DataFrame(data)
            df.to_excel(output_path, index=False, engine='openpyxl')
            logger.info(f"Data saved to Excel: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving to Excel: {str(e)}")
            return False 