# GPTALK
GPTalk is a client-server application which lets you use openai API with the GPT models.

## Features
Supports openai ChatCompletion API endpoint.
- Select the model you want to use
- Uses initial 'system' role to configure default behaviour (defaults to 'bro mode' for the lulz 🤣)
- Keeps track of the total tokens of the conversation
- Saves all your chats into a local sqlite database
- Supports markdown syntax
- Adds tl;dr of every chat after the first message
________________________________________________________________
## How to use
### Using the install script:
Requires [Docker](https://www.docker.com/products/docker-desktop/). 
* Register to openai and get your API key [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) (there's a generous free allowance)
* Run the below command
```bash
./install.sh -key {YOUR OPENAI API KEY}
```
* Navigate to http://localhost and start using the GPT models 😄

The install script will: 
1. build, start and setup two docker containers:
   - gptalk-client
   - gptalk-server
2. create a docker network for the containers to communicate between each other
3. create a default user configuration file within {your-install-folder}/gptalk-server/user_config/config.yml
________________________________________________________________
## Overview:
### Mobile View
![](https://github.com/Joe85gr/GPTalk/blob/main/docs/imgs/mobile1.png?raw=true)
![](https://github.com/Joe85gr/GPTalk/blob/main/docs/imgs/mobile2.png?raw=true)

### Desktop View
![](https://github.com/Joe85gr/GPTalk/blob/main/docs/imgs/desktop.png?raw=true)