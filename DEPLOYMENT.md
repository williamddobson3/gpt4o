# VPS Deployment Guide

This guide will help you deploy the GPT-4o chatbot on your VPS with GPU support.

## Prerequisites

- VPS with Ubuntu/Debian Linux
- NVIDIA GPU with CUDA support
- SSH access to your VPS
- At least 16GB RAM (32GB+ recommended)
- At least 50GB free disk space for the model

## Step 1: Initial VPS Setup

### 1.1 Connect to your VPS
```bash
ssh username@your-vps-ip
```

### 1.2 Update system packages
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 1.3 Install NVIDIA drivers (if not already installed)

Check if NVIDIA drivers are installed:
```bash
nvidia-smi
```

If not installed, install them:
```bash
# Add NVIDIA repository
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update

# Install NVIDIA drivers (adjust version as needed)
sudo apt-get install -y nvidia-driver-535

# Reboot
sudo reboot
```

After reboot, verify:
```bash
nvidia-smi
```

### 1.4 Install CUDA Toolkit (if needed)

```bash
# Check CUDA version required by PyTorch
# For PyTorch 2.0+, CUDA 11.8 or 12.1 is recommended

# Install CUDA 11.8 (example)
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run
```

## Step 2: Deploy the Chatbot

### 2.1 Clone or upload the project

If using git:
```bash
git clone <your-repo-url>
cd chat
```

Or upload files via SCP:
```bash
# From your local machine
scp -r /path/to/chat username@your-vps-ip:/home/username/
```

### 2.2 Run deployment script

**Option 1: Quick start (if virtual environment is already set up)**
```bash
chmod +x quick_start_vps.sh
source venv/bin/activate
./quick_start_vps.sh
```

**Option 2: Full deployment script**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Option 3: Manual setup**

```bash
# Install Python dependencies
sudo apt-get install -y python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
pip install -r requirements.txt
```

### 2.3 Verify GPU setup

```bash
source venv/bin/activate
python check_gpu.py
```

You should see your GPU information. If not, check:
- NVIDIA drivers: `nvidia-smi`
- CUDA installation: `nvcc --version`
- PyTorch CUDA: `python -c "import torch; print(torch.cuda.is_available())"`

## Step 3: Configure the Chatbot

### 3.1 Edit configuration

Edit `config.py` to optimize for your GPU:

```python
# For large GPUs (24GB+ VRAM)
MAX_NEW_TOKENS = 1024
LOAD_IN_8BIT = False
LOAD_IN_4BIT = False

# For smaller GPUs (8-16GB VRAM)
MAX_NEW_TOKENS = 512
LOAD_IN_8BIT = True  # Enable 8-bit quantization
LOAD_IN_4BIT = False

# For very small GPUs (<8GB VRAM)
MAX_NEW_TOKENS = 256
LOAD_IN_8BIT = False
LOAD_IN_4BIT = True  # Enable 4-bit quantization
```

### 3.2 Test the chatbot

```bash
source venv/bin/activate
python main.py
```

## Step 4: Run as a Service (Optional)

### 4.1 Create systemd service

Edit `chatbot.service` and replace:
- `YOUR_USERNAME` with your VPS username
- `/home/YOUR_USERNAME/path/to/chatbot` with your actual project path

Example:
```ini
[Unit]
Description=GPT-4o Chatbot Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/chat
Environment="PATH=/home/ubuntu/chat/venv/bin"
ExecStart=/home/ubuntu/chat/venv/bin/python /home/ubuntu/chat/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 4.2 Install and start service

```bash
# Copy service file
sudo cp chatbot.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable chatbot.service

# Start service
sudo systemctl start chatbot.service

# Check status
sudo systemctl status chatbot.service

# View logs
sudo journalctl -u chatbot.service -f
```

### 4.3 Service management commands

```bash
# Start
sudo systemctl start chatbot.service

# Stop
sudo systemctl stop chatbot.service

# Restart
sudo systemctl restart chatbot.service

# View logs
sudo journalctl -u chatbot.service -n 50

# Follow logs
sudo journalctl -u chatbot.service -f
```

## Step 5: Using Screen/Tmux (Alternative to systemd)

If you prefer not to use systemd:

### Using Screen:
```bash
screen -S chatbot
source venv/bin/activate
python main.py
# Press Ctrl+A then D to detach
# Reattach with: screen -r chatbot
```

### Using Tmux:
```bash
tmux new -s chatbot
source venv/bin/activate
python main.py
# Press Ctrl+B then D to detach
# Reattach with: tmux attach -t chatbot
```

## Step 6: Firewall Configuration (if needed)

If you want to access the chatbot remotely (requires web interface):

```bash
# Allow SSH (if not already allowed)
sudo ufw allow 22/tcp

# If using web interface on port 8000
sudo ufw allow 8000/tcp

# Enable firewall
sudo ufw enable
```

## Troubleshooting

### GPU not detected

1. Check NVIDIA drivers:
   ```bash
   nvidia-smi
   ```

2. Check PyTorch CUDA:
   ```bash
   python -c "import torch; print(torch.cuda.is_available())"
   ```

3. Reinstall PyTorch with CUDA:
   ```bash
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Out of Memory (OOM) errors

1. Reduce `MAX_NEW_TOKENS` in `config.py`
2. Enable quantization (`LOAD_IN_8BIT = True` or `LOAD_IN_4BIT = True`)
3. Reduce `MAX_HISTORY_LENGTH` in `config.py`
4. Check GPU memory: `nvidia-smi`

### Model download issues

1. Check internet connection
2. Check disk space: `df -h`
3. Clear Hugging Face cache if needed:
   ```bash
   rm -rf ~/.cache/huggingface/
   ```

### Service won't start

1. Check service status: `sudo systemctl status chatbot.service`
2. Check logs: `sudo journalctl -u chatbot.service -n 100`
3. Verify paths in service file are correct
4. Check file permissions

## Performance Optimization

### For best performance:

1. **Use GPU**: Ensure `DEVICE = "cuda"` in `config.py`
2. **Optimize batch size**: Adjust `MAX_NEW_TOKENS` based on your GPU memory
3. **Use mixed precision**: Already enabled with `torch.float16`
4. **Monitor GPU usage**: `watch -n 1 nvidia-smi`

### Memory optimization:

- Enable 8-bit quantization for GPUs with 8-16GB VRAM
- Enable 4-bit quantization for GPUs with <8GB VRAM
- Reduce `MAX_HISTORY_LENGTH` to save memory

## Monitoring

### Check GPU usage:
```bash
watch -n 1 nvidia-smi
```

### Check system resources:
```bash
htop
```

### Check disk space:
```bash
df -h
```

## Security Notes

- Keep your system updated: `sudo apt-get update && sudo apt-get upgrade`
- Use strong SSH keys
- Don't run as root
- Keep Python packages updated: `pip list --outdated`
- Consider using a firewall (ufw)

## Next Steps

- Consider adding a web interface (Flask/FastAPI) for remote access
- Set up log rotation
- Configure automatic backups
- Set up monitoring/alerting
