import configparser
import smtplib
import ssl

from libs.JStore import JStore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Read Configuration
config = configparser.ConfigParser()
config.read('../config.ini')

# Selenium Options
driver_options = Options()
driver_options.add_argument('--headless')
driver_options.add_argument('--no-sandbox')

# Selenium Service
driver_service = Service(ChromeDriverManager().install())

# Selenium Driver
driver = webdriver.Chrome(service=driver_service, options=driver_options)
driver.implicitly_wait(30)

# FileCache
cache = JStore('../cache.json')

previously_in_stock = cache.get_bool('in_stock')

print("-----------------------")
print("elePHPant-stock-scraper")
print("    - JacobFitzp       ")
print("-----------------------")
print("> Sending Request")

driver.get(config['DEFAULT']['PRODUCT'])

# Check if page has out-of-stock element
try:
    print(" > No Stock Found")
    driver.find_element(By.CSS_SELECTOR, '.stock.out-of-stock')
    in_stock = False
except():
    print(" > Stock Found")
    in_stock = True

# In-stock Email Message
in_stock_message = """\
Subject: elePHPant In-Stock!

elePHPant stock scraper has detected available stock!

Product URL: {}
""".format(config['DEFAULT']['PRODUCT'])

# Out-of-stock Email Message
out_of_stock_message = """\
Subject: elePHPant Out-Of-Stock!

elePHPant stock scraper has detected that all available stock has sold out.

Product URL: {}
""".format(config['DEFAULT']['PRODUCT'])

send_in_stock_email = in_stock and not previously_in_stock
send_out_of_stock_email = not in_stock and previously_in_stock

# Send email if in-stock
if send_in_stock_email or send_out_of_stock_email:
    print("> Sending Email")

    context = ssl.create_default_context()
    email_message = in_stock_message

    if send_out_of_stock_email:
        email_message = out_of_stock_message

    with smtplib.SMTP_SSL(config['SMTP']['HOST'], config['SMTP']['PORT'], context=context) as server:
        server.login(config['SMTP']['USERNAME'], config['SMTP']['PASSWORD'])
        server.sendmail(config['SMTP']['USERNAME'], config['DEFAULT']['RECIPIENT'], email_message)

        print(" > Email Sent")

cache.set('in_stock', in_stock)

print("> Finished")
