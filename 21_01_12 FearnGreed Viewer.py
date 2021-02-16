#!/usr/bin/python

from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import os, sys
import time
import os
from os import makedirs
import shutil
from currency_converter import CurrencyConverter
import quandl as ql
import datetime

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import quandl as ql
from datetime import date
import time
import datetime
import yfinance as yf
%matplotlib widget
%matplotlib inline


import pandas as pd
filename = "C:/Users/andre/Dropbox/Apps/alm.gold.2020.coin/Fear_and_Greed.csv"
# df = pd.read_csv(filename, sep='\t', encoding = 'utf-16',nrows=10,  index_col="CASE") #Filename, Tabulator, Textcodierung, lade nur die ersten 10 Reihen ein, nehme Case als Index
df = pd.read_csv(filename, sep=',')
df.columns = ['UNIX', 'Jahr', 'Monat', 'Tag','UHrzeit', 'FnG']


fig, ax1 = plt.subplots(figsize=(20,12))
ax1.grid(color='black', linestyle='--', linewidth=0.05)
color = 'tab:red'
ax1.set_xlabel('date')
ax1.set_ylabel('Fear and Greed', color=color)

ax1.plot(pd.to_datetime(df['UNIX'],unit='s'), df.FnG, label='FnG', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax1.axhspan(0, 10, alpha=0.3, color='#fb9898')
ax1.axhspan(100, 90, alpha=0.3, color='#6a5acd')


ax1.set_ylim([0, 100])
fig.tight_layout()  # otherwise the right y-label is slightly clipped