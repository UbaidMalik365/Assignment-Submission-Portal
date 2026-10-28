import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000
OUTPUT_FILE = "test-report.json"


class ReportHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            report = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        with open(OUTPUT_FILE, "w") as f:
            json.dump(report, f, indent=2)

        print("Report received and saved to", OUTPUT_FILE)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Report saved")

    def do_GET(self):
        # Lets you check in a browser that the receiver is running
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Receiver is running")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), ReportHandler)
    print(f"Receiver listening on port {PORT}...")
    server.serve_forever()