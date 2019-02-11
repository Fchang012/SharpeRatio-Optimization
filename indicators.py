# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 08:33:26 2017

@author: Frank
"""

import pandas as pd
import numpy as np
import datetime as dt


def Bollinger_Bands(stockSym, dfPrices, windowSize):
    #Strip SPX
    dfPrices = dfPrices[stockSym]
    
    #SMA
    sma = dfPrices.rolling(window=windowSize, min_periods=windowSize).mean()
#    sma = pd.rolling_mean(dfPrices, window=windowSize, min_periods=windowSize)
    
    #STD
    rolling_std = dfPrices.rolling(window=windowSize, min_periods=windowSize).std()
#    rolling_std = pd.rolling_std(dfPrices, window=windowSize, min_periods=windowSize)
    
    #Bands
    topBand = sma + rolling_std*2
    
    bottomBand = sma - rolling_std*2
    
    #BBvalue
    bbValue = (dfPrices - sma)/(rolling_std)
    
    #BB as %
    bbp = (dfPrices - bottomBand) / (topBand - bottomBand)
    
    topBand.columns = ['Top Bollinger Band']
    bottomBand.columns = ['Bottom Bollinger Band']
    bbValue.columns = ['Bollinger Band Value']
    bbp.columns = ['BB']
    
    return topBand, bottomBand, bbValue, bbp


def RSI(stockSyms, dfPrices, windowSize):
    #Find number of of stocks up
    dfPrices = dfPrices[stockSyms]
    
    #Find up or down
    diffs = dfPrices.diff()
    numUp, numDown = diffs.copy(), diffs.copy()
    
    #remove 1st item
    numUp = numUp[1:]
    numDown = numDown[1:]

    numUp[numUp < 0] = 0
    numDown[numDown > 0 ] = 0
    
    #Relative strength
    #Using SMA
    roll_up1 = numUp.rolling(window=windowSize, min_periods=windowSize).mean()
#    roll_up1 = pd.rolling_mean(numUp, window=windowSize, min_periods=windowSize)
    
    roll_down1 = numDown.rolling(window=windowSize, min_periods=windowSize).mean().abs()
#    roll_down1 = pd.rolling_mean(numDown, window=windowSize, min_periods=windowSize).abs()
    
    #Using EWMA
    roll_up2 = numUp.ewm(com=windowSize, min_periods=windowSize).mean()
#    roll_up2 = pd.ewma(numUp, com=windowSize, min_periods=windowSize)
    
    roll_down2 = numDown.ewm(com=windowSize, min_periods=windowSize).mean().abs()
#    roll_down2 = pd.ewma(numDown, com=windowSize, min_periods=windowSize).abs()
    
    RS1 = roll_up1 / roll_down1
    RS2 = roll_up2 / roll_down2
    
    RSI1 = 100.0 - (100.0 / (1.0+RS1))
    RSI2 = 100.0 - (100.0 / (1.0+RS2))
    
    RSI1.columns = ['RSI']
    RSI2.columns = ['RSI']
    
    return RSI1, RSI2
    
def MACD(stockSyms, dfPrices, nSlow=26, nFast=12, nSignal=9):
    dfPrices = dfPrices[stockSyms]
    
    ewmaSlow = dfPrices.ewm(com=nSlow, min_periods=nSlow).mean()
#    ewmaSlow = pd.ewma(dfPrices, com=nSlow, min_periods=nSlow)
    
    ewmaFast = dfPrices.ewm(com=nFast, min_periods=nFast).mean()
#    ewmaFast = pd.ewma(dfPrices, com=nFast, min_periods=nFast)
    
    MACD = ewmaFast-ewmaSlow
    signal = MACD.ewm(com=nSignal).mean()
#    signal = pd.ewma(MACD, com=nSignal)
    
    MACDIndicator = MACD - signal
    
    MACD.columns = ['MACD']
    signal.columns = ['Signal']
    MACDIndicator.columns = ['MACDIndicator']
    return MACD, signal, MACDIndicator
    
def SPYIndicator(dfSPY):
    SPYIndicator = dfSPY - dfSPY.shift(1)
    SPYIndicator[SPYIndicator<0] = -1.0
    SPYIndicator[SPYIndicator>0] = 1.0
    SPYIndicator.columns = ['SPYIndicator']
    return SPYIndicator