from pymilvus import MilvusClient, model
import json, spacy
def create(client):
    if client.has_collection(collection_name="saphia"):
        client.drop_collection(collection_name="saphia")
    client.create_collection(
        collection_name="saphia",
        dimension=128,
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

def custom_embedding():
    titles = [
        "Interstellar",
        "The Matrix",
        "The Godfather",
    ]
    nlp = spacy.load("en_core_web_lg")
    vectors = [nlp(doc).vector for doc in titles]
    data = [
        {"vector": vectors[i][:128].tolist(), "title": titles[i]}
        for i in range(len(vectors))
    ]
    with open("movies.json", "w") as f:
        json.dump(data, f, indent=4)
    return data


if __name__ != "__main__":
    # db = MilvusClient("demo.db")
    # create(db)
    # embed_test()
    custom_embedding()
    print("Done")
