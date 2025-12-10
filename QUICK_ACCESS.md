# Quick Access Guide - VPS to Local

## 3 Simple Steps

### 1. On VPS: Start Web Server

```bash
cd ~/chat
source venv/bin/activate
pip install flask flask-cors  # First time only
python web_server.py
```

### 2. Find Your VPS IP

On VPS, run:
```bash
curl ifconfig.me
```

This shows your public IP address.

### 3. On Local Machine: Open Browser

Open browser and go to:
```
http://YOUR_VPS_IP:8000
```

Replace `YOUR_VPS_IP` with the IP from step 2.

## Example

```bash
# Step 1: On VPS
$ python web_server.py
Starting Web Server for Chatbot
Server will be available at:
  - Local: http://localhost:8000
  - Network: http://123.45.67.89:8000

# Step 2: Find IP
$ curl ifconfig.me
123.45.67.89

# Step 3: On your local computer browser
# Go to: http://123.45.67.89:8000
```

## Firewall (If Can't Access)

```bash
# On VPS, allow port 8000
sudo ufw allow 8000/tcp
```

## Troubleshooting

**Can't connect?**
1. Check firewall: `sudo ufw status`
2. Check server is running: `ps aux | grep web_server`
3. Try SSH tunnel: `ssh -L 8000:localhost:8000 user@VPS_IP`

**See [ACCESS_FROM_LOCAL.md](ACCESS_FROM_LOCAL.md) for full guide.**
