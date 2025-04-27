## Demos on how to use LLM's.

This repo is meant for simple demonstrations on use of LLM's. It has some very basic chat and retrieval examples using some of the most commonly used api's and models.

* Ollama, on local and using docker.
* OpenAI api with HuggingFace (HF) and Ollama.
* Embeddings with Langchain, HF and Ollama.
* Vector stores with retrieval.
* etc., more incoming.

The `/documents/` folder includes a couple of sample documents for context retrieval.

#### Dependencies

The dependencies are listed in `pyproject.toml`, and can be installed easiest with uv, by running `uv sync`. If you are not familiar with uv, google: install uv. It is by far the best/fastest/most robust manager, and still allows using pip in same projects. Cuda should be automatically enabled if you have sufficient gpu.

If you have issues with cuda, remove all the dependencies, and install `uv add pip`. In order to use gpu for embeddings or model inference, you may need to install torch manually before installing other dependecies -- try this only after, if the default conf doesn't enable cuda. Go to: https://pytorch.org/get-started/locally/ and follow instructions for your cuda version. torchvision can cause some compatibility issues, so skip that. Use `uv run pip <see page for instructions>` according to the pytorch instructions, and only after that start adding the other dependencies.

You can obviously just use pip and install the dependencies listed in `pyproject.toml`. If you use pip, you should consider first installing cuda enabled torch following the instructions in: https://pytorch.org/get-started/locally/. 
