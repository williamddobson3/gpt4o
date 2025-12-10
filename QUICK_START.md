# Quick Start Guide - How to Run the Chatbot

## Step-by-Step Instructions

### 1. First Time Setup

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### On Linux/Mac/VPS:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# For GPU (if you have NVIDIA GPU):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt

# For CPU only:
pip install -r requirements.txt
```

### 2. Run the Chatbot

Simply run:
```bash
python main.py
```

Or on Linux/Mac:
```bash
python3 main.py
```

### 3. First Run

On the first run, the model will be downloaded automatically. This may take several minutes depending on your internet connection. The model will be cached for future use.

### 4. Using the Chatbot

Once loaded, you'll see:
```
============================================================
  GPT-4o Chatbot (Xenova/gpt-4o)
============================================================

Commands:
  - Type your message and press Enter to chat
  - Type '/clear' to clear conversation history
  - Type '/history' to view conversation history
  - Type '/exit' or '/quit' to exit
  - Type '/help' to show this help message

============================================================

Chatbot is ready! Start chatting...
```

### 5. Example Usage

```
You: Hello! What can you do?
Assistant: [Response from the model]

You: /history
[Shows conversation history]

You: /clear
Conversation history cleared.

You: /exit
Goodbye!
```

## Troubleshooting

### If you get "Module not found" error:
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

### If GPU is not detected:
- Check GPU: `python check_gpu.py`
- Verify NVIDIA drivers: `nvidia-smi` (Linux)
- Install CUDA-enabled PyTorch if needed

### If model download fails:
- Check internet connection
- Check disk space
- Try again later (Hugging Face servers may be busy)

## VPS Deployment

For VPS with GPU, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

Quick VPS setup:
```bash
chmod +x deploy.sh
./deploy.sh
```

Then run:
```bash
source venv/bin/activate
python main.py
```
