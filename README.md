# CNN-Fear-n-Greed-Scraper
If the market is crashing and everyone is afraid, then you should buy stocks.


This script downloads and saves the current CNN Fear and Greed Index at user-defined time intervals. At critical values it sends information mails, which warn you of a market overheating or if there is particularly big panic on the markets. 



---
## Fear and Greed

https://money.cnn.com/data/fear-and-greed/

The fear and greed index is a contrarian index of sorts. It is based on the premise that excessive fear can result in stocks trading well below their intrinsic values, and that unbridled greed can result in stocks being bid up far above what they should be worth. 

CNN examines seven different factors to establish how much fear and greed there is in the market. They are:


Stock Price Momentum: Measuring the Standard & Poor's 500 Index (S&P 500) versus its 125-day moving average (MA)

Stock Price Strength: Calculating the number of stocks hitting 52-week highs versus those hitting 52-week lows on the New York Stock Exchange (NYSE)

Stock Price Breadth: Analyzing trading volumes in rising stocks against declining stocks

Put and Call Options: How much do put options lag behind call options, signifying greed, or surpass them, indicating fear

Junk Bond Demand: Gauging appetite for higher risk strategies by measuring the spread between yields on investment-grade bonds and junk bonds

Market Volatility: CNN measures the Chicago Board Options Exchange Volatility Index (VIX), concentrating on a 50-day MA

Safe Haven Demand: The difference in returns for stocks versus treasuries

(https://www.investopedia.com/terms/f/fear-and-greed-index.asp#:~:text=The%20fear%20and%20greed%20index%20is%20a%20contrarian%20index%20of,what%20they%20should%20be%20worth)

---
## Python Script

copy attached python script on your raspberry pi or copy this text into a python file



```python
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

#TIME

UnixTime = int(time.time()) # get current unix epoch time
currentdate = datetime.datetime.fromtimestamp(UnixTime).strftime('%Y-%m-%d') # get current date


#Find Fear and Greed Value in Sourcecode

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



#csv load 
#If there is no existing list, then a NumPy list must be created for the first time
#FnG_csv = np.zeros((1,5))
Path = "/home/pi/Dokumente/Programme/Fear_and_Greed/Fear_and_Greed.csv"
FnG_csv = np.loadtxt(Path, delimiter=",")
FnG_csv = np.flipud(FnG_csv)
FnG_csv = np.vstack([FnG_csv, FnG_newrow])

FnG_csv = np.flipud(FnG_csv)
#csv save
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
```    


---
## Output csv file

    
| UNIX EPOCH | YEAR | MONTH | DAY | HOUR | Fear and Greed Index  |
|     :---:      | :---:      | :---:      | :---:      | :---:      | :---:      | 
| 1613484062 | 2021 | 2 | 16 | 1500 | 58 |
| 1613480463 | 2021 | 2 | 16 | 1400 | 58 |
| 1613476863 | 2021 | 2 | 16 | 1300 | 63 |


---
## Run the script automatically every hour

Go on your terminal and enter crontab -e and enter this command

```python
1 * * * * /usr/bin/python3 /home/pi/Dokumente/Programme/Fear_and_Greed/20_12_30_Fear_and_Greed.py
```   
This script will be executed every hour and one minute


---
## Upload your CSV file into your clouad on your raspberry pi


```python
3 * * * *  /home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Dokumente/Programme/Fear_and_Greed/Fear_and_Greed$
```   
This script will be executed every hour and 3 minutes. The time delay is due to the fact that in case the Python script takes longer to retrieve and save the data, the latest data will still be uploaded to the cloud.











