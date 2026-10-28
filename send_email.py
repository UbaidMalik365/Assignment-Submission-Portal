import json
import os
import smtplib
from email.message import EmailMessage

REPORT_FILE = "report-for-email.json"


def main():
    # Rebuild the same report from the real pytest results
    from send_report import build_report
    report = build_report()

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    s = report["summary"]
    lines = [
        f"Repository : {report['repository']}",
        f"Branch     : {report['branch']}",
        f"Commit     : {report['commit_sha']}",
        f"Run ID     : {report['run_id']}",
        f"Time (UTC) : {report['timestamp']}",
        "",
        f"Overall status: {s['status'].upper()}",
        f"Total: {s['total']}   Passed: {s['passed']}   Failed: {s['failed']}",
        "",
        "Individual results:",
    ]
    for t in report["tests"]:
        lines.append(f"  [{t['result'].upper()}] {t['name']}")
        if t["failure_message"]:
            lines.append(f"      {t['failure_message']}")

    msg = EmailMessage()
    msg["Subject"] = f"[{s['status'].upper()}] CI report - {report['repository']} @ {report['commit_sha'][:7]}"
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]
    msg.set_content("\n".join(lines))

    with open(REPORT_FILE, "rb") as f:
        msg.add_attachment(f.read(), maintype="application",
                           subtype="json", filename="test-report.json")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["EMAIL_USERNAME"], os.environ["EMAIL_PASSWORD"])
        server.send_message(msg)
    print("Email sent to", msg["To"])


if __name__ == "__main__":
    main()