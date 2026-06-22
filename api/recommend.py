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
        
        api_key = os.environ.get("GEMINI_API_KEY", "")
        
        payload = json.dumps({
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }).encode()
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read())
            
            # Transform Gemini response to match expected format
            if "candidates" in data and len(data["candidates"]) > 0:
                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                response = {
                    "content": [{"text": text_content}]
                }
            else:
                response = {"error": {"message": "No response from Gemini"}}
            
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        except urllib.error.HTTPError as e:
            err_text = e.read().decode()
            try:
                err = json.loads(err_text)
            except:
                err = {"error": {"message": err_text}}
            self.send_response(e.code)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(err).encode())

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
