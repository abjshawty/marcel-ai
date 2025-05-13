# Marcel DB

- cd marcel-ai
- python -m venv env
- . env/bin/activate
- python -m pip install -r rq.txt
- python -m spacy download en_core_web_lg

- sudo docker compose up -d
- sudo docker run --name attu -p 8000:3000 -e MILVUS_URL=172.17.0.1:19530 zilliz/attu