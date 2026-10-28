import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

RAW_FILE = "pytest-raw.json"
RECEIVER_URL = os.environ.get("RECEIVER_URL", "http://localhost:8000")


def build_report():
    with open(RAW_FILE) as f:
        raw = json.load(f)

    tests = []
    for t in raw.get("tests", []):
        failure = None
        if t["outcome"] == "failed":
            call = t.get("call", {})
            failure = (call.get("crash", {}) or {}).get("message") or call.get("longrepr")
        tests.append({
            "name": t["nodeid"],
            "result": t["outcome"],
            "failure_message": failure,
        })

    passed = sum(1 for t in tests if t["result"] == "passed")
    failed = sum(1 for t in tests if t["result"] == "failed")

    return {
        "repository": os.environ.get("GITHUB_REPOSITORY", "local"),
        "branch": os.environ.get("GITHUB_REF_NAME", "local"),
        "commit_sha": os.environ.get("GITHUB_SHA", "local"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(tests),
            "passed": passed,
            "failed": failed,
            "status": "passed" if failed == 0 and len(tests) > 0 else "failed",
        },
        "tests": tests,
    }


def main():
    report = build_report()
    data = json.dumps(report).encode("utf-8")
    req = urllib.request.Request(
        RECEIVER_URL, data=data,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        print("Receiver replied:", resp.status, resp.read().decode())
    print("Overall status:", report["summary"]["status"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Failed to send report:", e)
        sys.exit(1)