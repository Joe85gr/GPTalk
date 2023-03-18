#!/bin/bash

set -e

# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

app_name='gptalk'
client_name=$app_name-client
server_name=$app_name-server
network_name=$app_name-network
user_config_dir='user_config'
server_config_filename='config.yml'

# Parse command-line arguments
while getopts ":key:" opt; do
  case ${opt} in
    key )
      OPENAI_API_KEY=$OPTARG
      ;;
    \? )
      echo "${Red} Invalid option: -$OPTARG${Color_Off}" >&2
      exit 1
      ;;
    : )
      echo "${Red} Option -$OPTARG requires an argument.${Color_Off}" >&2
      exit 1
      ;;
  esac
done

# Check if any parameters were provided
if [ $# -eq 0 ]; then

  echo "${Yellow}Warning: No OpenAI API key provided. Attempting to retrieve OpenAI API key from environmental variables..${Color_Off}"
  OPENAI_API_KEY=${OPENAI_API_KEY}

  if [ -z "${OPENAI_API_KEY}" ]; then
    echo "${Red}Error: Unable to retrieve OpenAI API key from environmental variables. Please provide an OpenAI API key with the -key parameter.${Color_Off}"
    exit 1
  else
    echo "${Green}OpenAI API key loaded successfully.{Color_Off}"
  fi

fi

# Check if OPENAI_API_KEY is set
if [ -z "${OPENAI_API_KEY}" ]; then
  echo "${Red}Error: -key parameter is required. Please provide an OpenAI API key with the -key parameter.${Color_Off}"
  exit 1
fi

if [[ ! -e ./$server_name/$user_config_dir ]]; then
    mkdir ./$server_name/$user_config_dir
    echo $'openai:\n    placeholder: IGNORE_ME' >> ./$server_name/$user_config_dir/config.yml
fi

# Removes existing containers if exists
docker rm --force $server_name || true
docker rm --force $client_name || true

# Build Docker images
docker build -t $server_name:latest -f ./$server_name.Dockerfile .
docker build -t $client_name:latest -f ./$client_name.Dockerfile .

# Create docker networks so that the containers can communicate with each other
docker network rm $network_name || true
docker network create --subnet=172.20.0.0/16 --driver bridge $network_name

# Run Docker containers
docker run -d --name $server_name --network $network_name --ip 172.20.0.10 -p 8000:8000 -v $(pwd)/$server_name/user_config:/app/user_config -e OPENAI_API_KEY=${OPENAI_API_KEY} $server_name:latest
docker run -d --name $client_name --network $network_name --ip 172.20.0.11 -p 80:80 $client_name:latest
