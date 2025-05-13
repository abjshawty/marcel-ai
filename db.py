from pymilvus import MilvusClient, model
import json, os, spacy
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_milvus import Milvus

from langchain_openai import AzureOpenAIEmbeddings
embeddings = AzureOpenAIEmbeddings()

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
def file_embedding():
    pdf_path = os.curdir + "/pdf"
    documents = []
    for file in os.listdir(pdf_path):
        if file.endswith(".pdf"):
            uri = os.path.join(pdf_path, file)
            print(uri)
            loader = PyPDFLoader(uri)
            documents.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_splits = text_splitter.split_documents(documents)
    # embedding_fn = model.DefaultEmbeddingFunction()
    print(type(all_splits))
    # embeddings = embedding_fn.encode_documents(all_splits)
    vectorstore = Milvus.from_documents( 
        documents=all_splits,
        embedding=embeddings,
        connection_args={
            "uri": "http://localhost:19530",
        },
        drop_old=False,  
    )
    vectorstore.similarity_search("Parle moi du processus de ventilation des encaissements.")
    
def init():
    client = MilvusClient("demo.db")
    if client.has_collection(collection_name="saphia"):
        client.drop_collection(collection_name="saphia")
    client.create_collection(
        collection_name="saphia",
        dimension=128,
    )
    return client
if __name__ != "__main__":
    custom_embedding()
    print("Done")
else:
    file_embedding()