#Load the packages
from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.models import Legend
from bokeh.plotting import figure, show
from bokeh.models.formatters import DatetimeTickFormatter
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime

#Connect the app
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('home.html')




@app.route('/about',methods = ['GET','POST'])
def about():
  if request.method=='GET':
    return render_template('home.html')
  
  else:
    vars = {}
    ticker = request.form['ticker']
    varnames = ['close','adj_close','open']
    for vn in varnames:
      try:
        vars[vn] = request.form['features_'+vn]
      except:
        vars[vn] = 0
    key = 'O0YXZHA3HRN94A94'
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}&outputsize=compact'.format(ticker, key)
    response = requests.get(url)
    df = pd.DataFrame(response.json()['Time Series (Daily)']).transpose()
    df=df.iloc[::-1]
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'date'})
    df.columns=['date','open','high','low','close','adjusted close','volume','dividend','split']
    columnsdict = {'close': 'close',\
               'adj_close': 'adjusted close',\
               'open': 'open'}
    ys = [vn for vn in vars if vars[vn]!=0]
    columnslist=[columnsdict[y] for y in ys]
    clrs = ["orange","navy","grey"]
    plt = figure(plot_width=600, plot_height=500,x_axis_type="datetime", title =ticker+" Prices")
    for p in range(len(ys)):
      plt.line(df['date'],df[columnsdict[ys[p]]],\
           color = clrs[p],\
           alpha = 0.8,\
           line_width=1.5,\
           legend_label = ticker + ": " + columnslist[p])
      plt.xaxis.axis_label = "Date"
      plt.yaxis.axis_label = "Price $"
      plt.legend.location = "top_right"
    script,div=components(plt)
    
    return render_template('about.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
    
    
