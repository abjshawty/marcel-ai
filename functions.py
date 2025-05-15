import constants, os
from langchain_milvus import Milvus
from pymilvus import connections, Collection
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def embed_file(): # TODO: Implement unique file embedding
    try:
        pass
    except Exception as e:
        print(constants.EMBED_FILE_FAILURE, e)
        return constants.Failure(str(e))

def embed_files():
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=constants.RECURSIVE_CHARACTER_TEXT_SPLITTER_CHUNK_SIZE, chunk_overlap=constants.RECURSIVE_CHARACTER_TEXT_SPLITTER_CHUNK_OVERLAP)
        folder = os.curdir + constants.PDF_FOLDER
        files = []
        for file in os.listdir(folder):
            if file.endswith(".pdf"):
                files.extend(
                    PyPDFLoader(os.path.join(folder, file))
                    .load()
                )
        Milvus.from_documents( 
            documents=text_splitter.split_documents(files),
            embedding=constants.embeddings,
            connection_args={
                "uri": constants.MILVUS_URI,
            },
            collection_name="saphia",
            drop_old=True,  
        )
        return constants.Success(constants.EMBED_FOLDER_SUCCESS)
    except Exception as e:
        print(constants.EMBED_FOLDER_FAILURE, e)
        return constants.Failure(constants.EMBED_FOLDER_FAILURE + str(e))

def vector_search(user_input: str):
    try:
        connections.connect("default", host=constants.MILVUS_IP, port=constants.MILVUS_PORT)
        user_vector = constants.embeddings.embed_query(user_input)
        search_params = {
            "metric_type": "L2",
            "offset": 0,
            "params": {"nprobe": 10},
            "ignore_growing": False,
        }
        collection = Collection("saphia")
        results = collection.search(
            data=[user_vector],
            anns_field="vector",
            param=search_params,
            limit=10,
            output_fields=["text"],
        )
        paragraph = ""
        for result in results:
            for idx, hit in enumerate(result):
                score = hit.distance
                title = hit.entity.get("text")
                phrase = f"{idx + 1}. {title} (score: {score})\n<br>"
                paragraph += phrase
        return constants.Success(paragraph)
    except Exception as e:
        print(constants.VECTOR_SEARCH_FAILURE, e)
        return constants.Failure(str(e))
