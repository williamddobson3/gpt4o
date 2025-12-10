"""
Configuration file for the chatbot
"""
import os
import torch

# Model configuration
MODEL_NAME = "Xenova/gpt-4o"

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
