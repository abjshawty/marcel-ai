#!/bin/bash
if [[ $EUID -eq 0 ]]; then
  echo "Script is running as root (likely with sudo)."
else
  echo "Script is not running as root."
  exit 1
fi
echo "Killing the Marcel process."
ps ax | grep marcel | grep -v grep | head -n 1 | awk '{print $1}' | xargs kill
docker stop attu
docker compose down
docker system prune -a -y
echo "You can safely delete the parent folder."
