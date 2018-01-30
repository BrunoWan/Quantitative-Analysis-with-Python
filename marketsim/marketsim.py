"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
   
    port_data=pd.read_csv(orders_file)
    port_data['Date']=pd.to_datetime(port_data.Date, format='%Y-%m-%d')
    port_data['Commission']=commission
    port_data['Impact']=port_data['Shares']*impact
    port_data.loc[port_data['Order']=='BUY', 'ABS_Shares']=1*port_data['Shares']
    port_data.loc[port_data['Order'] == 'SELL', 'ABS_Shares'] = -1 * port_data['Shares']

    sd=port_data.iloc[0,0].date()
    ed=port_data.iloc[-1,0].date()
    dates=pd.date_range(sd,ed)
    syms=port_data.Symbol.unique().tolist()
    prices_all=get_data(syms, dates)

    matrix_shares=port_data.pivot_table(index="Date", columns="Symbol", values="ABS_Shares", aggfunc="sum")
    matrix_f_shares=matrix_shares.reindex(dates,fill_value=0).fillna(0)
    matrix_commission=port_data.pivot_table(index="Date", columns="Symbol", values="Commission", aggfunc="sum")
    matrix_f_commission = matrix_commission.reindex(dates, fill_value=0).fillna(0)
    matrix_impact = port_data.pivot_table(index="Date", columns="Symbol", values="Impact", aggfunc="sum")
    matrix_f_impact = matrix_impact.reindex(dates, fill_value=0).fillna(0)

    matrix_prices=prices_all.iloc[:,1:]
    matrix_c_impact=matrix_prices*matrix_f_impact
    matrix_c_shares=matrix_prices*matrix_f_shares
    matrix_c_commission=matrix_f_commission
    matrix_c_port=(matrix_c_impact+matrix_c_shares+matrix_c_commission).sum(axis=1).cumsum(axis=0).to_frame()
    matrix_v_stock=(matrix_f_shares.cumsum(axis=0)*matrix_prices).sum(axis=1).to_frame()
    matrix_v_cash=start_val-matrix_c_port
    matrix_v_port=prices_all.join(matrix_v_stock+matrix_v_cash,how='left',lsuffix='_x').iloc[:,-1].to_frame()




    portvals=matrix_v_port
    return portvals


def author():
    return 'ywan43'

def test_code():

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
