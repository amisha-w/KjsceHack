import numpy as np
from datetime import datetime
import smtplib
import time
import os
from selenium import webdriver
#For Prediction
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing,svm
from sklearn.model_selection import train_test_split
#For Stock Data
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data

def getStocks(n):
    #Navigating to the Yahoo stock screener    
    chrome_driver_path = './chromedriver.exe'
    driver = webdriver.Chrome(chrome_driver_path)
    url = 'https://finance.yahoo.com/screener/predefined/aggressive_small_caps?offset=0&count=202'
    driver.get(url)

    stock_list = []
    n += 1
    for i in range(1, n):
        ticker = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[' + str(i) + ']/td[1]/a')
        stock_list.append(ticker.text)

    #Using the stock list to predict the future price of the stock a specificed amount of days
    for i in stock_list:
        try:
            predictData(i, 5)
        except:
            print("Stock: " + i + " was not predicted")


def predictData(stock,days):
    start = datetime(2017, 1, 1)
    end = datetime.now()
    #Outputting the Historical data into a .csv for later use
    df = get_historical_data(stock, start=start, end=end,     output_format='pandas')
    csv_name = ('Exports/' + stock + '_Export.csv')
    df.to_csv(csv_name)
    df['prediction'] = df['close'].shift(-1)
    df.dropna(inplace=True)
    forecast_time = int(days)
    X = np.array(df.drop(['prediction'], 1))
    Y = np.array(df['prediction'])
    X = preprocessing.scale(X)
    X_prediction = X[-forecast_time:]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5)

    #Performing the Regression on the training data
    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))

    print(prediction)


getStocks(200)