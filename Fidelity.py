# -*- coding: utf-8 -*-
"""
Fidelity Script

@author: Frank
"""

import datetime as dt
import pandas as pd
import numpy as np
import SharpeRatioOptimizer as SRO
from read_CSV import get_data

if __name__=="__main__":
    
    #Setting Dates
    sd=dt.datetime(2016,2,1)
    ed=dt.datetime(2017,2,1)
    dates = pd.date_range(sd,ed)
    
    #Symbols    
    symbols = ['NON40OJJ4120317',
               'NON40OJJ5120317',
               'NON40OJJ6120317',
               'NON40OJJ8120317',
               'NON40OJPF120317',
               'NON40OJPG120317',
               'NON40OXLT120317',
               'OJPH120317']
               
    prices = get_data(symbols, dates)
    prices = prices.dropna()
    
    #Initial Allocation
    allocs = np.empty(len(symbols), float)
    allocs.fill(1.0/len(symbols))
    
    #Value of Portfolio with no optimization
    naivePortfolio = SRO.SharpeRatioOptimizer()
    naivePortfolio.getPortStats(allocs, prices, sf=12, sv=10000)
    
    print 'Cumulative Return: ', naivePortfolio.cr, '\n'
    print 'Avg Period Return: ', naivePortfolio.apr, '\n'
    print 'STD Period Return: ', naivePortfolio.sdpr, '\n'
    print 'Port Value: ', naivePortfolio.port_val, '\n'
    
    naive = naivePortfolio.port_val[-1]
    
    #Value With Optimization for CR
    optPortCR = naivePortfolio.optimize_cr(prices)
    naivePortfolio.getPortStats(optPortCR, prices, sf=12, sv=10000)

    print 'Cumulative Return: ', naivePortfolio.cr, '\n'
    print 'Avg Period Return: ', naivePortfolio.apr, '\n'
    print 'STD Period Return: ', naivePortfolio.sdpr, '\n'
    print 'Port Value: ', naivePortfolio.port_val, '\n'  
    
    optimalCR = naivePortfolio.port_val[-1]
    
    #Value With Optimization for Sharpe
    optPortSharpe = naivePortfolio.optimize_sharpe(prices)
    naivePortfolio.getPortStats(optPortSharpe, prices, sf=12, sv=10000)

    print 'Cumulative Return: ', naivePortfolio.cr, '\n'
    print 'Avg Period Return: ', naivePortfolio.apr, '\n'
    print 'STD Period Return: ', naivePortfolio.sdpr, '\n'
    print 'Port Value: ', naivePortfolio.port_val, '\n'  
    
    optimalSharpe = naivePortfolio.port_val[-1]