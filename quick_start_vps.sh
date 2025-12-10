#!/bin/bash
# Quick start script for VPS deployment

echo "=========================================="
echo "GPT-4o Chatbot - Quick VPS Setup"
echo "=========================================="

# Check for GPU
if command -v nvidia-smi &> /dev/null; then
    echo "✓ NVIDIA GPU detected"
    echo ""
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo ""
    echo "Installing PyTorch with CUDA support..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
else
    echo "⚠ No NVIDIA GPU detected - installing CPU-only PyTorch"
    pip install torch torchvision torchaudio
fi

# Install other dependencies
echo ""
echo "Installing other dependencies..."
pip install -r requirements.txt

# Verify setup
echo ""
echo "Verifying setup..."
python check_gpu.py

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To start the chatbot:"
echo "  python main.py"
echo ""
