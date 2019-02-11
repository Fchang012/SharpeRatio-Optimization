#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Decision Tree Trader
Created on Sat Jun  6 2017

@author: frank
"""

import datetime as dt
import pandas as pd
import numpy as np
from read_CSV import get_data_yahoo, get_data_google
from indicators import Bollinger_Bands, RSI, MACD, SPYIndicator

from sklearn.ensemble import RandomForestClassifier



if __name__ == "__main__":
    #Starting variables
    before_start_date = dt.datetime(2004,6,1)
    start_date = dt.datetime(2005,1,1)
    end_sample_date = dt.datetime(2016,12,31)
    start_outSample_Date = dt.datetime(2017,1,1)
    end_date = dt.datetime(2017,6,6)
    stockSym = ['COP']
    start_val = 100000
    windowSize = 2
    
    #Get full dataset
    dfPrices = get_data_google(stockSym, pd.date_range(before_start_date, end_sample_date))
    dfSPY = dfPrices[['SPY']]
    dfPrices = dfPrices[stockSym]
    
    #Normalize Price
    priceNormed = dfPrices / dfPrices.ix[0]
    SPYNormed = dfSPY / dfSPY.ix[0]
    
    #Call indicators
    topBand, bottomBand, bbValue, bbp = Bollinger_Bands(stockSym, dfPrices, windowSize)
    RSIValueSMA, RSIValueEWM = RSI(stockSym, dfPrices, windowSize)
    MACDValue, signal, MACDIndicator = MACD(stockSym, dfPrices)
    
    SPYInd = SPYIndicator(dfSPY)
    
    #Standardize
    bbp = (bbp - bbp.mean()) / (bbp.std())
    RSIValueEWM = (RSIValueEWM - RSIValueEWM.mean()) / (RSIValueEWM.std())
    MACDValue = (MACDValue - MACDValue.mean()) / (MACDValue.std())
    signal = (signal - signal.mean()) / (signal.std())
    MACDIndicator = (MACDIndicator - MACDIndicator.mean()) / (MACDIndicator.std())
    
    #5 Day Future Returns
    futureReturn = (dfPrices/dfPrices.shift(windowSize)) - 1.0
    futureReturn = futureReturn.shift(-windowSize)
    
    #STD
    STDMulti = 0.000001
#    STDMulti = 2.0
    YBUY = futureReturn.mean() + (STDMulti*futureReturn.std())
    YSELL = futureReturn.mean() - (STDMulti*futureReturn.std())
    
    futureReturn[futureReturn>YBUY] = 1.0
    futureReturn[futureReturn<YSELL] = -1.0
    futureReturn[(futureReturn >= YSELL) & (futureReturn <= YBUY)] = 0.0
    
    futureReturn.columns = ['Future_Return_Buy_Sell']

    dfIndicators = pd.concat((bbp, RSIValueEWM, MACDValue, signal, MACDIndicator, SPYInd, futureReturn), axis=1)
    #Show data from beginning of sample
    dfIndicators = dfIndicators[dfIndicators.index.searchsorted(start_date):]
    
    #Drop last 5 days
    dfIndicators = dfIndicators.dropna()
    
    #Sep X and Y
    trainX = dfIndicators.drop(['Future_Return_Buy_Sell'], axis=1).values
    trainY = dfIndicators['Future_Return_Buy_Sell'].values
    
    #Use Scikit Learn for Random Forrest
    clf = RandomForestClassifier(min_samples_leaf=1)
    clf = clf.fit(trainX, trainY)
    
    #Accuracy
    print clf.score(trainX, trainY)
    
    #Find errors
    differences = pd.DataFrame({"Predicted":clf.predict(trainX), "Actual":trainY})
    differences = differences["Predicted"] == differences["Actual"]