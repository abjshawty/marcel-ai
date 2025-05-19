# Marcel RAG

## Installation process
1. `git clone https://github.com/abjshawty/marcel-ai.git`
2. `cd marcel-ai`
3. Install dependencies (python3, python3-pip, python3-venv, docker)
4. `cp .env.example .env`
5. Edit the `.env` file to set the environment variables
6. `python -m venv env`
7. `sudo docker compose up -d`
8. `sudo docker run --name attu -p 8000:3000 -e MILVUS_URL=172.17.0.1:19530 zilliz/attu`
9. `. env/bin/activate`
10. `python -m pip install -r rq.txt`
11. Copy PDF files into the _**/pdf**_ folder
12. `flask run`

> If you have python3, python3-venv and docker installed, you can use `bash install.sh` after setting the environment variables in the `.env` file at *step 4*.