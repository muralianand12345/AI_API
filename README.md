# LLM ChatBot using FastAPI

A chat bot implementation using FastAPI framework and Large Language Models.

## Requirements

- Python 3.9 or higher
- Docker (optional)
- Poetry (recommended) or pip
- [Groq API Key](https://console.groq.com) and [Nvidia API Key](https://build.nvidia.com/nvidia/nv-embedqa-mistral-7b-v2) (You can also go with any alternative LLMs and Embeddings)

## Installation

### Option 1: Using Poetry (Recommended)

```shell
# Install Poetry globally if you haven't already
pip install poetry

# Install dependencies and create virtual environment
poetry install

# Activate the virtual environment
poetry shell

# Run the application
python app.py
```

### Option 2: Using requirements.txt

```shell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Option 3: Using Docker

```shell
# Build the Docker image
docker build -t llm-chatbot .

# Run the container
docker run -d -p 8000:8000 llm-chatbot

# Or use docker-compose
docker-compose up -d
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
GROQ_API_KEY=https://console.groq.com
NVIDIA_API_KEY=https://build.nvidia.com/nvidia/nv-embedqa-mistral-7b-v2
```

## Usage

Once the application is running, you can access:

- API documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`

## Development

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Update and test code.
5. Submit a pull request

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# LLM ChatBot using FastAPI

[Previous sections remain the same...]

## FAQ

### How to Change LLM and Embedding Models

You can customize the LLM and embedding models by modifying the `config.py` file. Below are several examples of different configurations:

#### 1. Using Groq and NVIDIA

```python
from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
import os

# Configure models
llm = ChatGroq(
    model="llama-3.2-90b-text-preview",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY")
)

embedding = NVIDIAEmbeddings(
    model="nvidia/nv-embedqa-mistral-7b-v2",
    truncate="START",
    api_key=os.getenv("NVIDIA_API_KEY")
)
```

#### 2. Using Ollama and HuggingFace

First, install required packages:
```bash
pip install langchain-ollama langchain-huggingface
```

Then update your configuration:
```python
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

# Configure models
llm = ChatOllama(
    model="llama3:8b",  # or other models like "mistral", "neural-chat"
    temperature=0
)

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cuda'}  # Optional: for GPU support
)
```

#### 3. Using OpenAI

First, install the package:
```bash
pip install langchain-openai
```

Then update your configuration:
```python
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Configure models
llm = ChatOpenAI(
    model="gpt-40",  # or "gpt-40-mini"
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

embedding = OpenAIEmbeddings(
    model="text-embedding-3-large",  # or "text-embedding-3-small"
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### Environment Variables

Make sure to set the appropriate environment variables in your `.env` file based on your chosen models:

```env
# For Groq
GROQ_API_KEY=your-groq-api-key

# For NVIDIA
NVIDIA_API_KEY=your-nvidia-api-key

# For OpenAI
OPENAI_API_KEY=your-openai-api-key

# For HuggingFace
HUGGINGFACE_API_KEY=your-huggingface-api-key  # If using API
```

### Model Selection Tips

1. **Local Models (Ollama)**
   - Best for development and testing
   - No API costs
   - Requires more computational resources

2. **Cloud Models (OpenAI, Groq, NVIDIA)**
   - Better performance
   - API costs apply (Groq has free tier)
   - No local computational requirements

3. **Embedding Models**
   - Local: HuggingFace embeddings are free but require more RAM
   - Cloud: OpenAI/NVIDIA embeddings are faster but have API costs