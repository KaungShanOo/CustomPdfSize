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

## Deployment Options

### 🚂 Railway (Highly Recommended)

Railway is the best platform for your PDF processing app because it handles large files, system dependencies, and Python apps seamlessly.

#### Why Railway?
- ✅ **No file size limits** - Handle 100MB+ PDFs easily
- ✅ **System dependencies** - Ghostscript works out of the box
- ✅ **Persistent storage** - Files don't disappear between requests
- ✅ **Python native** - Excellent Flask support
- ✅ **Free tier** - 512MB RAM, perfect for PDF processing
- ✅ **Auto-scaling** - Handles traffic automatically

#### Deployment Steps

1. **Create Railway account** at [railway.app](https://railway.app)

2. **Connect your GitHub repository**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select this repository

3. **Deploy**:
   - Railway auto-detects Python and installs dependencies from `requirements.txt`
   - Uses `python app.py` as the start command
   - Your app will be live at `your-project-name.railway.app`

#### Pricing
- **Free**: 512MB RAM, 1GB disk, enough for most users
- **Hobby**: $5/month for more resources
- **Pro**: $10/month for production workloads

### 🏗️ Other Good Alternatives

#### Render
- **Free tier**: 750MB RAM, good for testing
- **Deployment**: Connect GitHub repo, select Python
- **Pros**: Simple, reliable
- **Cons**: Cold starts, RAM limits

#### Heroku
- **Pricing**: $7/month basic dyno
- **Pros**: Mature, reliable platform
- **Cons**: More expensive, complex scaling

#### DigitalOcean App Platform
- **Pricing**: Starts at $12/month
- **Pros**: Good performance, easy scaling
- **Cons**: More expensive than Railway

### 🚫 Not Recommended for This App

#### Vercel
- **Issues**: 5MB file limit on free tier, Ghostscript not available, 30s timeout
- **Only viable with Pro plan** ($20/month) and still has limitations

## Local Development

For local testing with large files:

```bash
source venv/bin/activate
python app.py
```

Visit `http://127.0.0.1:5000/` to test your app locally.
