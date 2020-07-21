import requests
from bs4 import BeautifulSoup
import smtplib
import time
from configparser import ConfigParser
import re

parser = ConfigParser()
parser.read('configuration.ini')

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}


check1 = True
check2 = True
check3 = True
temp = []


def cur_URL(number):
    if(number == 0):
        return parser.get('settings', 'url1')
    elif(number == 1):
        return parser.get('settings', 'url2')
    elif(number == 2):
        return parser.get('settings', 'url3')


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
            'settings', 'recieving_mail'), parser.get('settings', 'password'), parser.get('settings', link))

    return


def send_mail(smail, rmail, password, link):
    global check1
    global check2
    global check3
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
    if(link == 'url1'):
        check1 = False
    elif(link == 'url2'):
        check2 = False
    else:
        check3 = False

    server.quit()
    return


def prods():
    for x in range(parser.getint('settings', 'products')):
        for y in range(x+1):
            temp_ = 'url' + str(y+1)
            index = y
            check_price(temp_, index)


while(True):

    print('checking price')
    print()

    prods()
    if(not(check1 and check2 and check3)):
        break

    time.sleep(parser.getint('settings', 'interval'))
