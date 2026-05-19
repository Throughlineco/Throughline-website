from http.server import BaseHTTPRequestHandler
import json, datetime, os, urllib.request, urllib.error

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
TO_EMAIL = "riya.miital18@gmail.com"
FROM_EMAIL = "Throughline Co <onboarding@resend.dev>"


def send_email(body):
    if not RESEND_API_KEY:
        return

    name    = body.get("name", "—")
    org     = body.get("org", "—")
    story   = body.get("story", "—")
    org_type = body.get("org_type", "—")
    source  = body.get("source", "—")
    submitted_at = body.get("submitted_at", "—")

    html = f"""
    <h2 style="color:#2C3E35;font-family:Georgia,serif;">New Throughline Inquiry</h2>
    <table style="font-family:Arial,sans-serif;font-size:14px;border-collapse:collapse;width:100%">
      <tr><td style="padding:8px 0;color:#888;width:160px">Name</td><td style="padding:8px 0"><strong>{name}</strong></td></tr>
      <tr><td style="padding:8px 0;color:#888">Organisation</td><td style="padding:8px 0"><strong>{org}</strong></td></tr>
      <tr><td style="padding:8px 0;color:#888">Type</td><td style="padding:8px 0">{org_type}</td></tr>
      <tr><td style="padding:8px 0;color:#888">Story</td><td style="padding:8px 0">{story}</td></tr>
      <tr><td style="padding:8px 0;color:#888">Found us via</td><td style="padding:8px 0">{source}</td></tr>
      <tr><td style="padding:8px 0;color:#888">Submitted</td><td style="padding:8px 0">{submitted_at}</td></tr>
    </table>
    """

    payload = json.dumps({
        "from": FROM_EMAIL,
        "to": [TO_EMAIL],
        "subject": f"New inquiry from {name} — {org}",
        "html": html,
    }).encode()

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        print("Email sent successfully")
    except urllib.error.HTTPError as e:
        print(f"Resend error: {e.read().decode()}")
    except Exception as e:
        print(f"Email error: {e}")


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
        body["submitted_at"] = datetime.datetime.now().isoformat()
        print("New form submission:", json.dumps(body, indent=2))
        send_email(body)
        self._json(200, {"ok": True})

    def _json(self, code, data):
        b = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(b))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b)
