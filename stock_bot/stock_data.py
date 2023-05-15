import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

"""
get_ticker_symbol(company_name) takes in a company's name and 
returns the company's ticker symbol

requires: company_name is valid

ex: get_ticker_symbol("Apple") -> AAPL
"""

def get_ticker_symbol(company_name: str):
    url = f"https://www.google.com/finance/quote/" + company_name
    page = requests.get(url)
    get_text = page.text
    bs4 = BeautifulSoup(get_text, 'html.parser')
    company_ticker = bs4.find("div", class_= "COaKTb")
    return company_ticker.get_text()

"""
get_company_name(ticker) takes in a company's ticker and 
returns the company's name

requires: ticker is valid

ex: get_ticker_symbol("AAPL") -> Apple Inc
"""

def get_company_name(ticker: str):
    url = f"https://www.google.com/finance/quote/" + ticker
    page = requests.get(url)
    get_text = page.text
    bs4 = BeautifulSoup(get_text, 'html.parser')
    company_ticker = bs4.find("div", class_= "ZvmM7")
    return company_ticker.get_text()

"""
get_current_price(ticker) takes in a company's ticker and 
returns the list: current stock price, change in stock price (in $), change in stock price (in %)

requires: ticker is valid

ex: get_current_price('AAPL') -> [173.55, 1.78, 1.04]
"""

def get_current_price(ticker: str):
    company = yf.Ticker(ticker)
    todays_data = company.history(period='5d')
    todays_price = round(todays_data['Close'][4],2)
    yesterdays_price = round(todays_data['Close'][3],2)
    diff_price = round(todays_price - yesterdays_price, 2)
    diff_percent = round((diff_price / yesterdays_price) * 100,2)
    return [todays_price,diff_price,diff_percent]

"""
stock_graph(ticker, time) takes in a company's ticker and desired time period to
return a png image (graph.png) which displays stock performance in that time period

if time is not give (time = None), time duration will be set to 1 year by default

requires: ticker is valid
"""

def stock_graph(ticker: str, time: str):
    company = yf.download(tickers = ticker, period = "1y")
    if time != None: 
        company = yf.download(tickers = ticker, period = time)
    company_name = get_company_name(ticker)
    company.reset_index(inplace=True)
    plt.figure(figsize=(10,5))
    sns.set_style("ticks")
    sns.lineplot(data=company,x="Date",y='Close',color='firebrick')
    sns.despine()
    if time == None:
        plt.title("The Stock Price of " + company_name + " (1y)",size='x-large',color='blue')
    else: 
        plt.title("The Stock Price of " + company_name + " (" + time + ")",size='x-large',color='blue')

    plt.savefig("graph.png")

def get_headlines(ticker:str): 
    company = yf.Ticker(ticker)
    return company.get_news()
    



 
