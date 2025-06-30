import pdfplumber
import fitz
import sys
import os
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io

def extract_text_pdfplumber(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
    except Exception as e:
        print(f"pdfplumber error: {e}")
        return None

def extract_text_pymupdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"
        doc.close()
        return text
    except Exception as e:
        print(f"PyMuPDF error: {e}")
        return None

def check_for_images(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            image_count = 0
            for page in pdf.pages:
                images = page.images
                if images:
                    image_count += len(images)
            return image_count
    except Exception as e:
        print(f"Error checking images: {e}")
        return -1

def extract_ocr_text_first_pages(pdf_path, num_pages=2):
    doc = fitz.open(pdf_path)
    for page_num in range(min(num_pages, len(doc))):
        page = doc[page_num]
        print(f"\n--- OCR TEXT FOR PAGE {page_num + 1} ---\n")
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(binary, config='--psm 6')
        print(text)
    doc.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_raw_text.py <pdf_file>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    print(f"\nChecking for images in {pdf_path}...")
    image_count = check_for_images(pdf_path)
    if image_count == -1:
        print("Could not check for images.")
    elif image_count == 0:
        print("No images detected in the PDF (likely not a scanned image).")
    else:
        print(f"Detected {image_count} images in the PDF (may be a scanned or image-based PDF).")

    print("\n--- Raw text extracted with pdfplumber ---\n")
    text1 = extract_text_pdfplumber(pdf_path)
    if text1:
        print(text1[:2000] + ("..." if len(text1) > 2000 else ""))
    else:
        print("No text extracted with pdfplumber.")

    print("\n--- Raw text extracted with PyMuPDF ---\n")
    text2 = extract_text_pymupdf(pdf_path)
    if text2:
        print(text2[:2000] + ("..." if len(text2) > 2000 else ""))
    else:
        print("No text extracted with PyMuPDF.")

    extract_ocr_text_first_pages(pdf_path, num_pages=2)

if __name__ == "__main__":
    main() 