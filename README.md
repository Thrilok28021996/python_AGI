# Python AGI

Ask questions to your python Agents and get your work done. A small take on understanding the AGI using the CAMEL AGENT from langchain.

## Prerequisites

1. Install [Ollama](https://ollama.ai) on your system
2. Pull the llama3.2 model:
   ```bash
   ollama pull llama3.2
   ```
3. Verify Ollama is running:
   ```bash
   ollama list
   ```

## Install the necessary packages

Create an environment using anaconda or python venv and then run the below command:

```bash
pip install -r requirements.txt
```

**Note:** This project uses Ollama (local LLM), not OpenAI. No API keys required for basic usage.

## Run the agent

To run the agent:

1. First change the task you want to complete in the `camel.py` file or you can run with the default task.
2. Go to the location of the Folder Python_AGI and type:
   ```bash
   python camel.py
   ```

## Configuration

If you want to customize the Ollama model or base URL, you can:
1. Copy `example.env` to `.env`:
   ```bash
   cp example.env .env
   ```
2. Edit the `.env` file to change `OLLAMA_MODEL` or `OLLAMA_BASE_URL` (optional)