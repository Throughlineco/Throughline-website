from http.server import BaseHTTPRequestHandler
import json, os, urllib.request, urllib.error

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


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        brand = body.get("brand", "").strip()

        if not brand:
            self._json(400, {"error": "brand required"})
            return

        if not API_KEY:
            self._json(200, {"sentence": f"{brand} has a throughline. Naming it will make your best work impossible to ignore."})
            return

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
            self._json(200, {"sentence": sentence})
        except urllib.error.HTTPError as e:
            print(f"Anthropic error: {e.read().decode()}")
            self._json(500, {"error": "API error"})
        except Exception as e:
            print(f"Error: {e}")
            self._json(500, {"error": str(e)})

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
