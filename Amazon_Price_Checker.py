import requests
from bs4 import BeautifulSoup
import smtplib
import time
head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
from configparser import ConfigParser

parser = ConfigParser()
parser.read('configuration.ini')

URL=parser.get('settings','url')
check = True
temp = input('Enter required price')
temp = int(temp)
def check_price():
    global temp
    page = requests.get(URL,headers=head)

    soup = BeautifulSoup(page.content, 'html.parser')


    price = soup.find(id='priceblock_ourprice').get_text()
    value=int(price[2:5])
    
    print('checking price')
    print()
    if(value<=temp):
        send_mail(parser.get('settings','sending_mail'),parser.get('settings','recieving_mail'),parser.get('settings','password'),parser.get('settings','url'))    




def send_mail(smail,rmail,password,link):
    global check
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(smail,password)

    subject = 'Price fell down'
    body='Product is a little cheaper '+ link

    msg = f"Subject :{subject}\n\n{body}"

    server.sendmail(
        smail,
        rmail,
        msg

    )
    print('email has been sent')
    check = False

    server.quit()



while(True):
    check_price()
    if(check==False):
        break
    time.sleep(parser.getint('settings','interval'))
    
