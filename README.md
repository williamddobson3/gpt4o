# GPT-4o Chatbot

A chatbot implementation using high-quality open-source language models from Hugging Face. This project runs models locally without requiring API keys. Currently configured to use **Qwen2.5-7B-Instruct** (a high-quality alternative).

## Features

- 🤖 Local model execution (no API keys needed)
- 💬 Interactive CLI interface
- 📝 Conversation history management
- ⚙️ Configurable parameters (temperature, top_p, etc.)
- 🚀 GPU support (CUDA) when available

## Requirements

- Python 3.8 or higher
- PyTorch (will be installed via requirements.txt)
- At least 8GB RAM (16GB+ recommended)
- GPU with CUDA support (optional, but recommended for better performance)

### Optional Dependencies

For quantization support (8-bit/4-bit loading to reduce memory usage):
```bash
pip install bitsandbytes
```

## Installation

### Local Installation

1. **Clone or download this project**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   
   **For GPU (CUDA):**
   ```bash
   # Install PyTorch with CUDA support first
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   # Then install other dependencies
   pip install -r requirements.txt
   ```
   
   **For CPU only:**
   ```bash
   pip install -r requirements.txt
   ```

### VPS Installation (Quick Start)

For VPS deployment with GPU:

**Quick setup (if venv exists):**
```bash
source venv/bin/activate
chmod +x quick_start_vps.sh
./quick_start_vps.sh
```

**Full deployment:**
```bash
chmod +x deploy.sh
./deploy.sh
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Usage

### Basic Usage

Run the chatbot:
```bash
python main.py
```

The model will be downloaded automatically on first run (this may take some time depending on your internet connection).

### Commands

Once the chatbot is running, you can use these commands:

- Type your message and press Enter to chat
- `/clear` - Clear conversation history
- `/history` - View conversation history
- `/exit` or `/quit` - Exit the chatbot
- `/help` - Show help message

### Example Session

```
You: Hello! What can you do?
Assistant: Hello! I'm a helpful assistant powered by GPT-4o. I can help you with various tasks like answering questions, having conversations, providing information, and more. How can I assist you today?

You: /history
[Shows conversation history]

You: /clear
Conversation history cleared.

You: /exit
Goodbye!
```

## Configuration

Edit `config.py` to customize the chatbot behavior:

- `MODEL_NAME`: Hugging Face model identifier
- `DEVICE`: "cuda" or "cpu"
- `MAX_NEW_TOKENS`: Maximum tokens to generate (default: 512)
- `TEMPERATURE`: Sampling temperature (0.0-1.0, default: 0.7)
- `TOP_P`: Nucleus sampling parameter (default: 0.9)
- `SYSTEM_PROMPT`: System message for the chatbot
- `MAX_HISTORY_LENGTH`: Number of previous messages to keep in context

### GPU Support

The chatbot automatically detects and uses GPU if available. No configuration needed!

To force a specific device, set the environment variable:
```bash
# Force CPU
export FORCE_DEVICE=cpu
python main.py

# Force CUDA
export FORCE_DEVICE=cuda
python main.py
```

Or modify `config.py` directly.

**Check GPU availability:**
```bash
python check_gpu.py
```

### VPS Deployment

For deploying on a VPS with GPU, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Project Structure

```
.
├── main.py           # CLI entry point
├── chatbot.py        # Core chatbot implementation
├── config.py         # Configuration settings
├── example.py        # Example script for programmatic usage
├── requirements.txt  # Python dependencies
├── .gitignore        # Git ignore file
└── README.md         # This file
```

## Programmatic Usage

You can also use the chatbot programmatically in your own scripts:

```python
from chatbot import ChatBot

# Initialize
chatbot = ChatBot()

# Chat
response = chatbot.chat("Hello!")
print(response)

# Clear history
chatbot.clear_history()

# Get history
history = chatbot.get_history()
```

See `example.py` for a complete example.

## Troubleshooting

### Model Download Issues
- Ensure you have a stable internet connection
- The model will be cached in `~/.cache/huggingface/` after first download
- If download fails, try again or check Hugging Face status

### Memory Issues
- Reduce `MAX_NEW_TOKENS` in `config.py`
- Enable quantization: set `LOAD_IN_8BIT = True` or `LOAD_IN_4BIT = True` in `config.py`
- Close other applications to free up RAM

### Slow Performance
- Use GPU if available (set `CUDA_AVAILABLE=true`)
- Reduce `MAX_HISTORY_LENGTH` in `config.py`
- Reduce `MAX_NEW_TOKENS` in `config.py`

## Model Information

The default model is **Qwen/Qwen2.5-7B-Instruct**, a high-quality open-source model. You can change the model by editing `MODEL_NAME` in `config.py`.

See [MODEL_OPTIONS.md](MODEL_OPTIONS.md) for a list of recommended models and how to switch between them.

## License

This project uses open-source models from Hugging Face. Please check each model's license on Hugging Face for usage terms.

## Notes

- First run will download the model (can be several GB)
- Model runs locally, so no internet required after initial download
- Response quality depends on the model's capabilities
- For best results, use a GPU with sufficient VRAM
