# backend/api/utils.py
import pywhatkit

def send_whatsapp_message(number, message):
    """
    Opens WhatsApp Web and types the message automatically.
    CR can manually press send.
    """
    # number: must include country code, e.g., "91xxxxxxxxxx"
    pywhatkit.sendwhatmsg_instantly(
        phone_no=f"+{number}",  # Add + if needed
        message=message,
        wait_time=10,           # Time to load WhatsApp Web
        tab_close=False,        # Do not close tab automatically
        close_time=3            # Optional, seconds to wait after typing
    )
