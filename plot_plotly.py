
# coding: utf-8

# In[1]:

import tpqib
import datetime
import zmq
import pandas as pd
import numpy as np
import numpy
from numpy import inf


import matplotlib.pyplot as plt

import json
import plotly_stream as plyst
import plotly.tools as plyt
import plotly.plotly as ply

import datetime
import time
import random
import pandas as pd
import plotly.plotly as py
import plotly.tools as tls 
from plotly.graph_objs import *
import cufflinks

context = zmq.Context()
# Subscribing to forwarder for trading
port = "7010"
socket_sub = context.socket(zmq.SUB)
socket_sub.connect("tcp://localhost:%s" % port)
socket_sub.setsockopt_string(zmq.SUBSCRIBE, u'SPY')

# Subscribing to IB data to get value
port = "7000"
socket_sub00 = context.socket(zmq.SUB)
socket_sub00.connect("tcp://localhost:%s" % port)
socket_sub00.setsockopt_string(zmq.SUBSCRIBE, u'SPY')

#Forwarding instant value during trade section TRADE
socket_pub = context.socket(zmq.PUB)
socket_pub.bind('tcp://127.0.0.1:7030')

print ("Collecting from <7010> to plot.")

field = ['lastTimestamp', 'askPrice', 'askSize',
         'bidPrice', 'bidSize',
         'low', 'high', 'close',
         'volume', 'lastPrice', 'lastSize', 'halted']


# In[2]:

'''
def preprocessing(df):
    df.bidPrice=df.loc[:,'bidPrice'].replace(to_replace=0, method='ffill')
    df.bidSize=df.loc[:,'bidSize'].replace(to_replace=0, method='ffill')
    df.askPrice=df.loc[:,'askPrice'].replace(to_replace=0, method='ffill')
    df.askSize=df.loc[:,'askSize'].replace(to_replace=0, method='ffill')
    df['Close']=(abs(df.loc[:,'bidPrice'])+abs(df.loc[:,'askPrice']))/2
    df=df.dropna()
    #df['price']=(df.loc[:,['bidPrice','bidSize']].prod(axis=1)+df.loc[:,['askPrice','df.askSize']].prod(axis=1))/(df.loc[:,'bidSize']+df.loc[:,'askSize'])
    df['price']=(df.loc[:,'bidPrice']*df.loc[:,'bidSize']+df.loc[:,'askPrice']*df.loc[:,'askPrice'])/(df.loc[:,'bidSize']+df.loc[:,'askSize'])
    return df
'''    


# In[3]:

#val_df=pd.DataFrame()


# In[4]:

'''
#window=10
#for _ in range(window):
while True:
    val = socket_sub00.recv_string()
    sym,bidPrice,bidSize,askPrice,askSize = val.split()
    dt = datetime.datetime.now()
    val_df = val_df.append(pd.DataFrame({'Stock':sym,'bidPrice': float(bidPrice),'bidSize': float(bidSize),'askPrice': float(askPrice),'askSize': float(askSize)},index=[dt]))
    val_data=preprocessing(val_df)
    val_d=val_data[['Stock','Close']]
    x = val_d.to_string(header=False,index=False).split('\n')
    socket_pub.send_string(x[-1])

    #print(val_df.tail(1))
    #print(val_data.tail(1))
    #print(val_d.tail(1))
    print(x[-1])
'''    


# In[6]:

pc = json.load(open('creds/plotly_creds.json', 'r'))

plyt.set_credentials_file(username=pc['username'], api_key=pc['api_key'])
plyst.plotly_stream.set_stream_tokens(pc['stream_ids'])
#!pip install twisted
# solving module 'twisted' has no attribute '__version__'
#!pip install --upgrade pyopenssl
pcreds = json.load(open('creds/plotly_creds.json', 'r'))
py.sign_in(pcreds['username'], pcreds['api_key'])
from autobahn.twisted.websocket import WebSocketClientProtocol,                                        WebSocketClientFactory
    
