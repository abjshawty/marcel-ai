from flask import Flask
import functions

app = Flask(__name__)

@app.route('/q/<q>', methods=['GET', 'POST'])
def question(q):
	result = functions.vector_search(q)
	return f"<p>{result.message}</p>"

@app.route('/embed', methods=['GET'])
def embed():
	return f"<p>{functions.embed_files().message}</p>"

@app.route('/embed/<file>', methods=['POST'])
def embed_file(file):
	return f"<p>{functions.embed_file(file).message}</p>"
