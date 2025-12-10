"""
Configuration file for the chatbot
"""
import os
import torch

# Model configuration
# Note: "Xenova/gpt-4o" is not a valid model. Using a high-quality alternative.
# You can change this to any valid Hugging Face model name.
# Popular options:
#   - "Qwen/Qwen2.5-7B-Instruct" (recommended, high quality)
#   - "mistralai/Mistral-7B-Instruct-v0.2"
#   - "meta-llama/Llama-3.1-8B-Instruct" (requires Hugging Face token)
#   - "microsoft/Phi-3-mini-4k-instruct" (smaller, faster)
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

# Local model path (for VPS deployment)
# If set, the model will be loaded from this local path instead of downloading from Hugging Face
# Set to None or empty string to use Hugging Face model hub
# Example: LOCAL_MODEL_PATH = "/home/user/models/Qwen2.5-7B-Instruct"
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", None)  # Set via environment or change here

# Auto-detect GPU: Use CUDA if available, otherwise CPU
# You can override by setting FORCE_DEVICE environment variable: "cuda" or "cpu"
FORCE_DEVICE = os.getenv("FORCE_DEVICE", "").lower()
if FORCE_DEVICE in ["cuda", "cpu"]:
    DEVICE = FORCE_DEVICE
elif torch.cuda.is_available():
    DEVICE = "cuda"
    print(f"GPU detected: {torch.cuda.get_device_name(0)}")
    print(f"CUDA version: {torch.version.cuda}")
else:
    DEVICE = "cpu"
    print("No GPU detected, using CPU")

MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7
TOP_P = 0.9
DO_SAMPLE = True

# Chat configuration
SYSTEM_PROMPT = "You are a helpful, harmless, and honest assistant."
MAX_HISTORY_LENGTH = 10  # Number of previous messages to keep in context

# Model loading configuration
LOAD_IN_8BIT = False
LOAD_IN_4BIT = False
TRUST_REMOTE_CODE = True
