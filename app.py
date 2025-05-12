from flask import Flask
from data import run_once

app = Flask(__name__)
@app.route("/")
def hello():
	return "<h1>Konnichiwa, bitches</h1>"

@app.route('/q/<q>', methods=['GET', 'POST'])
def quest(q):
	# Ask Milvus
	return "<h1>" + run_once(q) + "</h1>"

@app.route('/echo/<q>', methods=['GET'])
def echo(q):
	return "<h1>" + q + "</h1>"
