# VPS Local Model - Quick Start

Quick guide for deploying with local model on VPS.

## Quick Setup (3 Steps)

### 1. Download Model Locally

```bash
# Activate venv
source venv/bin/activate

# Download model (one time, ~14GB for Qwen2.5-7B)
python download_model.py
```

This saves model to: `./models/Qwen_Qwen2.5-7B-Instruct/`

### 2. Configure Local Path

Edit `config.py`:

```python
LOCAL_MODEL_PATH = "./models/Qwen_Qwen2.5-7B-Instruct"
```

### 3. Run Chatbot

```bash
python main.py
```

That's it! The chatbot will now use the local model.

## Full Example

```bash
# On your VPS
cd ~/chat

# Setup (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download model locally (one time, takes 10-30 minutes)
python download_model.py

# Configure
# Edit config.py: LOCAL_MODEL_PATH = "./models/Qwen_Qwen2.5-7B-Instruct"

# Run
python main.py
```

## Benefits

✅ **Faster**: No download on startup  
✅ **Reliable**: Works offline  
✅ **Consistent**: Same model every time  
✅ **Bandwidth**: Download once, use forever  

## Custom Model Path

```bash
# Download to custom location
python download_model.py --path "/home/user/my-models" --name "qwen-model"

# Then in config.py:
LOCAL_MODEL_PATH = "/home/user/my-models/qwen-model"
```

## Check Model Location

The chatbot will show:
```
Loading model from local path: ./models/Qwen_Qwen2.5-7B-Instruct
```

If you see "Loading model from Hugging Face", the local path isn't set correctly.

## Troubleshooting

**Model not found?**
- Check path exists: `ls -la ./models/Qwen_Qwen2.5-7B-Instruct`
- Verify `config.json` is in the directory
- Use absolute path if relative doesn't work

**Want to switch models?**
- Download new model: `python download_model.py --model "other-model"`
- Update `LOCAL_MODEL_PATH` in `config.py`

See [LOCAL_MODEL_SETUP.md](LOCAL_MODEL_SETUP.md) for detailed guide.
