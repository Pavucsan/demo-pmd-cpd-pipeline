"""Send a GitHub Actions failure email using only Python's standard library."""

import os
from pathlib import Path
import smtplib
import ssl
from email.message import EmailMessage


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Required environment variable {name} is empty")
    return value


def main() -> None:
    host = required("SMTP_HOST")
    port = int(required("SMTP_PORT"))
    username = required("SMTP_USERNAME")
    password = required("SMTP_PASSWORD")
    sender = required("SMTP_FROM")
    recipients = [item.strip() for item in required("SMTP_TO").split(",") if item.strip()]
    security = (os.environ.get("SMTP_SECURITY", "").strip() or "starttls").lower()

    message = EmailMessage()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = required("MAIL_SUBJECT")
    archive = Path(os.environ.get("REPORT_ARCHIVE", "target/quality-reports.zip"))
    attachment_status = (
        f"Attached report archive: {archive.name}"
        if archive.is_file()
        else "Report archive: unavailable for this run"
    )
    message.set_content(f"{required('MAIL_BODY').rstrip()}\n{attachment_status}\n")

    if archive.is_file():
        message.add_attachment(
            archive.read_bytes(),
            maintype="application",
            subtype="zip",
            filename=archive.name,
        )

    context = ssl.create_default_context()
    if security == "ssl":
        with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as smtp:
            smtp.login(username, password)
            smtp.send_message(message)
    elif security == "starttls":
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp.login(username, password)
            smtp.send_message(message)
    else:
        raise ValueError("SMTP_SECURITY must be 'starttls' or 'ssl'")


if __name__ == "__main__":
    main()

