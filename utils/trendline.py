__author__ = "Nestor Bermudez"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "nab6@illinois.edu"
__status__ = "Development"


import datetime as dt
import os
import pandas as pd


DATE_FORMAT = "%Y-%m-%d"


def NET_vs_all_over_time(start_date, root):
    days = (dt.date.today() - start_date).days + 1

    x = []
    result = []
    for i in range(days):
        day = start_date + dt.timedelta(days=i)
        filepath = '{0}/correlation_{1}.csv'.format(
            root, day.strftime(DATE_FORMAT))
        if not os.path.exists(filepath):
            continue
        x.append(day)
        df = pd.read_csv(filepath, index_col=0)
        df = df.drop('NET Rank', axis=1)
        values = df.loc['NET Rank']
        values.name = day
        result.append(values)
    return pd.concat(result, axis=1)


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import sys

    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = 'tmp'

    start_date = dt.date.today() - dt.timedelta(days=14)
    result = NET_vs_all_over_time(start_date, root=root)
    result.T.plot.line()
    plt.ylabel('SRC coefficient with NET rank')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.savefig(root + '/trend_{}_to_{}'.format(
        start_date.strftime(DATE_FORMAT),
        dt.date.today().strftime(DATE_FORMAT)))