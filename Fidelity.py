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
    symbols = ['NON40OJJ4',
               'NON40OJJ5',
               'NON40OJJ6',
               'NON40OJJ8',
               'NON40OJPF',
               'NON40OJPG',
               'NON40OXLT',
               'OJPH'
               ]
               
    prices = get_data(symbols, dates)
    prices = prices.dropna()
    
    #Initial Allocation
#    allocs = np.empty(len(symbols), float)
#    allocs.fill(1.0/len(symbols))
    
    allocs = np.array([0.22,
                       0.11,
                       0.1,
                       0.1,
                       0.13,
                       0.2,
                       0.12,
                       0.02
                       ])
    
    #Value of Portfolio with no optimization
    naivePortfolio = SRO.SharpeRatioOptimizer()
    naivePortfolio.getPortStats(allocs, prices, sf=12, sv=10000)
    
    print '---No Opt---\n'
    print 'Cumulative Return: ', naivePortfolio.cr, '\n'
    print 'Avg Period Return: ', naivePortfolio.apr, '\n'
    print 'STD Period Return: ', naivePortfolio.sdpr, '\n'
    print 'Sharpe Ratio: ', naivePortfolio.sr, '\n'
    print 'Port Value: ', naivePortfolio.port_val, '\n'
    
    naive = naivePortfolio.port_val[-1]
    
    #Value With Optimization for CR
    optPortCR = naivePortfolio.optimize_cr(prices, sf=12)
    naivePortfolio.getPortStats(optPortCR, prices, sf=12, sv=10000)

    print '---CR Opt---\n'
    print 'Cumulative Return: ', naivePortfolio.cr, '\n'
    print 'Avg Period Return: ', naivePortfolio.apr, '\n'
    print 'STD Period Return: ', naivePortfolio.sdpr, '\n'
    print 'Sharpe Ratio: ', naivePortfolio.sr, '\n'
    print 'Port Value: ', naivePortfolio.port_val, '\n'
    print np.round(optPortCR, decimals=2)
    print '\n'
    
    optimalCR = naivePortfolio.port_val[-1]
    
    #Value With Optimization for Sharpe
    optPortSharpe = naivePortfolio.optimize_sharpe(prices, sf=12)
    naivePortfolio.getPortStats(optPortSharpe, prices, sf=12, sv=10000)

    print '---Sharpe Opt---\n'
    print 'Cumulative Return: ', naivePortfolio.cr, '\n'
    print 'Avg Period Return: ', naivePortfolio.apr, '\n'
    print 'STD Period Return: ', naivePortfolio.sdpr, '\n'
    print 'Sharpe Ratio: ', naivePortfolio.sr, '\n'
    print 'Port Value: ', naivePortfolio.port_val, '\n'
    print np.round(optPortSharpe, decimals=2)
    print '\n'
    
    optimalSharpe = naivePortfolio.port_val[-1]