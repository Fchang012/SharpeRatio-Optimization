#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
General Stock

@author: frank
"""

import datetime as dt
import pandas as pd
import numpy as np
import SharpeRatioOptimizer as SRO
from read_CSV import get_data

def test_split(df, percent=0.9):
    train = df.ix[0:int(np.round(prices.shape[0]*percent)), :]
    test = df.ix[int(np.round(prices.shape[0]*percent)): , :]
    return train, test

if __name__=="__main__":
    
    #Setting Dates
    sd=dt.datetime(2005,1,1)
    ed=dt.datetime(2017,5,29)
    dates = pd.date_range(sd,ed)
    
    #Symbols    
    symbols = ['PRHSX',
               'PRDSX',
               'TRBCX',
               'TRPBX',
               'PRIDX',
               'PRGTX']
               
    prices = get_data(symbols, dates)
    prices = prices.dropna()
    
    #S&P500 Index
    SPX = get_data(['SPY'], dates)
    SPX = SPX.dropna()
    
    #Testing and Training
    X_train, X_test = test_split(prices)
    SPX_train, SPX_test = test_split(SPX)
    
#    #Initial Allocation
    allocs = np.empty(len(symbols), float)
    allocs.fill(1.0/len(symbols))
    
#    allocs = np.array([0.41,
#                       0.16,
#                       0.14,
#                       0.15,
#                       0.14
#                       ])    
    
    #Value of Portfolio with no optimization
    naivePortfolio = SRO.SharpeRatioOptimizer()
    naivePortfolio.getPortStats(allocs, X_test, sf=252, sv=10000)
    
    print '---No Opt---\n'
    print 'Cumulative Return: ', naivePortfolio.cr, '\n'
    print 'Avg Period Return: ', naivePortfolio.apr, '\n'
    print 'STD Period Return: ', naivePortfolio.sdpr, '\n'
    print 'Sharpe Ratio: ', naivePortfolio.sr, '\n'
    print 'Port Value: ', naivePortfolio.port_val, '\n'
    
    naive = naivePortfolio.port_val[-1]
    
    #Value With Optimization for CR
    optPortolioCR = SRO.SharpeRatioOptimizer()
    optPortCR = optPortolioCR.optimize_cr(X_train, sf=252)
    optPortolioCR.getPortStats(optPortCR, X_test, sf=252, sv=10000)

    print '---CR Opt---\n'
    print 'Cumulative Return: ', optPortolioCR.cr, '\n'
    print 'Avg Period Return: ', optPortolioCR.apr, '\n'
    print 'STD Period Return: ', optPortolioCR.sdpr, '\n'
    print 'Sharpe Ratio: ', optPortolioCR.sr, '\n'
    print 'Port Value: ', optPortolioCR.port_val, '\n'
    print np.round(optPortCR, decimals=2)
    print '\n'
    
    optimalCR = optPortolioCR.port_val[-1]
    
    #Value With Optimization for Sharpe
    optPortolioSR = SRO.SharpeRatioOptimizer()
    optPortSharpe = optPortolioSR.optimize_sharpe(X_train, sf=252)
    optPortolioSR.getPortStats(optPortSharpe, X_test, sf=252, sv=10000)

    print '---Sharpe Opt---\n'
    print 'Cumulative Return: ', optPortolioSR.cr, '\n'
    print 'Avg Period Return: ', optPortolioSR.apr, '\n'
    print 'STD Period Return: ', optPortolioSR.sdpr, '\n'
    print 'Sharpe Ratio: ', optPortolioSR.sr, '\n'
    print 'Port Value: ', optPortolioSR.port_val, '\n'
    print np.round(optPortSharpe, decimals=2)
    print '\n'
    
    optimalSharpe = optPortolioSR.port_val[-1]
    
    
    #S&P500 Baseline
    
    #Initial Allocation
    allocs = np.empty(1, float)
    allocs.fill(1.0/1.0)
    
    SPPortfolio = SRO.SharpeRatioOptimizer()
    SPPortfolio.getPortStats(allocs, SPX_test, sf=252, sv=10000)

    print '---S&P 500 Baseline---\n'
    print 'Cumulative Return: ', SPPortfolio.cr, '\n'
    print 'Avg Period Return: ', SPPortfolio.apr, '\n'
    print 'STD Period Return: ', SPPortfolio.sdpr, '\n'
    print 'Sharpe Ratio: ', SPPortfolio.sr, '\n'
    print 'Port Value: ', SPPortfolio.port_val, '\n'
    print '\n'
    
    optimalSharpe = optPortolioSR.port_val[-1]