"""
Dev server with Claude API proxy.
Usage: ANTHROPIC_API_KEY=sk-... python3 serve_api.py
Serves the site at http://localhost:3000
  POST /api/throughline  — calls Claude to complete a brand throughline sentence
  POST /api/form         — logs form submissions to console (add email later)
"""

import http.server, json, os, socketserver, urllib.request, urllib.error, datetime

SUBMISSIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submissions.json")

PORT = 3000
ROOT = os.path.dirname(os.path.abspath(__file__))
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

SYSTEM_PROMPT = (
    "You complete one sentence in exactly this format: [brand name] has a throughline. "
    "Your completion should be warm, optimistic, and specific. "
    "It should describe what finding and telling their throughline would unlock or amplify for them — "
    "assume they are already doing meaningful work and that the throughline will make it more visible, "
    "more resonant, and more powerful. "
    "Never use negative words like overlooked, struggling, missing, or stuck. "
    "Always frame it as an amplification of something already good, not a fix for something broken. "
    "Under 12 words. End with a full stop. Return only the completed sentence, nothing else."
)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} {fmt % args}")

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/throughline":
            self.handle_throughline()
        elif self.path == "/api/form":
            self.handle_form()
        else:
            self.send_json(404, {"error": "Not found"})

    def handle_throughline(self):
        body = self.read_body()
        brand = body.get("brand", "").strip()
        if not brand:
            return self.send_json(400, {"error": "brand required"})

        if not API_KEY:
            fallback = f"{brand} has a throughline. Naming it will make your best work impossible to ignore."
            return self.send_json(200, {"sentence": fallback})

        payload = {
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 80,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": brand}],
        }
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode(),
            headers={
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read())
            sentence = data["content"][0]["text"].strip()
            self.send_json(200, {"sentence": sentence})
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            print(f"  Anthropic error: {err}")
            self.send_json(500, {"error": "API error"})
        except Exception as e:
            print(f"  Error: {e}")
            self.send_json(500, {"error": str(e)})

    def handle_form(self):
        body = self.read_body()
        body["submitted_at"] = datetime.datetime.now().isoformat()

        # Append to submissions.json
        submissions = []
        if os.path.exists(SUBMISSIONS_FILE):
            try:
                with open(SUBMISSIONS_FILE, "r") as f:
                    submissions = json.load(f)
            except Exception:
                submissions = []
        submissions.append(body)
        with open(SUBMISSIONS_FILE, "w") as f:
            json.dump(submissions, f, indent=2)

        print("\n  ── New form submission saved ──")
        for k, v in body.items():
            print(f"  {k}: {v}")
        print(f"  Total submissions: {len(submissions)}\n")
        self.send_json(200, {"ok": True})


os.chdir(ROOT)
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"\n  Throughline Co. dev server")
    print(f"  http://localhost:{PORT}\n")
    if API_KEY:
        print(f"  Claude API: connected ✓")
    else:
        print(f"  Claude API: set ANTHROPIC_API_KEY to enable live completions")
    print(f"  Press Ctrl+C to stop\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
