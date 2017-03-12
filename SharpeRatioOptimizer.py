# -*- coding: utf-8 -*-
"""
Sharpe-Ratio Optimization

@author: Frank
"""

import pandas as pd
import matplotlib.pyplot as plt
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
        port_val = position_vals.sum(axis=1)
        daily_return = port_val.pct_change(1)
        daily_return = daily_return.ix[1:,]
        
        self.cr = (port_val.ix[-1]/port_val.ix[0]) - 1
        self.adr = daily_return.mean()
        self.sddr = daily_return.std()
        
        # Sharpe Ratio  
        sr = ((daily_return - rfr).mean()) / daily_return.std()
        
        # Sharpe Ratio Adjustment
        k = sf**(1/2.0)
        self.sr = k*sr
    
        return self.cr, self.adr, self.sddr, self.sr, self.daily_return, self.port_val


    def normalize_data(self, df):
        return df / df.ix[0, :]
        
    def max_sharpe(self, allocs, prices):
        return -self.getPortStats(allocs, prices)[3]