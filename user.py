# Next update user login
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

import os
import random

def userlogin():
    key  = random.randint(100000, 999999 )


    msg = MIMEText(f"Testing mail service code : {key}")
    msg['Subject'] = "Test email"
    msg["From"] = os.getenv("EMAIL")
    msg["To"] = os.getenv("EMAIL_TO")


    with smtplib.SMTP("smtp.gmail.com" , 587) as server:
        server.starttls()
        server.login(os.getenv("EMAIL"), os.getenv("PW"))
        server.send_message(msg)

    return key
             

    
