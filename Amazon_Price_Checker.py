import requests
from bs4 import BeautifulSoup
import smtplib
import time
from configparser import ConfigParser
import re
from functools import reduce

parser = ConfigParser()
parser.read('configuration.ini')

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}


check = []
temp = []


def bool_list(number):
    global check
    temp_ = True
    for x in range(number):
        check.append(temp_)


bool_list(parser.getint('settings', 'products'))


def cur_URL(number):
    temp_ = 'url' + str(number+1)
    return(parser.get('settings', temp_))


def cur_Price(no):

    URL = cur_URL(no)
    page = requests.get(URL, headers=head)
    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find(id='priceblock_ourprice').get_text()
    price = remove_sp(price)
    print('current price is ₹', price)


def remove_sp(str):
    str = re.sub("\s", '', str)
    str = re.sub("₹", '', str)
    str = re.sub(",", '', str)

    str = float(str)
    return str


for x in range(parser.getint('settings', 'products')):
    cur_Price(x)
    swap = input('enter required price for product' + str(x+1) + " ")
    temp.append(swap)
    print()


def check_price(link, product_no):
    global temp
    URL = parser.get('settings', link)
    page = requests.get(URL, headers=head)
    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find(id='priceblock_ourprice').get_text()
    price = remove_sp(price)

    if(price <= float(temp[product_no])):
        send_mail(parser.get('settings', 'sending_mail'), parser.get(
            'settings', 'recieving_mail'), parser.get('settings', 'password'), parser.get('settings', link), product_no)

    return


def send_mail(smail, rmail, password, link, number):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(smail, password)

    subject = 'Price fell down'
    body = 'Product is a little cheaper ' + link

    msg = f"Subject :{subject}\n\n{body}"

    server.sendmail(
        smail,
        rmail,
        msg

    )
    print('email has been sent')
    check[number] = False

    server.quit()
    return


def prods():
    x = parser.getint('settings', 'products')
    for y in range(x):
        temp_ = 'url' + str(y+1)
        index = y
        if(check[y] == True):
            check_price(temp_, index)


while(True):

    print('checking price')
    print()
    prods()
    if (not(reduce(lambda a, b: a+b, check))):
        break

    time.sleep(parser.getint('settings', 'interval'))
