# CustomPdfSize

A tool to compress and adjust PDF files to a specific size.

## Features

- Compress PDF files using Ghostscript
- Pad or trim PDFs to exact target size
- Web UI for easy file upload and download

## Requirements

- Python 3.x
- Ghostscript (gs command)

## Installation

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure Ghostscript is installed:
   - On macOS: `brew install ghostscript`
   - On Ubuntu: `sudo apt-get install ghostscript`

## Usage

### Command Line

Run the script directly (modify ComPdf.py for your input):

```python
python ComPdf.py
```

### Web UI

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Start the Flask app:
   ```bash
   python app.py
   ```

3. Open your browser to `http://127.0.0.1:5000/`

4. Upload a PDF file and specify the target size in MB.

5. Download the processed PDF.

## How it Works

1. Compresses the PDF using Ghostscript with screen quality settings.
2. Adjusts the file size to exactly match the target by padding with zeros or trimming content (while trying to preserve PDF validity).
