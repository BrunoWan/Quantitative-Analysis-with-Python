"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo


def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices_all = prices_all.fillna(method='backfill')
    prices_all = prices_all.fillna(method='ffill')
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    rfr=0.0
    sf=252.0
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    arg_num=len(prices.columns)
    allocs =np.asarray(arg_num*[1/float(arg_num)])# add code here to find the allocations
    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    #arg_num=len(prices.columns)
    def con(x):
        return float(sum(x))-1.0
    cons=({'type':'eq','fun': con})
    bnds=arg_num*[(0.0,1.0)]

    min_result=spo.minimize(lambda x: prices.div(prices.iloc[0]).multiply(x).sum(axis=1).pct_change().std(), allocs, method='SLSQP', bounds=bnds, constraints=cons)
    allocs=min_result.x
    prices_test=prices.div(prices.iloc[0])
    prices_test1=prices_test.multiply(allocs)    
    port_val=prices_test1.sum(axis=1)
    cr=port_val.iloc[-1]/port_val.iloc[0]-1
    daily_ret=port_val.pct_change()
    adr=daily_ret.mean()
    sddr=daily_ret.std()
    daily_rfr=rfr
    sharp_ratio= (daily_ret.sub(daily_rfr)).mean()/((daily_ret.sub(daily_rfr)).std())
    sr=sharp_ratio*np.power(sf,1.0/2.0)
    # Get daily portfolio value
    #port_val = prices_SPY # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        #df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        prices_SPY_test=prices_SPY.div(prices_SPY.iloc[0])
        plot_prices=pd.DataFrame(prices_test.multiply(allocs).sum(axis=1)).join(pd.DataFrame(prices_SPY_test)).rename(columns={0:'PORTFOLIO'})
        plot_data(plot_prices)
        pass

    return allocs, cr, adr, sddr, sr

def test_code():
    

    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":

    test_code()
