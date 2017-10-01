
""" Choose the inputs and run the application as 'python bin/cli.py' """

from forcerank.application import Application

input_filename = 'data/input/Sectors.csv'
output_filename = 'data/output/ForceRankSectors.xlsx'
ma_window = 200     # e.g. 50-Day Moving Average
high_window = 252   # e.g. 50-Day High
period = 4          # e.g. every 4 weeks
num_periods = 10     # e.g. 0, 4, 8, 12, 16

app = Application(input_filename, output_filename, ma_window, high_window,
                  period, num_periods)
app.run()
