import configparser
import json
import os.path
import smtplib
import ssl

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

# Get Previous Results
if os.path.exists("../cache.json"):
    with open('../cache.json', 'r') as openfile:
        json_object = json.load(openfile)
        previouslyInStock = json_object['inStock']
else:
    previouslyInStock = False

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
    inStock = False
except():
    print(" > Stock Found")
    inStock = True

# In-stock Email Message
inStockMessage = """\
Subject: elePHPant In-Stock!

elePHPant stock scraper has detected available stock!

Product URL: {}
""".format(config['DEFAULT']['PRODUCT'])

# Out-of-stock Email Message
outOfStockMessage = """\
Subject: elePHPant Out-Of-Stock!

elePHPant stock scraper has detected that all available stock has sold out.

Product URL: {}
""".format(config['DEFAULT']['PRODUCT'])

# Send email if in-stock
if inStock and not previouslyInStock:
    print("> Sending Email")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(config['SMTP']['HOST'], config['SMTP']['PORT'], context=context) as server:
        server.login(config['SMTP']['USERNAME'], config['SMTP']['PASSWORD'])
        server.sendmail(config['SMTP']['USERNAME'], config['DEFAULT']['RECIPIENT'], inStockMessage)

        print(" > Email Sent [In-Stock]")

if not inStock and previouslyInStock:
    print("> Sending Email")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(config['SMTP']['HOST'], config['SMTP']['PORT'], context=context) as server:
        server.login(config['SMTP']['USERNAME'], config['SMTP']['PASSWORD'])
        server.sendmail(config['SMTP']['USERNAME'], config['DEFAULT']['RECIPIENT'], outOfStockMessage)

        print(" > Email Sent [Out-Of-Stock]")

print("> Caching Results")
# Write results to disk
results = {
    "inStock": inStock
}

jsonData = json.dumps(results, indent=4)

with open("../cache.json", "w") as outfile:
    outfile.write(jsonData)
    print(" > Results Cached")

print("> Finished")
