from flask import Flask
import functions

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
	return "<h1>🦆</h1>"

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

# if __name__ == '__main__':
	# app.run('0.0.0.0', 5000, debug=False, use_reloader=False)
