from config import SEND_EMAIL_ADDRESS, SEND_EMAIL_PASSWORD
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(mail_body: str, todays_date: str) -> None:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'Weather report - {todays_date}'
    msg['From'] = SEND_EMAIL_ADDRESS
    msg['To'] = 'vince@krijnsen.com'

    html_contents = MIMEText(mail_body, 'html')
    msg.attach(html_contents)

    with smtplib.SMTP('smtp.greenhost.nl', 587) as greenhost:
        greenhost.starttls()
        greenhost.login(SEND_EMAIL_ADDRESS, SEND_EMAIL_PASSWORD)
        greenhost.send_message(msg)
