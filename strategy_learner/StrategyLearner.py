"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""
#############
#Implemented by
#Name: Yun Wan
#GTID: ywan43
#############

import datetime as dt
import pandas as pd
import util as ut
import random
import os
from util import get_data, plot_data
from indicators import Indicators
import numpy as np
#import DTLearner as dtl
import BagLearner as bgl


class StrategyLearner(object):
    # constructor
    def __init__(self, verbose=False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        ##########################################################
        self.learner = None
        self.buy_trigger = 0.05
        self.sell_trigger = -0.05
        self.order_threshold = 0.05
        self.indicator_window=21
        self.return_window=10
        ############################################################

    ################################################################################################
    def process(self, symbol="AAPL", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31) ):
        dates = pd.date_range(sd, ed)
        prices_all = get_data([symbol], dates)
        indi = Indicators()
        indi.get_indicators(prices_all, self.indicator_window)
        pd.concat([indi.momentum.iloc[:, 1], indi.smap.iloc[:, 1], indi.bbp.iloc[:, 1]], axis=1)
        prices_norm = prices_all / prices_all.iloc[0]
        on_coming_returns = prices_norm.iloc[:, 1].pct_change(periods=self.return_window).shift(-self.return_window).dropna(
            axis=0)
        on_coming_returns[on_coming_returns > self.order_threshold] = 1
        on_coming_returns[on_coming_returns < -self.order_threshold] = -1
        on_coming_returns[on_coming_returns.abs() <> 1] = 0
        data = pd.concat([indi.momentum.iloc[:, 1], indi.smap.iloc[:, 1], indi.bbp.iloc[:, 1], on_coming_returns],
                         axis=1).dropna(axis=0)
        data.columns = ['MOMENTUM', 'SMAP', 'BBP', 'ORDER']
        x = data.loc[:, ['MOMENTUM', 'SMAP', 'BBP']].values
        y = data.loc[:, ['ORDER']].values
        return data, x, y

    #######################################################################################################


    #######################################################################################################################
    def order_generate(self,prdct):

        order_index = prdct.loc[:, 'PRDCT'].to_frame()
        order_index['Holding'] = 0.0
        order_index['Trade'] = 0.0
        upper_limit = 1000
        lower_limit = -1000

        for i in range(1, order_index.shape[0]):
            if order_index.iloc[i, 0] > self.buy_trigger:
                order_index.iloc[i, 2] = upper_limit - order_index.iloc[i - 1, 1]
            elif order_index.iloc[i, 0] < self.sell_trigger:
                order_index.iloc[i, 2] = lower_limit - order_index.iloc[i - 1, 1]
            order_index.iloc[i, 1] = order_index.iloc[i - 1, 1] + order_index.iloc[i, 2]

        order_index = order_index.loc[:,'Trade'].to_frame()
        return order_index

    ###############################################################################################################################


    def addEvidence(self, symbol="IBM", \
                    sd=dt.datetime(2008, 1, 1), \
                    ed=dt.datetime(2009, 1, 1), \
                    sv=10000):
        #######################################################################################################
        train_data = self.process(symbol=symbol, sd=sd, ed=ed)
        train_x = train_data[1]
        train_y = train_data[2]
        self.learner = bgl.BagLearner(learner=bgl.DTLearner, kwargs={"leaf_size": 5}, bags=20, boost=False,
                                      verbose=False)
        self.learner.addEvidence(train_x, train_y)
        #####################################################################################


    def testPolicy(self, symbol="IBM", \
                   sd=dt.datetime(2009, 1, 1), \
                   ed=dt.datetime(2010, 1, 1), \
                   sv=10000):

        #######################################################################################################
        test_data = self.process(symbol=symbol, sd=sd, ed=ed)
        test_x = test_data[1]
        test_y = test_data[2]
        predicted_orders = self.learner.query(test_x)
        prdct_orders = pd.DataFrame(predicted_orders, index=test_data[0].index)
        prdct_orders.columns = ['PRDCT']
        trades = self.order_generate(prdct=prdct_orders)
        #######################################################################
        return trades


if __name__ == "__main__":
    print "One does not simply think up a strategy"
