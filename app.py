from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from invoice_parser import InvoiceParser
import pandas as pd
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Use environment variable in production

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET'])
def upload_redirect():
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename
            unique_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            base_name = os.path.splitext(filename)[0]
            pdf_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
            
            # Save uploaded file
            file.save(pdf_path)
            
            # Initialize parser and extract data
            parser = InvoiceParser()
            extracted_data = parser.parse_pdf(pdf_path)
            
            if not extracted_data:
                flash('No data could be extracted from the PDF. Please ensure it contains invoice information.', 'error')
                return redirect(url_for('index'))
            
            # Create output files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = f"{base_name}_{timestamp}.csv"
            excel_filename = f"{base_name}_{timestamp}.xlsx"
            
            csv_path = os.path.join(OUTPUT_FOLDER, csv_filename)
            excel_path = os.path.join(OUTPUT_FOLDER, excel_filename)
            
            # Save as CSV
            parser.save_to_csv(extracted_data, csv_path)
            
            # Save as Excel
            parser.save_to_excel(extracted_data, excel_path)
            
            # Clean up uploaded file
            os.remove(pdf_path)
            
            # Prepare response data
            result = {
                'success': True,
                'records_extracted': len(extracted_data),
                'csv_filename': csv_filename,
                'excel_filename': excel_filename,
                'preview_data': extracted_data[:5]  # First 5 records for preview
            }
            
            flash(f'Successfully extracted {len(extracted_data)} records from the invoice!', 'success')
            return render_template('results.html', result=result)
            
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload a PDF file.', 'error')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/open-google-sheets/<filename>')
def open_google_sheets(filename):
    # Instead of trying to upload automatically, redirect to Google Sheets and show instructions
    flash('In Google Sheets, go to File > Import and upload your downloaded CSV file.', 'info')
    return redirect('https://sheets.new')

@app.route('/cleanup/<filename>')
def cleanup_file(filename):
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash('File cleaned up successfully', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error cleaning up file: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port) 