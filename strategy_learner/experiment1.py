#############
#Implemented by
#Name: Yun Wan
#GTID: ywan43
#############


import ManualStrategy as ms
import StrategyLearner as sl
import pandas as pd
import numpy as np
import datetime as dt
import marketsimcode as mktsim


def testStrategy(symbol, sd, ed, sv=100000):
    # Set the symbol and the time period
    sd = sd
    ed = ed

    # Get the orders
    #############################################################
    sleanrer = sl.StrategyLearner()
    sleanrer.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    order_index = sleanrer.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    order_index = order_index[order_index.iloc[:, 0] != 0]
    order_index['Order'] = ''
    order_index.loc[order_index['Trade'] > 0, 'Order'] = 'BUY'
    order_index.loc[order_index['Trade'] < 0, 'Order'] = 'SELL'
    order_index['Shares'] = order_index.loc[:, 'Trade'].abs()
    order_index['Symbol'] = symbol
    order_index.reset_index(inplace=True)
    order_index = order_index.iloc[:, [0, 4, 2, 3]]
    order_index.columns = ['Date', 'Symbol', 'Order', 'Shares']
    df_trades=order_index
    ######################################################################

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
    ms.plot_data(pl_data, orders=orders)


if __name__ == '__main__':

   ms.testStrategy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
   testStrategy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)