# plotly preparations

# get stream id from stream id list
stream_ids = pcreds['stream_ids']

# generate Stream objects
stream_0 = Stream(
    token=stream_ids[0],
    maxpoints=150)
stream_1 = Stream(
    token=stream_ids[1],
    maxpoints=150)
stream_2 = Stream(
    token=stream_ids[2],
    maxpoints=150)
stream_3 = Stream(
    token=stream_ids[3],
    maxpoints=150)
stream_4 = Stream(
    token=stream_ids[4],
    maxpoints=150)
# generate Scatter & Data objects
trace0 = Scatter(
    x=[], y=[],
    mode='lines+markers',
    stream=stream_0,
    name='mid')
trace1 = Scatter(
    x=[], y=[],
    mode='lines+markers',
    stream=stream_1,
    name='REG')
trace2 = Scatter(
    x=[], y=[],
    mode='lines+markers',
    stream=stream_2,
    name='ARIMA')
trace3 = Scatter(
    x=[], y=[],
    mode='lines+markers',
    stream=stream_3,
    name='KM')
trace4 = Scatter(
    x=[], y=[],
    mode='lines+markers',
    stream=stream_4,
    name='LSTM')

dats = Data([trace0, trace1, trace2,trace3,trace4])

# generate figure object
layout = Layout(title='Streaming Plot')
fig = Figure(data=dats, layout=layout)
unique_url = py.plot(fig, filename='stream_plot', auto_open=False)

print('URL of the streaming plot:\n%s' % unique_url)

s0 = py.Stream(stream_ids[0])
s1 = py.Stream(stream_ids[1])
s2 = py.Stream(stream_ids[2])
s3 = py.Stream(stream_ids[3])
s4 = py.Stream(stream_ids[4])

s0.open()
s1.open()
s2.open()
s3.open()
s4.open()


# In[9]:

df = pd.DataFrame()
## warm up upto preprocessing
#final=pd.DataFrame()

#window=20
#for _ in range(window):
while True:
    #iterations += 1
    # after forwarder's start
    ml=socket_sub.recv_string()
    sym,mid,REG,SVR,arima,km,LSTM,UD= ml.split()
    dt = datetime.datetime.now()
    df = df.append(pd.DataFrame({'Stock':sym,'mid': float(mid),'REG':float(REG),'SVR':float(SVR),'arima': float(arima),'km': float(km),'LSTM':float(LSTM),'UD':float(UD)},index=[dt]))
    
        #plotting
    dt = datetime.datetime.now()
    s0.write({'x': str(dt)[11:-3], 'y': float(df['mid'].tail(1))})
    s1.write({'x': str(dt)[11:-3], 'y': float(df['REG'].tail(1))})
    s2.write({'x': str(dt)[11:-3], 'y': float(df['arima'].tail(1))})
    s3.write({'x': str(dt)[11:-3], 'y': float(df['km'].tail(1))})
    s4.write({'x': str(dt)[11:-3], 'y': float(df['LSTM'].tail(1))})
   
    '''
        ## Quaick updation of price
    val = socket_sub00.recv_string()
    sym,bidPrice,bidSize,askPrice,askSize = val.split()
    dt = datetime.datetime.now()
    val_df = val_df.append(pd.DataFrame({'Stock':sym,'bidPrice': float(bidPrice),'bidSize': float(bidSize),'askPrice': float(askPrice),'askSize': float(askSize)},index=[dt]))
    val_data=preprocessing(val_df)
    val_d=val_data[['Stock','Close']]
    x = val_d.to_string(header=False,index=False).split('\n')
    socket_pub.send_string(x[-1])

    #print(val_df.tail(1))
    #print(val_data.tail(1))
    #print(val_d.tail(1))
    print(x[-1])
    '''
    x = df.to_string(header=False,index=False).split('\n')
    print(x[-1])    
    


# In[ ]:



