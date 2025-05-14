# Marcel RAG

## Installation process
1. `git clone https://github.com/abjshawty/marcel-ai.git`
2. `cd marcel-ai`
3. `python -m venv env`
4. `. env/bin/activate`
5. `python -m pip install -r rq.txt`
6. `python -m spacy download fr_core_news_sm`
7. `sudo docker compose up -d`
8. `sudo docker run --name attu -p 8000:3000 -e MILVUS_URL=172.17.0.1:19530 zilliz/attu`
9. Copy PDF files into the _**/pdf**_ folder
10. `flask run`
