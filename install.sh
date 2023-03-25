#!/bin/bash

set -e

app_name='gptalk'
client_name=$app_name-client
server_name=$app_name-server
redis_name=$app_name-redis
network_name=$app_name-network
user_config_dir='user_config'
server_config_filename='config.yml'

CLIENT_PORT=6222
SERVER_PORT=8222
REDIS_PORT=6379

while getopts k: flag
do
  # echo ${OPTARG}
    case "${flag}" in
        # p) CLIENT_PORT=${OPTARG};;
        k) API_KEY=${OPTARG};;
    esac
done

# Check if any parameters were provided
if [ $# -eq 0 ]; then

  echo "Warning: No OpenAI API key provided. Attempting to retrieve OpenAI API key from environmental variables.."
  API_KEY=${OPENAI_API_KEY}

  if [ -z "${OPENAI_API_KEY}" ]; then
    echo "Error: Unable to retrieve OpenAI API key from environmental variables. Please provide an OpenAI API key with the -key parameter."
    exit 1
  else
    echo "OpenAI API key loaded successfully."
  fi

fi

# Check if OPENAI_API_KEY is set
if [ -z "${API_KEY}" ]; then
  echo "Error: -key parameter is required. Please provide an OpenAI API key with the -key parameter."
  exit 1
fi

if [[ ! -e ./$server_name/$user_config_dir ]]; then
    mkdir ./$server_name/$user_config_dir
    echo $'gptalk:\n    logging_level: INFO\n    max_log_size: 10 # max log size in MB\n    client_address: http://localhost:'${CLIENT_PORT}$'\n\nopenai:\n    behaviour: "talk like a bro, use markdown code highlighting"' >> ./$server_name/$user_config_dir/config.yml
fi

# Removes existing containers if exists
docker rm --force $server_name || true
docker rm --force $client_name || true

# Build Docker images
docker build -t $server_name:latest -f ./$server_name.Dockerfile .
docker build -t $client_name:latest -f ./$client_name.Dockerfile .

# Create docker networks so that the containers can communicate with each other
docker network rm $network_name || true
docker network create --subnet=172.25.0.0/16 --driver bridge $network_name || true

# Run Docker containers
docker run -d --name redis --network $network_name --ip 172.25.0.12 -p 6379:6379 redis || true
docker run -d --name $server_name --network $network_name --ip 172.25.0.10 -p ${SERVER_PORT}:8222 -v $(pwd)/$server_name/user_config:/app/user_config -e OPENAI_API_KEY=${API_KEY} $server_name:latest
docker run -d --name $client_name --network $network_name --ip 172.25.0.11 -p ${CLIENT_PORT}:80 $client_name:latest
