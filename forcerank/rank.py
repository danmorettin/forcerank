
""" This module uses the source of truth data and creates a new dataframe
with the selected historical data. It then force ranks the data and shows
the historical rankings also. """

import pandas
from pandas import read_csv

from forcerank.sourceoftruth import SOTCreator


class Ranker():

    def __init__(self, input_filename, ma_window, high_window, period,
                 num_periods, df_sot):
        self.input_file = input_filename
        self.ma_window = ma_window
        self.high_window = high_window
        self.period = period
        self.num_periods = num_periods
        self.df_sot = df_sot

    def rank(self):
        """ Call the methods in the correct order. """
        self._create_ranking_table()
        self._populate_with_spreads_and_sort()
        self._populate_with_rankings()

    def _create_ranking_table(self):
        """ Reads in the desired ticker list as a pandas dataframe. Adds
        columns for the High and historical MAs, and initializes them with
        zeros. """
        self.df_rank = read_csv(self.input_file)
        self.df_rank['Abv {}d High'.format(self.high_window)] = 0
        self.df_rank['Abv {}d MA'.format(self.ma_window)] = 0

        for num in range(1, self.num_periods):
            self.df_rank['{}Wk Ago'.format(num * self.period)] = 0

    def _populate_with_spreads_and_sort(self):
        """ Copies in the selected data from the source of truth. Then sorts
        the data in descending order. """
        for index, row in self.df_rank.iterrows():
            col_name1 = 'Abv {}d High'.format(self.high_window)
            col_name2 = '{} {}-Day High Spread'.format(row['Ticker'],
                                                       self.high_window)

            self.df_rank.loc[index, col_name1] = (
                self.df_sot[col_name2][-1].round(1))
            col_name1 = 'Abv {}d MA'.format(self.ma_window)
            col_name2 = '{} {}-Day MA Spread'.format(row['Ticker'],
                                                     self.ma_window)

            self.df_rank.loc[index, col_name1] = (
                self.df_sot[col_name2][-1].round(1))
            col_name = '{} {}-Day MA Spread'.format(row['Ticker'],
                                                    self.ma_window)

            for num in range(1, self.num_periods):
                self.df_rank.loc[
                    index, '{}Wk Ago'.format(num * self.period)] = self.df_sot[
                        col_name][-(5 * num * self.period + 1)].round(1)

        self.df_rank = self.df_rank.sort_values(
            by='Abv {}d MA'.format(self.ma_window), ascending=False)
        self.df_rank.set_index(['Ticker', 'Description'], inplace=True)

    def _populate_with_rankings(self):
        """ Creates a numerical ranking 1, 2, 3, etc for each ticker. Then
        creates the historical ranking for each as well. """
        col_name1 = 'Abv {}d MA Rank'.format(self.ma_window)
        col_name2 = 'Abv {}d MA'.format(self.ma_window)
        self.df_rank[col_name1] = self.df_rank[col_name2].rank(
            ascending=False).astype(int)

        for num in range(1, self.num_periods):
            col_name1 = '{}Wk Ago Rank'.format(num * self.period)
            col_name2 = '{}Wk Ago'.format(num * self.period)
            self.df_rank[col_name1] = self.df_rank[col_name2].rank(
                ascending=False).astype(int)


def _test():
    input_filename = 'data/input/Sectors.csv'
    ma_window = 200     # e.g. 50-Day Moving Average
    high_window = 252   # e.g. 50-Day High
    period = 4          # e.g. every 4 weeks
    num_periods = 5     # e.g. 0, 4, 8, 12, 16
    db_path = ('/Users/Dan/Coding/Finance/projects/' +
               'forcerank/data/test_data/')
    sot = SOTCreator(input_filename, ma_window, high_window, db_path)
    sot.build()
    rankings = Ranker(input_filename, ma_window, high_window, period,
                      num_periods, sot.df_sot)
    rankings.rank()
    with pandas.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.width', 1000):
        # print(rankings.df_sot)
        print(rankings.df_rank)


if __name__ == "__main__":
    _test()
