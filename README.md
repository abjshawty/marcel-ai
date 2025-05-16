# Marcel RAG

## Installation process
1. `git clone https://github.com/abjshawty/marcel-ai.git`
2. `cd marcel-ai`
3. `cp .env.example .env`
4. Edit the `.env` file to set the environment variables
5. `python -m venv env`
6. `sudo docker compose up -d`
7. `sudo docker run --name attu -p 8000:3000 -e MILVUS_URL=172.17.0.1:19530 zilliz/attu`
8. `. env/bin/activate`
9. `python -m pip install -r rq.txt`
10. Copy PDF files into the _**/pdf**_ folder
11. `flask run`

> If you have python3 and docker installed, you can use `bash install.sh` after *step 2*.
