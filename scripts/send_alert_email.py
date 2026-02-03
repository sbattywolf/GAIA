"""Send an email alert via SMTP using environment-provided credentials.
Usage (PowerShell):
$env:SMTP_HOST='smtp.example.com'; $env:SMTP_PORT='587'; $env:SMTP_USER='user'; $env:SMTP_PASS='pass'; python scripts\send_alert_email.py --to sbattywolf@hotmail.com --subject "GAIA Alert" --body "Test"

This script DOES NOT store credentials in the repo. It uses env vars:
- SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL (optional)
"""
import os
import smtplib
import argparse
from email.message import EmailMessage


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--to', required=True)
    p.add_argument('--subject', default='GAIA Alert')
    p.add_argument('--body', default='This is a test alert from GAIA')
    args = p.parse_args()

    host = os.environ.get('SMTP_HOST')
    port = int(os.environ.get('SMTP_PORT', '587'))
    user = os.environ.get('SMTP_USER')
    pwd = os.environ.get('SMTP_PASS')
    from_email = os.environ.get('FROM_EMAIL', user)

    if not host or not user or not pwd:
        print('ERROR: SMTP_HOST, SMTP_USER, and SMTP_PASS must be set in environment')
        return 2

    msg = EmailMessage()
    msg['Subject'] = args.subject
    msg['From'] = from_email
    msg['To'] = args.to
    msg.set_content(args.body)

    try:
        with smtplib.SMTP(host, port) as s:
            s.starttls()
            s.login(user, pwd)
            s.send_message(msg)
        print('Email sent to', args.to)
        return 0
    except Exception as e:
        print('Failed to send email:', e)
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
