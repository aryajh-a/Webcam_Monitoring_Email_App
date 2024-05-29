import smtplib
import imghdr
from email.message import EmailMessage

SENDER = "aryajha0601@gmail.com"
RECEIVER = "aryajha0601@gmail.com"
PASSWORD = "bcumonikdyjytpsc"
smtp_server = "smtp.gmail.com"
smtp_port = 587

def send_mail(image_path):
    email_message = EmailMessage()
    email_message['Subject'] = "Someone arrived at the front door"
    email_message.set_content(f"Hey!! Someone just arrived at your front door. \nPlease find the attached image.")
    
    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype = "image", subtype = imghdr.what(None, content))
    
    
    gmail = smtplib.SMTP(smtp_server, smtp_port)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    