import requests
from bs4 import BeautifulSoup
import smtplib
import time
from configparser import ConfigParser
import re

parser = ConfigParser()
parser.read('configuration.ini')

head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}


check1 = True
check2 = True
check3 = True
temp=[]

for x in range(parser.getint('settings','products')):
    swap = input('enter required price for product'+ str(x+1) + " ")
    temp.append(swap) 
    print()
    
    

def check_price(link,product_no):
    global temp
    URL=parser.get('settings',link)
    page = requests.get(URL,headers=head)
    soup = BeautifulSoup(page.content, 'html.parser' )

    price = soup.find(id='priceblock_ourprice').get_text()
    price =remove_sp(price)
    
    
    if(price<=float(temp[product_no])):
        send_mail(parser.get('settings','sending_mail'),parser.get('settings','recieving_mail'),parser.get('settings','password'),parser.get('settings',link))    

    return

def remove_sp(str):
    str = re.sub("\s",'',str)
    str = re.sub("₹",'',str)
    str = re.sub(",",'',str)
    
    str= float(str)
    return str

def send_mail(smail,rmail,password,link):
    global check1
    global check2
    global check3
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(smail,password)

    subject = 'Price fell'
    body='Product is a little cheaper '+ link

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


while(True):
    
    print('checking price')
    print()
    
    if(parser.getint('settings','products')==1):
        check_price('url1',0)
    elif(parser.getint('settings','products')==2):
        check_price('url1',0)
        check_price('url2',1)
    elif(parser.getint('settings','products')==3):    
        check_price('url1',0)
        check_price('url2',1)
        check_price('url3',2)
    if(not(check1 and check2 and check3)):
        break
    
    time.sleep(parser.getint('settings','interval'))
    


