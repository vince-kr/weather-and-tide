import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(mail_body: str, todays_date: str) -> None:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'Weather report - {todays_date}'
    msg['From'] = 'weather@krijnsen.com'
    msg['To'] = 'vince@krijnsen.com'

    html_contents = MIMEText(mail_body, 'html')
    msg.attach(html_contents)

    with smtplib.SMTP('smtp.greenhost.nl', 587) as greenhost:
        greenhost.starttls()
        greenhost.login('weather@krijnsen.com', 'BenWe4th')
        greenhost.send_message(msg)
