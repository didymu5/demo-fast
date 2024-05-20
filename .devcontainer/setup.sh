#!/bin/sh
# set -eu

echo "Installing libraries from requirements.txt..."
chmod +x ./requirements.txt && pip install -r ./requirements.txt
echo "Done."
echo

# Check if the "redis" container is running
# if ! docker ps --filter "status=running" --format "{{.Names}}" | grep -q "redis"; then
#   # If the "redis" container is not running, start it using docker-compose
#   docker-compose -f ./docker-compose.yml up -d
# else
#   echo "The 'redis' container is already running."
# fi

echo
echo "Let's set up your development environment..."
echo
# echo "Please enter your OpenAI API key found here: https://platform.openai.com/account/api-keys:"
# read -r OPENAI_API_KEY

# Export the OPENAI_API_KEY environment variable
# export OPENAI_API_KEY
# export DATASTORE=redis 
# export BEARER_TOKEN=footoken
# export PLUGIN_HOSTNAME=https://$CODESPACE_NAME-8000.$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN 



echo "Once your app is running, use the following URL to use this plugin in the OpenAI Plugin store:"
echo $PLUGIN_HOSTNAME
echo
echo "Enter 'footoken' if OpenAI prompts you for a Bearer Token"