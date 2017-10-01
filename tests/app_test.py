
""" run 'pytest -v' at the command line in the main directory """

from datetime import date
import pytest

from forcerank.database import DatabaseManager
from forcerank.sourceoftruth import SOTCreator
from forcerank.rank import Ranker


class TestDatabaseModule():

    def test_database_manager(self):
        ticker = 'GLD'
        filename = ('/Users/Dan/Coding/Finance/projects/' +
                    'forcerank/data/test_data/{}.db').format(ticker)
        db = DatabaseManager(ticker, filename)
        db.read()
        test_date = date(2007, 5, 3)
        assert db.df.at[test_date, 'Close'] == 67.489998
        db.close()


class TestSourceOfTruthModule():

    def test_calculation_accuracy(self):
        input_filename = 'data/input/Test2.csv'
        ma_window = 200     # e.g. 50-Day Moving Average
        high_window = 252   # e.g. 50-Day High
        db_path = ('/Users/Dan/Coding/Finance/projects/' +
                   'forcerank/data/test_data/')
        sot = SOTCreator(input_filename, ma_window, high_window, db_path)
        sot.build()

        test_date = date(2009, 3, 31)
        SPY_close = sot.df_sot.loc[test_date]['SPY']
        SPY_MA = sot.df_sot.loc[test_date]['SPY 200-Day MA']
        SPY_MA_spread = sot.df_sot.loc[test_date]['SPY 200-Day MA Spread']
        SPY_high = sot.df_sot.loc[test_date]['SPY 252-Day High']
        SPY_high_spread = sot.df_sot.loc[test_date]['SPY 252-Day High Spread']

        assert SPY_close == pytest.approx(66.883247, 0.000001)
        assert SPY_MA == pytest.approx(83.88097428, 0.000001)
        assert SPY_high == pytest.approx(117.232109, 0.000001)
        assert SPY_MA_spread == pytest.approx((SPY_close - SPY_MA) /
                                              SPY_MA * 100, 0.000001)
        assert SPY_high_spread == pytest.approx((SPY_close - SPY_high) /
                                                SPY_high * 100, 0.000001)


class TestRankModule():

    def test_ranking_accuracy(self):
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

        XRT_high = rankings.df_rank.loc['XRT', 'Retail']['Abv 252d High']
        XRT_MA = rankings.df_rank.loc['XRT', 'Retail']['Abv 200d MA']
        XRT_MA_4 = rankings.df_rank.loc['XRT', 'Retail']['4Wk Ago']
        XRT_MA_8 = rankings.df_rank.loc['XRT', 'Retail']['8Wk Ago']
        XRT_MA_16 = rankings.df_rank.loc['XRT', 'Retail']['16Wk Ago']

        assert XRT_high == -11.9
        assert XRT_MA == 0.8
        assert XRT_MA_4 == -7.0
        assert XRT_MA_8 == -4.1
        assert XRT_MA_16 == -6.3
