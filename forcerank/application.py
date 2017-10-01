
"""This is the main module for the Force Rank Application.

This module abstracts the application into a class. Note that the program
contains filenames that are hard-coded. Update as required.
"""

from pandas import ExcelWriter

from forcerank.sourceoftruth import SOTCreator
from forcerank.rank import Ranker


class Application():

    def __init__(self, input_filename, output_filename, ma_window,
                 high_window, period, num_periods):
        self.input_file = input_filename
        self.output_file = output_filename
        self.ma_window = ma_window
        self.high_window = high_window
        self.period = period
        self.num_periods = num_periods
        self.db_path = ('/Users/Dan/Coding/Finance/projects/' +
                        'downloadstock/data/databases/')

    def run(self):
        sot = SOTCreator(self.input_file, self.ma_window, self.high_window,
                         self.db_path)
        sot.build()
        # print(sot.df_sot)

        rankings = Ranker(self.input_file, self.ma_window, self.high_window,
                          self.period, self.num_periods, sot.df_sot)
        rankings.rank()
        # print(rankings.df_rank)

        writer = ExcelWriter(self.output_file)
        rankings.df_rank.to_excel(writer, 'Sheet1')
        writer.save()
        print('Ranking complete! Excel file: {}'.format(self.output_file))
