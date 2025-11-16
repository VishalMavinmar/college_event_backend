# backend/api/utils.py
import requests
from django.conf import settings

def send_whatsapp_message(number, message):
    """
    Send a simple text message using WhatsApp Cloud API.
    `number` must be in international format without + (e.g. 919699136772 or 919699136772).
    """
    url = f"https://graph.facebook.com/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {"body": message}
    }

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers)
    try:
        data = resp.json()
    except Exception:
        data = resp.text

    if resp.status_code not in (200, 201):
        # log for debugging
        print("WhatsApp API error", resp.status_code, data)
    else:
        print("WhatsApp API success:", data)

    return resp.status_code, data
