#############
#Implemented by
#Name: Yun Wan
#GTID: ywan43
#############

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data
from indicators import Indicators
import marketsimcode as mktsim

def testPolicy(symbol ='JPM',sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):

    dates = pd.date_range(sd, ed)
    prices = get_data([symbol], dates)
    prices_norm = prices / prices.iloc[0]
    indi = Indicators()
    indi.get_indicators(prices, 21)
    momentum=indi.momentum
    smap=indi.smap
    bbp=indi.bbp
    upper_limit=1000
    lower_limit=-1000
    prices['Holding']=0
    prices['Trade']=0

    for i in range(30, prices.shape[0]):
        # if  smap.iloc[i, 1] < -0.05 and bbp.iloc[i, 1] < 0:
        if momentum.iloc[i, 1] < 0 or smap.iloc[i, 1] < -0.05 and bbp.iloc[i, 1] < 0:
            prices.iloc[i, 3] = upper_limit - prices.iloc[i - 1, 2]

        elif momentum.iloc[i, 1] > 0 and smap.iloc[i, 1] > 0.05 and bbp.iloc[i, 1] > 1:
            # elif smap.iloc[i, 1] > 0.05 and bbp.iloc[i, 1] > 1:
            prices.iloc[i, 3] = lower_limit - prices.iloc[i - 1, 2]
        # prices.iloc[i, 2] = prices.iloc[i - 1, 2] + prices.iloc[i, 3]
        prices.iloc[i, 2] = prices.iloc[i - 1, 2] + prices.iloc[i, 3]

    price_order=prices.loc[prices.iloc[:, 3] != 0]
    price_order['Order']=''
    price_order.loc[price_order['Trade']>0,'Order']='BUY'
    price_order.loc[price_order['Trade']<0, 'Order'] = 'SELL'
    price_order['Shares']=price_order.loc[:,'Trade'].abs()
    price_order['Symbol']=symbol
    price_order.reset_index(inplace=True)
    price_order=price_order.iloc[:,[0,7,5,6]]
    price_order.columns = ['Date','Symbol', 'Order', 'Shares']
    return price_order

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price", orders=None):
    import matplotlib.pyplot as plt
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12, color=['black','b'])

    if orders is not None:
        ymin, ymax=ax.get_ylim()
        ax.vlines(x=orders.loc[orders.iloc[:,2]=='BUY',:].set_index('Date').index.values, ymin=ymin, ymax=ymax,color='g')
        ax.vlines(x=orders.loc[orders.iloc[:, 2] == 'SELL', :].set_index('Date').index.values, ymin=ymin, ymax=ymax,
                  color='r')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def testStrategy(symbol, sd, ed, sv=100000):
    # Set the symbol and the time period
    sd = sd
    ed = ed

    # Get the orders
    df_trades = testPolicy(symbol=symbol, sd=sd, ed=ed)

    # Get the portfolio value and the benchmark value
    matrix_v_port = mktsim.compute_portvals(df_trades, start_val=sv, commission=9.95, impact=0.005, sd=sd, ed=ed)[0]
    data_bench = df_trades.iloc[:1]
    data_bench.iloc[0, 2] = 'BUY'
    matrix_v_bench = mktsim.compute_portvals(data_bench, start_val=sv, commission=9.95, impact=0.005, sd=sd, ed=ed)[
        0]

    # Get the orders data for vertical lines
    orders = mktsim.compute_portvals(df_trades, start_val=sv, commission=9.95, impact=0.005, sd=sd, ed=ed)[1]

    # Get the statistics for the portfolio
    daily_ret = matrix_v_port.pct_change()
    adr = matrix_v_port.pct_change().mean()
    sddr = matrix_v_port.pct_change().std()
    cr = matrix_v_port.iloc[-1] / matrix_v_port.iloc[0] - 1

    # Get the statistics for the benchmark
    daily_ret_bench = matrix_v_bench.pct_change()
    adr_bench = matrix_v_bench.pct_change().mean()
    sddr_bench = matrix_v_bench.pct_change().std()
    cr_bench = matrix_v_bench.iloc[-1] / matrix_v_port.iloc[0] - 1

    # Get the normalized data for the two portfolios
    port_norm = matrix_v_port / matrix_v_port.iloc[0]
    bench_norm = matrix_v_bench / matrix_v_bench.iloc[0]

    print 'Cumulative return of the benchmark is ', cr_bench
    print 'Cumulative return of the portfolio is ', cr
    print 'Stdev of the daily return of the benchmark is ', sddr_bench
    print 'Stdev of the daily return of the portfolio is ', sddr
    print 'Mean of the daily return of the benchmark is ', adr_bench
    print 'Mean of the daily return of the portfolio is ', adr
    print 'The trading strategy is \n', df_trades
    pl_data = pd.concat([port_norm, bench_norm], axis=1)
    pl_data.columns = ['Manual Strategy', 'Benchmark']
    plot_data(pl_data, orders=orders)



if __name__ == '__main__':

    testStrategy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    testStrategy(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
