from werkzeug.utils import secure_filename
from flask import Flask, request
import functions
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'pdf/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Test route
@app.route('/hello', methods=['GET'])
def hello():
	return "<h1>🦆</h1>"

# Vector search route
@app.route('/q/<q>', methods=['GET', 'POST'])
def question(q):
	result = functions.vector_search(q)
	return f"<p>{result.message}</p>"

# Embed route
@app.route('/embed', methods=['GET'])
def embed():
	return f"<p>{functions.embed_files().message}</p>"

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
	if 'file' not in request.files:
		print(request.files)
		return 'No file part', 400
	file = request.files['file']
	if file.filename == '':
		return 'No selected file', 400
	if file and file.filename.lower().endswith('.pdf'):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return 'File uploaded successfully', 200
	return 'Invalid file type', 400

if __name__ == '__main__':
	app.run('0.0.0.0', 5000, debug=False, use_reloader=False)
