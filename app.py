from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import tempfile
from werkzeug.utils import secure_filename
from ComPdf import process_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
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
@app.route('/favicon.svg')
def favicon():
    from flask import send_from_directory, make_response
    try:
        response = send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.svg',
            mimetype='image/svg+xml'
        )
        response.headers['Cache-Control'] = 'public, max-age=43200'
        return response
    except:
        # Fallback inline SVG if file not found
        from flask import Response
        svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="4" fill="#667eea"/><path d="M8 6h10l6 6v14a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2z" fill="white"/><path d="M18 6v6h6" fill="none" stroke="#667eea" stroke-width="1.5"/><text x="16" y="20" font-family="Arial" font-size="9" font-weight="bold" fill="#667eea" text-anchor="middle">PDF</text></svg>'''
        return Response(svg, mimetype='image/svg+xml')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)