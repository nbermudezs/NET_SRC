__author__ = "Nestor Bermudez"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "nab6@illinois.edu"
__status__ = "Development"


import datetime as dt
import os
import pandas as pd


DATE_FORMAT = "%Y-%m-%d"


def RPI_vs_all_over_time(start_date, root):
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
        df = df.drop('RPI', axis=1)
        values = df.loc['RPI']
        values.name = day
        result.append(values)
    return pd.concat(result, axis=1)


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import seaborn as sns
    import sys

    sns.set_palette('dark')

    plt.style.use('seaborn-white')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['figure.dpi'] = 300

    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = 'tmp'

    start_date = dt.date(year=2018, month=12, day=20)
    result = RPI_vs_all_over_time(start_date, root=root)

    fig = plt.subplot()
    result.T.plot(kind='line', y='Sagarin_RK', color='black', marker='+', label='Sagarin', ax=fig)
    result.T.plot(kind='line', y='Pomeroy_RK', color='black', marker='^', label='KenPom', ax=fig)
    result.T.plot(kind='line', y='BPI_RK', color='black', marker='o', label='BPI', ax=fig)
    plt.ylabel('SRC coefficient w.r.t. RPI')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())
    plt.legend(fancybox=True)
    plt.savefig(root + '/rpi_trend_{}_to_{}'.format(
        start_date.strftime(DATE_FORMAT),
        dt.date.today().strftime(DATE_FORMAT)))