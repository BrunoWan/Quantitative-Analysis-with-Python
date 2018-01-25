#############
#Implemented by
#Name: Yun Wan
#GTID: ywan43
#############


import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


class Indicators(object):

      def __init__(self):

          self.momentum=None
          self.sma =None
          self.blger_band=None
          self.prices_norm=None
          self.smap=None
          self.std=None
          self.blger_upband=None
          self.blger_lowband=None
          self.bbp=None
          self.df_momentum=None

      def author(self): return 'ywan43'

      def get_indicators(self, prices, window):

          self.prices_norm=prices/prices.iloc[0]
          self.momentum = prices.pct_change(periods=window)
          self.sma = self.prices_norm.rolling(window=window).mean()
          self.smap = self.prices_norm.div(self.sma) - 1
          self.std = self.prices_norm.rolling(window=window).std()
          self.blger_upband = self.sma + 2 * self.std
          self.blger_lowband = self.sma - 2 * self.std
          self.bbp = (self.prices_norm - self.blger_lowband) / (self.blger_upband - self.blger_lowband)

      def momentum(self, prices, window) :

          self.momentum=prices.pct_change(periods=window)


      def sma(self, prices, window):

          self.sma=self.prices_norm.rolling(window=window).mean()
          self.smap=self.prices_norm.div(self.sma)-1

      def blger_band(self, prices, window):

          self.std = self.prices_norm.rolling(window=window).std()
          self.blger_upband=self.sma+2*self.std
          self.blger_lowband = self.sma - 2 * self.std
          self.bbp=(self.prices_norm-self.blger_lowband)/(self.blger_upband-self.blger_lowband)


      def plot_indicators(self):
          self.df_momentum=pd.concat([self.prices_norm.iloc[:,1], self.momentum.iloc[:,1]], axis=1)
          self.df_momentum.columns=['Normalized price', 'Momentum']
          plot_data(self.df_momentum)

          self.df_sma = pd.concat([self.prices_norm.iloc[:,1], self.sma.iloc[:, 1], self.smap.iloc[:, 1]], axis=1)
          self.df_sma.columns=['Normalised price','Simple Moving Average(SMA)','SMAP']
          plot_data(self.df_sma)

          self.df_bbp = pd.concat([self.prices_norm.iloc[:, 1], self.sma.iloc[:, 1], self.blger_upband.iloc[:, 1], self.blger_lowband.iloc[:, 1], self.bbp.iloc[:, 1]], axis=1)
          self.df_bbp.columns = ['Normalized price', 'Simple Moving Average(SMA)', 'Bollinger Upper Band', 'Bollinger Lower Band','BBP']
          #plot_data(self.df_bbp.iloc[:,:-1])
          plot_data(self.df_bbp)

if __name__ == '__main__':

    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    syms = ['JPM']
    prices_all = get_data(syms, dates)
    indi = Indicators()
    indi.get_indicators(prices_all, 21)
    indi.plot_indicators()
    print __name__