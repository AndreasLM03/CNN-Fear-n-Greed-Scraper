#!/usr/bin/python

import time 
import datetime
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP
import smtplib
import sys

### TIME
UnixTime = int(time.time()) # get current unix epoch time
currentdate = datetime.datetime.fromtimestamp(UnixTime).strftime('%Y-%m-%d') # get current date


### Find Fear and Greed Value in Sourcecode
URL = 'https://money.cnn.com/data/fear-and-greed/'
response = requests.get(URL).text
soup = BeautifulSoup(response, 'html.parser')
soup2 = str(soup)
ind1=soup2.find('; Greed Now: ') # Show the position in the string where the first search indicator is located
ind2=soup2.find('; Greed Previous Close:') # Show the position in the string where the second search indicator is located
FnG = soup2[ind1:ind2] # Store only the range between first and second indicator
FnG = re.findall(r'\d+', FnG) # find a digits
FnG = int(FnG[0]) 

FnG_newrow = ([UnixTime, int(datetime.datetime.fromtimestamp(UnixTime).strftime('%Y')), int(datetime.datetime.fromtimestamp(UnixTime).strftime('%m')), int(datetime.datetime.fromtimestamp(UnixTime).strftime('%d')), int(datetime.datetime.fromtimestamp(UnixTime).strftime('%H' + "00")), FnG])

## Save Data
# If there is no existing list, then a NumPy list must be created for the first time
#FnG_csv = np.zeros((1,5))
Path = "/home/pi/Dokumente/Programme/Fear_and_Greed/Fear_and_Greed.csv"

# csv load 
FnG_csv = np.loadtxt(Path, delimiter=",")
FnG_csv = np.flipud(FnG_csv)
FnG_csv = np.vstack([FnG_csv, FnG_newrow])

FnG_csv = np.flipud(FnG_csv)
# csv save
fmt = fmt = '%d', '%d', '%d', '%d','%d', '%1.2f'
np.savetxt(Path, FnG_csv, delimiter=",", fmt=fmt)



MailTrigger = 0
if FnG > 90:
    State = "Overheated"
    MailTrigger = 1
    print(State)
elif FnG < 5:
    State = "Buying-opportunity"
    MailTrigger = 1
    print(State)
    
 
    
if MailTrigger == 1:
    fromaddr = 'OutputMailAccount' #(eg. peter_pan@gmail.com)
    toaddr = 'TargetMailAccound' #(eg. mice@gmail.com)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = currentdate + "_FnG: " + State
    body = ''
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, 'OutputMailAccountPassword') #(e.g. 123123)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
