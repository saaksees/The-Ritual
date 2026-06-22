from http.server import BaseHTTPRequestHandler
import json, os, urllib.request, urllib.error

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        prompt = body.get('prompt', '')
        
        api_key = os.environ.get("XAI_API_KEY", "")
        
        url = "https://api.x.ai/v1/chat/completions"
        
        payload = json.dumps({
            "model": "grok-beta",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }).encode()
        
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read())
            
            # Extract text from Grok response (OpenAI-compatible format)
            text = data["choices"][0]["message"]["content"]
            
            # Return in same shape as Anthropic so frontend works unchanged
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "content": [{"type": "text", "text": text}]
            }).encode())
        except urllib.error.HTTPError as e:
            err = e.read()
            self.send_response(e.code)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": {
                    "type": "grok_error",
                    "message": err.decode()
                }
            }).encode())

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
