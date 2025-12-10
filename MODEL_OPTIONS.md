# Model Options Guide

The original "Xenova/gpt-4o" model name is not valid on Hugging Face. Here are recommended alternatives:

## Recommended Models

### 1. Qwen2.5-7B-Instruct (Default - Currently Configured)
- **Model**: `Qwen/Qwen2.5-7B-Instruct`
- **Size**: ~14GB
- **Quality**: Excellent, very capable
- **VRAM**: ~16GB recommended
- **Best for**: General purpose, high quality responses

### 2. Qwen2.5-3B-Instruct (Smaller, Faster)
- **Model**: `Qwen/Qwen2.5-3B-Instruct`
- **Size**: ~6GB
- **Quality**: Very good
- **VRAM**: ~8GB recommended
- **Best for**: Faster responses, less VRAM

### 3. Mistral-7B-Instruct
- **Model**: `mistralai/Mistral-7B-Instruct-v0.2`
- **Size**: ~14GB
- **Quality**: Excellent
- **VRAM**: ~16GB recommended
- **Best for**: High quality, balanced performance

### 4. Phi-3-mini (Small, Fast)
- **Model**: `microsoft/Phi-3-mini-4k-instruct`
- **Size**: ~7GB
- **Quality**: Good
- **VRAM**: ~8GB recommended
- **Best for**: Quick responses, lower resource usage

### 5. Llama 3.1 8B (Requires Hugging Face Token)
- **Model**: `meta-llama/Llama-3.1-8B-Instruct`
- **Size**: ~16GB
- **Quality**: Excellent
- **VRAM**: ~20GB recommended
- **Note**: Requires Hugging Face account and token
- **Best for**: Maximum quality (if you have access)

## How to Change the Model

Edit `config.py` and change the `MODEL_NAME` variable:

```python
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"  # Change this line
```

## For Smaller GPUs (8GB VRAM or less)

If you have limited VRAM, use a smaller model or enable quantization:

**Option 1: Use smaller model**
```python
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
# or
MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
```

**Option 2: Enable 8-bit quantization**
```python
LOAD_IN_8BIT = True
LOAD_IN_4BIT = False
```

**Option 3: Enable 4-bit quantization (most memory efficient)**
```python
LOAD_IN_8BIT = False
LOAD_IN_4BIT = True
```

Note: For quantization, install `bitsandbytes`:
```bash
pip install bitsandbytes
```

## Finding More Models

Visit [Hugging Face Models](https://huggingface.co/models) and search for:
- "instruct" models (for chat/conversation)
- Filter by task: "Text Generation"
- Check model size and requirements

## Model Comparison

| Model | Size | VRAM (FP16) | VRAM (8-bit) | Quality | Speed |
|-------|------|-------------|--------------|---------|-------|
| Qwen2.5-7B | 14GB | ~16GB | ~8GB | ⭐⭐⭐⭐⭐ | Medium |
| Qwen2.5-3B | 6GB | ~8GB | ~4GB | ⭐⭐⭐⭐ | Fast |
| Mistral-7B | 14GB | ~16GB | ~8GB | ⭐⭐⭐⭐⭐ | Medium |
| Phi-3-mini | 7GB | ~8GB | ~4GB | ⭐⭐⭐⭐ | Fast |
| Llama-3.1-8B | 16GB | ~20GB | ~10GB | ⭐⭐⭐⭐⭐ | Medium |

## Your Current Setup

You have an **NVIDIA RTX 4000 SFF Ada Generation** with CUDA 11.8.

Recommended for your GPU:
- **Qwen2.5-7B-Instruct** (if you have 16GB+ VRAM)
- **Qwen2.5-3B-Instruct** (if you have 8-16GB VRAM)
- **Mistral-7B-Instruct** (alternative to Qwen2.5-7B)

Check your GPU VRAM:
```bash
nvidia-smi
```

Look for the "Memory" line to see total and available VRAM.
