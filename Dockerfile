FROM python:3.10-slim

# Install system dependencies for Tesseract, OpenCV, and PDF tools
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \
    build-essential \
    gcc \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose port for web server
EXPOSE 10000

# Start the app with gunicorn
CMD ["gunicorn", "run_webapp:app", "--bind", "0.0.0.0:10000"] 