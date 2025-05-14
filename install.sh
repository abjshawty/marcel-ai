#!/bin/bash
if [[ $EUID -eq 0 ]]; then
  echo "Script is running as root (likely with sudo)."
else
  echo "Script is not running as root."
  exit 1
fi
python3 -m venv env;
docker compose up -d;
container_name="attu"
if [ -f ".env" ]; then
    echo "Environment variables file exists"
else
    echo "Environment variables file does not exist"
    cp .env.example .env
    nano .env
fi
if docker inspect "$container_name" > /dev/null 2>&1; then
    echo "The container $container_name exists."
    if $(docker inspect -f '{{.State.Status}}' "$container_name" | grep -q "running"); then
        echo "The container $container_name is running."
    else
        echo "The container $container_name is not running."
        docker start "$container_name"
    fi
else
    echo "The container $container_name does not exist."
    source .env
    docker run --name "$container_name" -p 8000:3000 -e MILVUS_URL="$MILVUS_IP:$MILVUS_PORT" zilliz/attu
fi
source env/bin/activate;
python3 -m pip install -r requirements.txt;
flask run;
