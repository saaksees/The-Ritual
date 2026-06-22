from http.server import BaseHTTPRequestHandler
import json, os, urllib.request, urllib.error

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY", "")

def call_groq(prompt):
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
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "User-Agent": "the-ritual-app/1.0"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read())
    return data["choices"][0]["message"]["content"]

def log_to_supabase(answers, parsed):
    try:
        # Extract fields from answers dict and parsed AI response
        record = {
            "skin_type": answers.get("skin_type"),
            "concerns": answers.get("concerns", []),
            "acne_type": answers.get("acne_type", []),
            "lifestyle": answers.get("lifestyle", []),
            "sun_exposure": answers.get("sun_exposure"),
            "actives_experience": answers.get("actives_experience", []),
            "sensitivities": answers.get("sensitivities", []),
            "routine_time": answers.get("routine_time"),
            "budget": answers.get("budget"),
            "skin_diagnosis": parsed.get("skin_diagnosis", ""),
            "recommended_products": parsed.get("routine", [])
        }
        
        payload = json.dumps(record).encode()
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/quiz_responses",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "apikey": SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {SUPABASE_SECRET_KEY}",
                "Prefer": "return=minimal"
            },
            method="POST"
        )
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Supabase logging error: {e}")

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        prompt = body.get('prompt', '')
        answers = body.get('answers', {})
        is_chat = body.get('is_chat', False)
        
        try:
            text = call_groq(prompt)
            
            if is_chat:
                self.send_response(200)
                self._cors()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "content": [{"type": "text", "text": text}]
                }).encode())
                return
            
            clean = text.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(clean)
            
            # Log to Supabase in background
            log_to_supabase(answers, parsed)
            
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
        except Exception as e:
            self.send_response(500)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": {
                    "type": "server_error",
                    "message": str(e)
                }
            }).encode())

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
