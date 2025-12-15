from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import tempfile
from werkzeug.utils import secure_filename
from ComPdf import process_pdf

app = Flask(__name__)

# Use /tmp for Vercel serverless
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB limit

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        size_mb = int(request.form.get('size_mb', 20))
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)

            output_filename = f'processed_{filename}'
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

            try:
                process_pdf(input_path, size_mb, output_path)
                return render_template('result.html', filename=output_filename)
            except Exception as e:
                return f'Error processing PDF: {str(e)}'
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        return 'File not found', 404

@app.route('/favicon.ico')
def favicon():
    from flask import Response
    # Simple SVG favicon for PDF processing
    svg_favicon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="4" fill="#667eea"/>
<path d="M8 6h10l6 6v14a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2z" fill="white"/>
<path d="M18 6v6h6" fill="none" stroke="#667eea" stroke-width="1"/>
<text x="16" y="19" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#667eea" text-anchor="middle">P</text>
</svg>'''
    return Response(svg_favicon, mimetype='image/svg+xml')

# Vercel handler
def handler(event, context):
    from werkzeug.wrappers import Request
    from werkzeug.wsgi import make_environ

    # Convert Vercel event to WSGI environ
    environ = make_environ(event, context)
    request = Request(environ)

    # Process the request through Flask
    with app.request_context(environ):
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }

# Export the app for Vercel
application = app