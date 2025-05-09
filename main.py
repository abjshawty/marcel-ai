from flask import Flask
from pymilvus import MilvusClient, model
def create(client):
    if client.has_collection(collection_name="demo_collection"):
        client.drop_collection(collection_name="demo_collection")
    client.create_collection(
        collection_name="demo_collection",
        dimension=768,
        # The vectors we will use in this demo has 768 dimensions.
    )

    print("Collection created.")

def embed_test():
    # If connection to https://huggingface.co/ failed, uncomment the following path
    # import os
    # os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

    # This will download a small embedding model "paraphrase-albert-small-v2" (~50MB).

    embedding_fn = model.DefaultEmbeddingFunction()
    docs = [
        "Artificial intelligence was founded as an academic discipline in 1956.",
        "Alan Turing was the first person to conduct substantial research in AI.",
        "Born in Maida Vale, London, Turing was raised in southern England.",
    ]

    vectors = embedding_fn.encode_documents(docs)
    # The output vector has 768 dimensions, matching the collection that we just created.
    print("Dim:", embedding_fn.dim, vectors.shape)
    # Each entity has id, vector representation, raw text, and a subject label that we use
    # to demo metadata filtering later.
    data = [
        {"id": i, "vector": vectors[i], "text": docs[i], "subject": "history"}
        for i in range(len(vectors))
    ]

    # print("Data has", len(data), "entities, each with fields: ", data[0].keys())
    # print("Vector dim:", len(data[0]["vector"]))

app = Flask(__name__)
db = MilvusClient("demo.db")
create(db)

@app.route("/")
def hello():
	return "<h1>Konnichiwa, bitches</h1>"

@app.route('/question', methods=['GET'])
def quest():
	q = "Parle moi du processus de mutation"
	# Ask Milvus
