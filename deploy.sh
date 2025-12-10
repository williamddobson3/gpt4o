#!/bin/bash
# Deployment script for VPS

set -e

echo "=========================================="
echo "GPT-4o Chatbot VPS Deployment Script"
echo "=========================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo "Please do not run as root. Use a regular user with sudo privileges."
   exit 1
fi

# Update system packages
echo -e "\n[1/6] Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip if not present
echo -e "\n[2/6] Installing Python and dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv git

# Check for NVIDIA GPU
echo -e "\n[3/6] Checking for NVIDIA GPU..."
if command -v nvidia-smi &> /dev/null; then
    echo "✓ NVIDIA GPU detected"
    nvidia-smi
    echo -e "\nInstalling CUDA-enabled PyTorch..."
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
else
    echo "⚠ No NVIDIA GPU detected. Installing CPU-only PyTorch..."
fi

# Create virtual environment
echo -e "\n[4/6] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install Python dependencies
echo -e "\n[5/6] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Verify GPU setup
echo -e "\n[6/6] Verifying GPU setup..."
python check_gpu.py

echo -e "\n=========================================="
echo "Deployment complete!"
echo "=========================================="
echo -e "\nTo run the chatbot:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo -e "\nTo check GPU status:"
echo "  python check_gpu.py"
echo -e "\nTo set up as a service, see DEPLOYMENT.md"
