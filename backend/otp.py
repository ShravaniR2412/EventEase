# otp.py
import os
import random
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

otp_storage = {}

def generate_and_send_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    subject = "Your OTP for EventEase"
    body = f"Your One-Time Password is: {otp}"

    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return {"success": True, "message": "OTP sent successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_stored_otp(email):
    return otp_storage.get(email)
