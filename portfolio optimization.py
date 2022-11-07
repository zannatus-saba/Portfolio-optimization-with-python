import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import os
import numpy as np
import datetime
import yfinance as yf

os.chdir('C:/Users/zanna/Downloads/')
df1=pd.read_parquet('taq_20210301.parquet',columns=['secs', 'Symbol', 'Trade Volume', 'Trade Price', 'BS'])
print(df1)

day0 = '2021-03-01'
day1= '2021-09-01'
df1['date'] = pd.to_datetime(day0 + ' '+ (df1['secs']).astype(str), format = '%Y-%m-%d %H%M%S%f')

#Dollar volume today for all stocks
df1["dol_vol"]= df1['Trade Volume']*df1['Trade Price']

# change sell dvol to negative
df1.loc[df1.BS == 'S' , 'dol_vol'] = -df1.dol_vol

#for 500 stocks
n=500
middle=[int(n/2)-3 , int(n/2)+2]

#daily data
daily= df1.groupby('Symbol')['dol_vol'].sum()
daily=daily.sort_values(ascending=False)
daily.plot()

#top 5, middle 5, last 5
top05=daily[0:n][0:5].index.to_list()
mid05=daily[0:n][middle[0]:middle[1]].index.to_list()
last05=daily[0:n][-5:].index.to_list()

#plotting each stock

ticker=top05+mid05+last05
tic_df=yf.Tickers(ticker).history(start=day0, end=day1).Close.pct_change().cumsum()
tic_df.plot()
tic_df[top05].plot()
tic_df[mid05].plot()
tic_df[last05].plot()

#creating a table for returning stock return in annual terms
tic_df=yf.Tickers(ticker).history(start=day0, end=day1).Close.pct_change()
tic_df=(((tic_df+1)**365)-1)*100
print(tic_df)

#standard deviation
tic_df.std()





