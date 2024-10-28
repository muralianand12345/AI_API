# LLM ChatBot using FastAPI

A chat bot implementation using FastAPI framework and Large Language Models.

## Requirements

- Python 3.9 or higher
- Docker (optional)
- Poetry (recommended) or pip

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
4. Run tests:
   ```shell
   pytest tests/
   ```
5. Submit a pull request

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.