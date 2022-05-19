# elePHPant Stock Scraper

Simple python script to scrape for elePHPant stock.

### Disclaimer 

Please do not abuse this script! Run only occasionally, to minimise any disruption.

### Prerequisites 

- Install Python 3
- Install dependencies 
  - `pip install webdriver-manager`
  - `pip install selenium`

### Configuration 

This script can be configured in `config.ini`

`PRODUCT` The URL of the product you want (only supports vincentpontier.com)

`RECIPIENT` The email address to send stock alerts to

#### SMTP

You will need to set up SMTP to send the emails, I recommend making a free Gmail account and using Google's SMTP server.

### Usage 

Simply run `./src/main.py` to check for stock.

I recommend setting up a cronjob to run this for you every so often.

