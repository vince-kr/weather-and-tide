from config import SEND_EMAIL_ADDRESS, SEND_EMAIL_PASSWORD
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(mail_body: str, recipients: list[str], todays_date: str) -> None:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'Weather report - {todays_date}'
    msg['From'] = SEND_EMAIL_ADDRESS
    msg['To'] = ", ".join(recipients)

    html_contents = MIMEText(mail_body, 'html')
    msg.attach(html_contents)

    with smtplib.SMTP('smtp.greenhost.nl', 587) as greenhost:
        greenhost.starttls()
        greenhost.login(SEND_EMAIL_ADDRESS, SEND_EMAIL_PASSWORD)
        greenhost.sendmail(SEND_EMAIL_ADDRESS, recipients, msg.as_string())
