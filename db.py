from pymilvus import MilvusClient

def create():
    client = MilvusClient("milvus_demo.db")

    if client.has_collection(collection_name="demo_collection"):
        client.drop_collection(collection_name="demo_collection")
    client.create_collection(
        collection_name="demo_collection",
        dimension=768,
        # The vectors we will use in this demo has 768 dimensions.
    )

    print("Collection created.")

if __name__ == '__main__':
    create()