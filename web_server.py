"""
Web server for the chatbot - Access from your local machine
"""
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from chatbot import ChatBot
import threading
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for API access

# Global chatbot instance (loaded once)
chatbot = None
chatbot_lock = threading.Lock()

def init_chatbot():
    """Initialize chatbot in a separate thread"""
    global chatbot
    print("Initializing chatbot...")
    chatbot = ChatBot()
    print("Chatbot ready!")

# Initialize chatbot in background
init_thread = threading.Thread(target=init_chatbot, daemon=True)
init_thread.start()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPT-4o Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 900px;
            height: 90vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }
        .header p {
            opacity: 0.9;
            font-size: 14px;
        }
        .chat-area {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
            animation: fadeIn 0.3s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user {
            justify-content: flex-end;
        }
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        .message.user .message-content {
            background: #667eea;
            color: white;
            border-bottom-right-radius: 4px;
        }
        .message.assistant .message-content {
            background: white;
            color: #333;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .message-label {
            font-size: 11px;
            opacity: 0.7;
            margin-bottom: 5px;
            padding: 0 5px;
        }
        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        #messageInput {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }
        #messageInput:focus {
            border-color: #667eea;
        }
        #sendButton {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        #sendButton:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        #sendButton:active {
            transform: translateY(0);
        }
        #sendButton:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .status {
            text-align: center;
            padding: 10px;
            font-size: 12px;
            color: #666;
        }
        .status.loading {
            color: #667eea;
        }
        .clear-btn {
            background: #f44336;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 15px;
            cursor: pointer;
            font-size: 12px;
            margin-left: 10px;
        }
        .clear-btn:hover {
            background: #d32f2f;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 GPT-4o Chatbot</h1>
            <p>Running on VPS - Access from anywhere</p>
        </div>
        <div id="status" class="status loading">Initializing chatbot...</div>
        <div class="chat-area" id="chatArea"></div>
        <div class="input-area">
            <div class="input-container">
                <input 
                    type="text" 
                    id="messageInput" 
                    placeholder="Type your message..." 
                    disabled
                    onkeypress="if(event.key === 'Enter') sendMessage()"
                >
                <button id="sendButton" onclick="sendMessage()" disabled>Send</button>
                <button class="clear-btn" onclick="clearChat()">Clear</button>
            </div>
        </div>
    </div>

    <script>
        let isReady = false;

        // Check if chatbot is ready
        function checkReady() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    if (data.ready) {
                        isReady = true;
                        document.getElementById('status').textContent = 'Chatbot ready!';
                        document.getElementById('status').classList.remove('loading');
                        document.getElementById('messageInput').disabled = false;
                        document.getElementById('sendButton').disabled = false;
                        document.getElementById('messageInput').focus();
                    } else {
                        setTimeout(checkReady, 2000);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    setTimeout(checkReady, 2000);
                });
        }

        // Send message
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message || !isReady) return;

            // Add user message to chat
            addMessage('user', message);
            input.value = '';
            input.disabled = true;
            document.getElementById('sendButton').disabled = true;
            document.getElementById('sendButton').innerHTML = '<div class="loading"></div>';

            // Send to API
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    addMessage('assistant', 'Error: ' + data.error);
                } else {
                    addMessage('assistant', data.response);
                }
                input.disabled = false;
                document.getElementById('sendButton').disabled = false;
                document.getElementById('sendButton').textContent = 'Send';
                input.focus();
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('assistant', 'Error: Failed to get response');
                input.disabled = false;
                document.getElementById('sendButton').disabled = false;
                document.getElementById('sendButton').textContent = 'Send';
            });
        }

        // Add message to chat area
        function addMessage(role, content) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            
            const label = document.createElement('div');
            label.className = 'message-label';
            label.textContent = role === 'user' ? 'You' : 'Assistant';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(label);
            messageDiv.appendChild(contentDiv);
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        // Clear chat
        function clearChat() {
            if (!confirm('Clear conversation history?')) return;
            
            fetch('/api/clear', { method: 'POST' })
                .then(() => {
                    document.getElementById('chatArea').innerHTML = '';
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }

        // Check ready status on load
        checkReady();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    """Check if chatbot is ready"""
    return jsonify({
        'ready': chatbot is not None
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    if chatbot is None:
        return jsonify({'error': 'Chatbot is still initializing. Please wait...'}), 503
    
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        with chatbot_lock:
            response = chatbot.chat(message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear():
    """Clear conversation history"""
    if chatbot is None:
        return jsonify({'error': 'Chatbot is not ready'}), 503
    
    try:
        with chatbot_lock:
            chatbot.clear_history()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def history():
    """Get conversation history"""
    if chatbot is None:
        return jsonify({'error': 'Chatbot is not ready'}), 503
    
    try:
        with chatbot_lock:
            history = chatbot.get_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Web server for chatbot')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to (default: 0.0.0.0 for all interfaces)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Starting Web Server for Chatbot")
    print("=" * 60)
    print(f"Server will be available at:")
    print(f"  - Local: http://localhost:{args.port}")
    print(f"  - Network: http://<VPS_IP>:{args.port}")
    print(f"  - From your local machine: http://<VPS_IP>:{args.port}")
    print("=" * 60)
    print("\nWaiting for chatbot to initialize...")
    print("(This may take a few minutes on first run)\n")
    
    app.run(host=args.host, port=args.port, debug=args.debug, threaded=True)
