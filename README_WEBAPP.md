# Invoice Data Extractor - Web Application

A beautiful, user-friendly web application for extracting structured data from PDF invoices. Perfect for non-technical users who need to process invoice data quickly and easily.

## 🌟 Features

- **Drag & Drop Interface**: Simply drag your PDF invoice onto the upload area
- **Multi-Format Support**: Handles both text-based and scanned/image-based PDFs
- **Multiple Export Options**: 
  - CSV download
  - Excel download  
  - Direct Google Sheets integration
- **Data Preview**: See your extracted data before downloading
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Secure Processing**: Files are automatically cleaned up after processing

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Tesseract OCR** installed (for scanned PDFs)
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - Mac: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

### Installation

1. **Clone or download** this project to your computer

2. **Open a terminal/command prompt** in the project folder

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Web Application

1. **Start the web server**:
   ```bash
   python run_webapp.py
   ```

2. **Open your web browser** and go to:
   ```
   http://localhost:5000
   ```

3. **Upload your PDF invoice** and start extracting data!

## 📖 How to Use

### Step 1: Upload Your Invoice
- Drag and drop your PDF invoice onto the upload area, or
- Click "Choose File" to browse and select your PDF

### Step 2: Process the Data
- Click "Extract Data" to start processing
- Wait for the extraction to complete (usually takes 10-30 seconds)

### Step 3: Download Your Results
- **CSV File**: Download as a comma-separated values file
- **Excel File**: Download as a Microsoft Excel file with formatting
- **Google Sheets**: Open directly in Google Sheets for online collaboration

### Step 4: Review Your Data
- Preview the first 5 records to verify the extraction
- Download the full dataset in your preferred format

## 🛠️ Technical Details

### Supported Invoice Formats
- Multi-page PDF invoices
- Scanned/image-based PDFs (using OCR)
- Text-based PDFs
- Various invoice layouts and formats

### Extracted Fields
- **Billed To**: Customer/client information
- **Invoice Period**: Billing period dates
- **Invoice Issue Date**: Date the invoice was issued
- **Company Name**: Company or service provider name
- **Plan**: Service plan or product type
- **Quantity**: Number of units
- **Unit Price**: Price per unit
- **Amount**: Total amount for the line item

### File Management
- Uploaded files are processed securely
- Output files are saved with timestamps
- Files are automatically cleaned up after 24 hours
- Manual cleanup option available

## 🔧 Configuration

### Changing the Port
Edit `run_webapp.py` and change the port number:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change 5000 to your preferred port
```

### Production Deployment
For production use, consider:
- Using a production WSGI server like Gunicorn
- Setting up HTTPS/SSL
- Configuring proper file storage
- Adding user authentication if needed

## 🐛 Troubleshooting

### Common Issues

**"No data could be extracted"**
- Ensure your PDF contains invoice information
- Try with a different PDF to test
- Check that Tesseract OCR is properly installed

**"File not found" errors**
- Make sure you're running the app from the correct directory
- Check that all required files are present

**Upload fails**
- Ensure the file is a valid PDF
- Check file size (should be under 50MB)
- Verify internet connection

### Getting Help
1. Check that all dependencies are installed correctly
2. Verify Tesseract OCR is installed and accessible
3. Try with a simple, text-based PDF first
4. Check the console output for error messages

## 📱 Mobile Usage

The web application is fully responsive and works great on:
- Smartphones
- Tablets
- Desktop computers
- All modern web browsers

## 🔒 Security Notes

- Files are processed locally on your machine
- No data is sent to external servers
- Uploaded files are automatically deleted after processing
- Output files are stored locally and can be manually cleaned up

## 🎯 Perfect For

- **Small Business Owners**: Process vendor invoices quickly
- **Accountants**: Extract data for bookkeeping
- **Office Managers**: Organize invoice data efficiently
- **Anyone**: Who needs to convert PDF invoices to spreadsheet format

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify your setup matches the requirements
3. Try with a different PDF file
4. Check the console output for detailed error messages

---

**Enjoy using the Invoice Data Extractor!** 🎉 