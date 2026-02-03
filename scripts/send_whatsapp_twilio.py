"""Send a WhatsApp message via Twilio REST API using env vars TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_WHATSAPP, TO_WHATSAPP.
Usage (PowerShell):
$env:TWILIO_ACCOUNT_SID='AC...'; $env:TWILIO_AUTH_TOKEN='...'; $env:FROM_WHATSAPP='whatsapp:+1415...'; $env:TO_WHATSAPP='whatsapp:+1XXX...'; python scripts\send_whatsapp_twilio.py --text "Hello"

Note: Requires a Twilio account with WhatsApp sandbox or approved WhatsApp business number.
"""
import os
import argparse
import requests
from requests.auth import HTTPBasicAuth


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--text', default='GAIA test WhatsApp alert')
    args = p.parse_args()

    sid = os.environ.get('TWILIO_ACCOUNT_SID')
    token = os.environ.get('TWILIO_AUTH_TOKEN')
    frm = os.environ.get('FROM_WHATSAPP')
    to = os.environ.get('TO_WHATSAPP')
    if not sid or not token or not frm or not to:
        print('ERROR: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_WHATSAPP, TO_WHATSAPP must be set')
        return 2

    url = f'https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json'
    data = {'From': frm, 'To': to, 'Body': args.text}
    try:
        r = requests.post(url, data=data, auth=HTTPBasicAuth(sid, token))
        r.raise_for_status()
        print('WhatsApp message enqueued via Twilio')
        return 0
    except Exception as e:
        print('Failed to send WhatsApp message via Twilio:', e)
        try:
            print(r.text)
        except Exception:
            pass
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
