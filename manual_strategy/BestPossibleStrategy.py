import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data
import marketsimcode as mktsim

def testPolicy(symbol ='JPM',sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):

    dates = pd.date_range(sd, ed)
    prices = get_data([symbol], dates)
    prices_norm = prices / prices.iloc[0]
    price_dir=prices_norm.pct_change()/(prices_norm.pct_change().abs())
    price_dir.iloc[0,:]=0.0
    price_dir=price_dir.fillna(method='ffill')
    long_date=price_dir.shift(-1)>price_dir
    short_date=price_dir.shift(-1)<price_dir
    price_order=price_dir.copy()
    price_order.iloc[:,:]=np.nan
    price_order.iloc[long_date.iloc[:,1].values,1]='BUY'
    price_order.iloc[short_date.iloc[:,1].values,1]='SELL'
    orders=price_order.dropna(how='all')
    orders.iloc[:,0]=symbol
    orders['Shares']=2000
    orders.iloc[0,2]=1000
    #orders.columns=['Symbol','Order','Shares']
    #Convert Index to column
    orders.reset_index(inplace=True)
    orders.columns = ['Date','Symbol', 'Order', 'Shares']
    return orders

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
    df_trades = testPolicy(symbol=symbol, sd=sd, ed=ed)

    # Get the portfolio value and the benchmark value
    matrix_v_port = mktsim.compute_portvals(df_trades, start_val=sv, commission=0.0, impact=0.0)[0]
    data_bench = df_trades.iloc[:1]
    data_bench.iloc[0, 2] = 'BUY'
    matrix_v_bench = mktsim.compute_portvals(data_bench, start_val=sv, commission=0.0, impact=0.0)[0]

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
    pl_data.columns = ['Best Possible Strategy', 'Benchmark']
    plot_data(pl_data)


if __name__ == '__main__':


    testStrategy(symbol ='JPM',sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000)

