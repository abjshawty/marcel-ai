#!/bin/bash
if [[ $EUID -eq 0 ]]; then
  echo "Script is running as root (likely with sudo)."
else
  echo "Script is not running as root."
  exit 1
fi
echo "Creating Python environment."
python3 -m venv env;
echo "Installing Milvus Database."
docker compose up -d;
echo "Milvus database installed. Proceeding with installation."
container_name="attu"
if [ -f ".env" ]; then
    echo "Environment variables file exists. Proceeding with installation."
else
    echo "Environment variables file does not exist."
    echo "Creating environment variables file based on preset."
    cp .env.example .env
    nano .env
    echo "Environment variables file initialized. Proceeding with installation."
fi
source .env
if docker inspect "$container_name" > /dev/null 2>&1; then
    echo "The container $container_name exists."
    if $(docker inspect -f '{{.State.Status}}' "$container_name" | grep -q "running"); then
        echo "The container $container_name is running."
    else
        echo "The container $container_name is not running. Proceeding with startup of container."
        docker start -d "$container_name"
    fi
else
    echo "The container $container_name does not exist. Proceeding with download and startup of database GUI $container_name."
    docker run -d --name "$container_name" -p 8000:3000 -e MILVUS_URL="$MILVUS_IP:$MILVUS_PORT" zilliz/attu
fi
source env/bin/activate;
echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt --quiet;
echo "Starting daemon..."
gunicorn --name marcel --workers 1 --bind 0.0.0.0:5000 app:app --daemon
echo "Marcel AI installed successfully."
echo "The process is running on port 5000"
echo "To stop all Gunicorn processes, run 'pkill -f gunicorn'."
echo "To stop only Marcel AI, run 'ss -tulpn | grep :5000', find pid and run 'kill <pid>'."
