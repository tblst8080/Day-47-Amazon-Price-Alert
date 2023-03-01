from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

load_dotenv()


class Notifier:
    def __init__(self):
        self.sender = os.environ['SENDER_EMAIL']
        self.password = os.environ['SENDER_PASSWORD']
        self.recipient = os.environ['RECIPIENT_EMAIL']

    def send_price_alert(self, price, product, link):
        message = f"Subject: Price Alert!\n\nThe {product} on your watchlist is currently on sale for {price}!"

        email_body = f'\
        <p style="font-family:Arial;font-size:14px;text-align:center;"><b>\
        The {product} on your watchlist is currently on sale for {price}!\
        </b><br><br>\
        <a href="{link}">Link to product!</a><br><br>\
        </p>'

        msg = MIMEText(email_body, 'html')
        msg['Subject'] = f"Record low price for {product}!"
        msg['To'] = 'Subscribers'

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.sender, password=self.password)
            connection.sendmail(from_addr=self.sender, to_addrs=self.recipient, msg=msg.as_string())
        print("Notification sent.")