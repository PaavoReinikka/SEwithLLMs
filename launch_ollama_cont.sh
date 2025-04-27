#!/bin/bash
docker run -d -v ollama:/root/.ollama -p 11435:11434 --name ollama ollama/ollama

# you can enter the container with:
# docker exec -it ollama bash
# and run the following command to pull a model (takes a while):
# ollama pull <model_name>
# run ollama serve to start the server (might not be needed if it's already running):
# ollama serve
# exit the container with:
# exit
# on local machine, you can access the server on port 11435:
# curl http://localhost:11435 --> "ollama is running"
# to stop the container, run:
# docker stop ollama
# to remove the container, run:
# docker rm ollama