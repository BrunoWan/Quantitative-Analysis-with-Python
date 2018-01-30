"""Analyze a portfolio."""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data


def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices_all = prices_all.fillna(method='backfill')
    prices_all = prices_all.fillna(method='ffill')
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    # add code here to compute daily portfolio values
    prices_test=prices.div(prices.iloc[0])
    prices_test1=prices_test.multiply(allocs)
    prices_test2=prices_test1.multiply(sv)
    port_val=prices_test2.sum(axis=1)
    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr=port_val.iloc[-1]/port_val.iloc[0]-1
    daily_ret=port_val.pct_change()
    adr=daily_ret.mean()
    sddr=daily_ret.std()
    daily_rfr=rfr
    sharp_ratio= (daily_ret.sub(daily_rfr)).mean()/((daily_ret.sub(daily_rfr)).std())
    sr=sharp_ratio*np.power(sf,1.0/2.0)
     # add code here to compute stats

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        
        prices_SPY_test=prices_SPY.div(prices_SPY.iloc[0])
        plot_prices=pd.DataFrame(prices_test.multiply(allocs).sum(axis=1)).join(pd.DataFrame(prices_SPY_test)).rename(columns={0:'PORTFOLIO'})  
        plot_data(plot_prices)
        
        pass

    # Add code here to properly compute end value
    ev = port_val.iloc[-1]

    return cr, adr, sddr, sr, ev

def test_code():

    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
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
