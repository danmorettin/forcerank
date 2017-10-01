
"""This module builds the source of truth from the individual databases
and then computes the moving average, the local high, and the spreads of
each of those to the price."""

import pandas
from pandas import read_csv

from forcerank.database import DatabaseManager


class SOTCreator():

    def __init__(self, input_filename, ma_window, high_window, db_path):
        self.input_file = input_filename
        self.ma_window = ma_window
        self.high_window = high_window
        self.input_df = read_csv(self.input_file)
        self.db_path = db_path

    def build(self):
        self._build_dataframe_of_tickers()
        self._create_spreads()

    def _build_dataframe_of_tickers(self):
        for index, row in self.input_df.iterrows():
            ticker = row['Ticker']
            db_path = (self.db_path + '{}.db').format(ticker)
            db = DatabaseManager(ticker, db_path)
            db.read()
            df = db.df
            db.close()
            df = df.drop(['Open', 'Close', 'High', 'Low', 'Volume'], axis=1)
            df = df.rename(columns={'Adj Close': '{}'.format(ticker)})
            if index == 0:
                df_sot = df
            else:
                df_temp = df
                df_sot = df_sot.merge(df_temp,
                                      left_index=True,
                                      right_index=True,
                                      how='left')
        # Remove any NaN
        df_sot = df_sot.interpolate()
        self.df_sot = df_sot
        # print(self.df_sot)

    def _create_spreads(self):
        for index, row in self.input_df.iterrows():
            ticker = row['Ticker']
            met = Metrics(
                self.df_sot, ticker, self.ma_window, self.high_window)
            met.calculate_metrics()
            self.df_sot = met.df
        self.df_sot = self.df_sot.dropna(axis=0, how='any')
        # print(self.df_sot.loc[:, self.df_sot.columns.str.contains(
        #     'XME')].tail(10))


class Metrics():

    def __init__(self, df, ticker, ma_window, high_window):
        self.df = df.copy()
        self.ticker = ticker
        self.ma_window = ma_window
        self.high_window = high_window

    def calculate_metrics(self):
        self._create_moving_average()
        self._create_ma_spread_percent()
        self._create_local_high()
        self._create_high_spread_percent()

    def _create_moving_average(self):
        self.col_name_1 = '{} {}-Day MA'.format(self.ticker, self.ma_window)
        self.df[self.col_name_1] = self.df[self.ticker].rolling(
            window=self.ma_window).mean()

    def _create_ma_spread_percent(self):
        col_name_2 = '{} {}-Day MA Spread'.format(self.ticker, self.ma_window)
        self.df[col_name_2] = (
            (self.df[self.ticker] - self.df[self.col_name_1]) /
            self.df[self.col_name_1] * 100)

    def _create_local_high(self):
        self.col_name_3 = '{} {}-Day High'.format(self.ticker,
                                                  self.high_window)
        self.df[self.col_name_3] = self.df[self.ticker].rolling(
            window=self.high_window).max()

    def _create_high_spread_percent(self):
        col_name_4 = '{} {}-Day High Spread'.format(self.ticker,
                                                    self.high_window)
        self.df[col_name_4] = (
            (self.df[self.ticker] - self.df[self.col_name_3]) /
            self.df[self.col_name_3] * 100)


def _test():
    input_filename = 'data/input/Test.csv'
    ma_window = 200     # e.g. 50-Day Moving Average
    high_window = 252   # e.g. 50-Day High
    db_path = ('/Users/Dan/Coding/Finance/projects/' +
               'forcerank/data/test_data/')
    sot = SOTCreator(input_filename, ma_window, high_window, db_path)
    sot.build()
    with pandas.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.width', 1000):
        print(sot.df_sot)


if __name__ == "__main__":
    _test()
