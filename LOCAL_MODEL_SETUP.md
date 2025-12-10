# Local Model Setup for VPS

This guide explains how to download and use models locally on your VPS, avoiding repeated downloads.

## Why Use Local Models?

- **Faster startup**: No need to download on each deployment
- **Offline capability**: Works without internet after initial download
- **Version control**: Use specific model versions
- **Bandwidth savings**: Download once, use many times

## Step 1: Download the Model

### Option A: Using the Download Script (Recommended)

```bash
# Activate virtual environment
source venv/bin/activate

# Download the default model (Qwen2.5-7B-Instruct)
python download_model.py

# Or specify a custom model and path
python download_model.py --model "Qwen/Qwen2.5-7B-Instruct" --path "/home/user/models"

# Or use a custom directory name
python download_model.py --model "Qwen/Qwen2.5-7B-Instruct" --path "/home/user/models" --name "my-model"
```

The model will be saved to `./models/Qwen_Qwen2.5-7B-Instruct/` by default.

### Option B: Manual Download

You can also download models manually using Python:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "Qwen/Qwen2.5-7B-Instruct"
local_path = "./models/Qwen2.5-7B-Instruct"

# Download and save
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(local_path)

model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained(local_path)
```

## Step 2: Configure the Chatbot to Use Local Model

### Method 1: Edit config.py (Recommended)

Edit `config.py` and set `LOCAL_MODEL_PATH`:

```python
LOCAL_MODEL_PATH = "/home/user/chat/models/Qwen_Qwen2.5-7B-Instruct"
```

Or use a relative path:

```python
LOCAL_MODEL_PATH = "./models/Qwen_Qwen2.5-7B-Instruct"
```

### Method 2: Use Environment Variable

Set the environment variable before running:

```bash
export LOCAL_MODEL_PATH="/home/user/chat/models/Qwen_Qwen2.5-7B-Instruct"
python main.py
```

Or add to your `.bashrc` or service file:

```bash
# In ~/.bashrc
export LOCAL_MODEL_PATH="/home/user/chat/models/Qwen_Qwen2.5-7B-Instruct"
```

## Step 3: Verify Local Model

Check that the model files exist:

```bash
ls -lh /path/to/your/model/
```

You should see files like:
- `config.json`
- `tokenizer.json`
- `model-*.safetensors` or `pytorch_model.bin`
- Other model files

## Step 4: Run the Chatbot

Now run the chatbot - it will use the local model:

```bash
source venv/bin/activate
python main.py
```

You should see:
```
Loading model from local path: /path/to/your/model
Loading tokenizer...
Loading model from local storage...
```

## Complete VPS Deployment Example

```bash
# 1. Clone/download project
cd ~/chat

# 2. Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download model locally (one time)
python download_model.py --model "Qwen/Qwen2.5-7B-Instruct" --path "./models"

# 5. Configure local model path
# Edit config.py and set:
# LOCAL_MODEL_PATH = "./models/Qwen_Qwen2.5-7B-Instruct"

# 6. Run chatbot
python main.py
```

## Model Storage Locations

### Recommended Structure

```
~/chat/
├── main.py
├── chatbot.py
├── config.py
├── models/                    # Local models directory
│   └── Qwen_Qwen2.5-7B-Instruct/
│       ├── config.json
│       ├── tokenizer.json
│       └── model files...
└── venv/
```

### Alternative: Centralized Model Storage

Store all models in a central location:

```bash
# Create central models directory
mkdir -p ~/models

# Download to central location
python download_model.py --model "Qwen/Qwen2.5-7B-Instruct" --path "~/models"

# Use in config.py
LOCAL_MODEL_PATH = "~/models/Qwen_Qwen2.5-7B-Instruct"
```

## Disk Space Requirements

Model sizes (approximate):
- **Qwen2.5-7B-Instruct**: ~14GB
- **Qwen2.5-3B-Instruct**: ~6GB
- **Mistral-7B-Instruct**: ~14GB
- **Phi-3-mini**: ~7GB

Ensure you have enough disk space:

```bash
df -h  # Check available disk space
```

## Updating Local Models

To update a local model:

```bash
# Delete old model
rm -rf ./models/Qwen_Qwen2.5-7B-Instruct

# Download fresh copy
python download_model.py
```

Or download to a new location and update `LOCAL_MODEL_PATH`.

## Using Multiple Models

You can switch between models by changing `LOCAL_MODEL_PATH`:

```python
# In config.py, switch models:
LOCAL_MODEL_PATH = "./models/Qwen_Qwen2.5-7B-Instruct"  # Use Qwen
# LOCAL_MODEL_PATH = "./models/Mistral-7B-Instruct"     # Switch to Mistral
```

## Troubleshooting

### Model Not Found Error

If you get "model path not found":
1. Check the path is correct: `ls -la /path/to/model`
2. Verify `config.json` exists in the directory
3. Check file permissions: `chmod -R 755 /path/to/model`

### Permission Denied

```bash
# Fix permissions
chmod -R 755 /path/to/model
```

### Disk Space Issues

```bash
# Check disk usage
du -sh ./models/*

# Clean up old models
rm -rf ./models/old-model-name
```

### Model Verification Failed

If model verification fails during download but files are present:
- This is often due to memory constraints during verification
- The model files are likely fine
- Try loading the model in the chatbot - it should work

## Integration with systemd Service

If using systemd service, update `chatbot.service`:

```ini
[Service]
Environment="LOCAL_MODEL_PATH=/home/user/chat/models/Qwen_Qwen2.5-7B-Instruct"
```

Or set it in `config.py` directly.

## Benefits for VPS Deployment

1. **Faster restarts**: No download time
2. **Reliability**: Works even if Hugging Face is down
3. **Consistency**: Same model version every time
4. **Bandwidth**: Save bandwidth on VPS
5. **Offline**: Can work completely offline after setup
