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
        
        api_key = os.environ.get("GROQ_API_KEY", "")
        
        payload = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.7
        }).encode()
        
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "Mozilla/5.0"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read())
            
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
                    "type": "groq_error",
                    "message": err.decode()
                }
            }).encode())

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
