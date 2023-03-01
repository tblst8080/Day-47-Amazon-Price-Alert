import requests
from bs4 import BeautifulSoup
import lxml
from price_log import Tracker
from smtpfile import Notifier
import re
from dotenv import load_dotenv
import os
from watchlist import WishList

load_dotenv()

header = {
    'Accepted-Language': os.environ['ACCEPTED_LANGUAGE'],
    'User-Agent': os.environ['USER_AGENT']}


def check_price(url, header):
    response = requests.get(url=url, headers=header)
    content = response.text

    soup = BeautifulSoup(content, 'lxml')

    price_element = soup.find(name='input', id='twister-plus-price-data-price')
    current_price = float(price_element.get("value"))

    product_element = soup.find(name='title')
    product_name = product_element.getText().replace("Amazon.com: ", "")
    print(f"\nSearching: {product_name}...")

    coupon_element = soup.find(id=re.compile('couponText'))
    if coupon_element:
        coupon_text = coupon_element.getText()
        coupon_text = coupon_text.split('coupon')[0]
        coupon_text = coupon_text.split('Apply')[1]
        coupon_text = coupon_text.strip()
        if '$' in coupon_text:
            value = float(coupon_text.replace('$', ''))
            current_price = round(current_price - value, 2)
        elif '%' in coupon_text:
            value = float(coupon_text.replace('%', '')) / 100
            current_price = round(current_price * (1 - value))
    else:
        print("no coupon found")

    tracker.add_price(product=product_name, price=current_price)
    if current_price < tracker.price_threshold(product_name) and len(tracker.df[product_name.title()].values) > 7:
        notifier = Notifier()
        notifier.send_price_alert(price=current_price, product=product_name, link=url)
    else:
        print("No notification sent.")


tracker = Tracker()
my_wishlist = WishList()

# Refresh price history:
for column in tracker.df.columns.values:
    if column not in [entry['url'] for entry in my_wishlist.content]:
        tracker.remove_column(column)

# Check low prices for each item in watchlist
for entry in my_wishlist.content:
    check_price(url=entry['url'], header=header)
