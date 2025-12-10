# Access VPS Chatbot from Local Machine

This guide explains how to access your chatbot running on VPS from your local computer.

## Quick Start

### Step 1: Start Web Server on VPS

```bash
# On your VPS
cd ~/chat
source venv/bin/activate

# Start web server
python web_server.py
```

The server will start on port 8000 by default.

### Step 2: Access from Local Machine

Open your browser and go to:
```
http://YOUR_VPS_IP:8000
```

Replace `YOUR_VPS_IP` with your VPS's IP address.

## Finding Your VPS IP Address

### On VPS (check public IP):
```bash
# Method 1: Using curl
curl ifconfig.me

# Method 2: Using hostname
hostname -I

# Method 3: Check network interfaces
ip addr show
```

### Common IP Types:
- **Public IP**: Accessible from internet (e.g., `123.45.67.89`)
- **Private IP**: Only accessible within same network (e.g., `192.168.1.100`)

## Configuration Options

### Change Port

```bash
# Use custom port (e.g., 5000)
python web_server.py --port 5000
```

### Bind to Specific Interface

```bash
# Only allow localhost (more secure)
python web_server.py --host 127.0.0.1

# Allow all interfaces (default, for remote access)
python web_server.py --host 0.0.0.0
```

## Firewall Configuration

### Allow Port in Firewall

**Ubuntu/Debian (ufw):**
```bash
# Allow port 8000
sudo ufw allow 8000/tcp

# Check status
sudo ufw status
```

**CentOS/RHEL (firewalld):**
```bash
# Allow port 8000
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

**Check if port is open:**
```bash
# From your local machine
telnet YOUR_VPS_IP 8000
# or
nc -zv YOUR_VPS_IP 8000
```

## Running as a Service

### Create systemd Service for Web Server

Create `/etc/systemd/system/chatbot-web.service`:

```ini
[Unit]
Description=Chatbot Web Server
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/chat
Environment="PATH=/home/YOUR_USERNAME/chat/venv/bin"
Environment="LOCAL_MODEL_PATH=/home/YOUR_USERNAME/chat/models/Qwen_Qwen2.5-7B-Instruct"
ExecStart=/home/YOUR_USERNAME/chat/venv/bin/python /home/YOUR_USERNAME/chat/web_server.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable chatbot-web.service
sudo systemctl start chatbot-web.service

# Check status
sudo systemctl status chatbot-web.service

# View logs
sudo journalctl -u chatbot-web.service -f
```

## Security Considerations

### 1. Use HTTPS (Recommended for Production)

For production, use a reverse proxy with SSL:

**Install Nginx:**
```bash
sudo apt-get install nginx certbot python3-certbot-nginx
```

**Configure Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Get SSL Certificate:**
```bash
sudo certbot --nginx -d your-domain.com
```

### 2. Add Authentication (Optional)

For basic authentication, you can add a simple password check:

```python
# Add to web_server.py
from functools import wraps
from flask import request

def check_auth(username, password):
    return username == 'admin' and password == 'your-password'

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response('Login required', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated

@app.route('/api/chat', methods=['POST'])
@requires_auth
def chat():
    # ... existing code
```

### 3. Restrict Access by IP

In `web_server.py`, you can add IP filtering:

```python
from flask import request, abort

ALLOWED_IPS = ['YOUR_LOCAL_IP', '192.168.1.0/24']  # Add your IPs

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
```

## Access Methods

### Method 1: Direct Browser Access

Simply open browser and go to:
```
http://YOUR_VPS_IP:8000
```

### Method 2: SSH Tunnel (More Secure)

If you don't want to expose the port publicly:

**On your local machine:**
```bash
ssh -L 8000:localhost:8000 user@YOUR_VPS_IP
```

Then access: `http://localhost:8000`

### Method 3: API Access

You can also use the API directly:

```bash
# Send a message
curl -X POST http://YOUR_VPS_IP:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Check status
curl http://YOUR_VPS_IP:8000/api/status

# Clear history
curl -X POST http://YOUR_VPS_IP:8000/api/clear
```

## Troubleshooting

### Can't Access from Local Machine

1. **Check firewall:**
   ```bash
   sudo ufw status
   ```

2. **Check if server is running:**
   ```bash
   # On VPS
   netstat -tulpn | grep 8000
   # or
   ss -tulpn | grep 8000
   ```

3. **Check server logs:**
   ```bash
   # If running as service
   sudo journalctl -u chatbot-web.service -f
   ```

4. **Test from VPS itself:**
   ```bash
   curl http://localhost:8000
   ```

5. **Check VPS provider firewall:**
   - Some VPS providers have additional firewalls
   - Check your VPS control panel for firewall settings

### Connection Refused

- Server might not be running
- Wrong port number
- Firewall blocking the port
- Server bound to 127.0.0.1 instead of 0.0.0.0

### Slow Response

- Model is still loading (first time takes several minutes)
- GPU not being used
- Network latency

### Port Already in Use

```bash
# Find what's using the port
sudo lsof -i :8000
# or
sudo netstat -tulpn | grep 8000

# Kill the process or use different port
python web_server.py --port 8001
```

## Example: Complete Setup

```bash
# On VPS
cd ~/chat
source venv/bin/activate

# Install web dependencies
pip install flask flask-cors

# Configure firewall
sudo ufw allow 8000/tcp

# Start web server
python web_server.py --host 0.0.0.0 --port 8000

# On local machine, open browser:
# http://YOUR_VPS_IP:8000
```

## API Endpoints

- `GET /` - Web interface
- `GET /api/status` - Check if chatbot is ready
- `POST /api/chat` - Send message, get response
- `POST /api/clear` - Clear conversation history
- `GET /api/history` - Get conversation history

## Next Steps

- Set up as systemd service for auto-start
- Configure HTTPS with Nginx
- Add authentication if needed
- Set up monitoring and logging
