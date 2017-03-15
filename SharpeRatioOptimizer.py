# -*- coding: utf-8 -*-
"""
Sharpe-Ratio Optimization

@author: Frank
"""

import pandas as pd
import numpy as np
import datetime as dt
import scipy.optimize as sco

class SharpeRatioOptimizer(object):
    # Constructor
    def __init__(self):
        pass
    
    
    # Portfolio Stats
    def getPortStats(self, allocs, prices, sf=252, rfr=0.0, sv=1):
        normed = self.normalize_data(prices)
        allocation = normed * allocs
        position_vals = allocation * sv
        self.port_val = position_vals.sum(axis=1)
        self.period_return = self.port_val.pct_change(1)
        self.period_return = self.period_return.ix[1:,]
        
        self.cr = (self.port_val.ix[-1]/self.port_val.ix[0]) - 1
        self.apr = self.period_return.mean()
        self.sdpr = self.period_return.std()
        
        # Sharpe Ratio  
        sr = ((self.period_return - rfr).mean()) / self.period_return.std()
        
        # Sharpe Ratio Adjustment
        k = sf**(1/2.0)
        self.sr = k*sr
        
        return self.cr, self.apr, self.sdpr, self.sr, self.port_val
    
    # Optimize on CR
    def optimize_cr(self, prices):
        # Initial allocation
        allocs = np.empty(len(prices.columns))
        allocs.fill(1.0/len(prices.columns))
        
        # constraints
        # Sum of weights = 1
        cons = ({'type': 'eq', 'fun' : lambda x: np.sum(x) - 1})
    
        # Bounds x between 0 and 1
        bnds = tuple((0,1) for x in range(len(allocs)))
        
        # Find Max Sharpe ratio
        opts = sco.minimize(self.max_cr, allocs, args=(prices,), method='SLSQP', 
                        constraints=cons, bounds=bnds)
        
        #Optimized allocations
        optAllocs = np.asarray(opts.x)
        
        return optAllocs
        
        
    # Optimize on Sharpe
    def optimize_sharpe(self, prices):
        # Initial allocation
        allocs = np.empty(len(prices.columns))
        allocs.fill(1.0/len(prices.columns))
        
        # constraints
        # Sum of weights = 1
        cons = ({'type': 'eq', 'fun' : lambda x: np.sum(x) - 1})
    
        # Bounds x between 0 and 1
        bnds = tuple((0,1) for x in range(len(allocs)))
        
        # Find Max Sharpe ratio
        opts = sco.minimize(self.max_sharpe, allocs, args=(prices,), method='SLSQP', 
                        constraints=cons, bounds=bnds)
        
        #Optimized allocations
        optAllocs = np.asarray(opts.x)
        
        return optAllocs


    def normalize_data(self, df):
        return df / df.ix[0, :]
    
    def max_cr(self, allocs, prices):
        return -self.getPortStats(allocs, prices,sf=12)[0]
        
    def max_sharpe(self, allocs, prices):
        return -self.getPortStats(allocs, prices, sf=12)[3]