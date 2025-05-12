import json, spacy
from pymilvus import connections, Collection, MilvusException

nlp = spacy.load("en_core_web_lg")
def run():
	try:
		connections.connect("default", host="localhost", port="19530")
		while True:
			user_input = input("Enter your question: ")
			if user_input.lower() == "exit":
				break
			user_input_doc = nlp(user_input)
			user_vector = user_input_doc.vector[:128].tolist()
			search_params = {
				"metric_type": "L2",
				"offset": 0,
				"params": {"nprobe": 10},
				"ignore_growing": False,
			}
			collection = Collection("Movies")
			results = collection.search(
				data=[user_vector],
				anns_field="vector",
				param=search_params,
				limit=5,
                output_fields=["title"],
			)
			for idx, hit in enumerate(results[0]):
				score = hit.distance
				title = hit.entity.get("title")
				print(f"{idx + 1}. {title} (score: {score})")
	except MilvusException as e:
		print(e)
		return
	finally:
		connections.disconnect("default")
	
	with open("movies.json", "r") as f:
		data = json.load(f)
		vectors = [nlp(doc["title"]).vector for doc in data]
		collection.insert([vectors])

def run_once(user_input: str):
	try:
		connections.connect("default", host="localhost", port="19530")
		user_input_doc = nlp(user_input)
		user_vector = user_input_doc.vector[:128].tolist()
		search_params = {
			"metric_type": "L2",
			"offset": 0,
			"params": {"nprobe": 10},
			"ignore_growing": False,
		}
		collection = Collection("Movies")
		results = collection.search(
			data=[user_vector],
			anns_field="vector",
			param=search_params,
			limit=5,
			output_fields=["title"],
		)
		for idx, hit in enumerate(results[0]):
			score = hit.distance
			title = hit.entity.get("title")
			print(f"{idx + 1}. {title} (score: {score})")
		return f"1. {results[0][0].entity.get('title')} (score: {results[0][0].distance})"
	except MilvusException as e:
		print(e)
		return
	finally:
		connections.disconnect("default")
	
if __name__ == "__main__":
	run()
