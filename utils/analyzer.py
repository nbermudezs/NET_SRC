__author__ = "Nestor Bermudez"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "nab6@illinois.edu"
__status__ = "Development"


import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


sns.set_palette('dark')
plt.style.use("seaborn-white")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 250


labels_map = {
    'Sagarin_RK': 'Sagarin',
    'Pomeroy_RK': 'KenPom',
    'BPI_RK': 'BPI',
    'RPI': 'RPI',
    'NET Rank': 'NET'
}


class Analyzer:
    def get_outliers(self, rankings, correlation):
        columns = rankings.columns

        results = {}
        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                label = '{} vs {}'.format(columns[i], columns[j])
                diff = rankings[columns[i]] - rankings[columns[j]]
                diff = diff.abs()
                mean = diff.values.mean()
                std = diff.values.std(ddof=1)
                selector = (diff > mean + 3 * std) | (diff < mean - 3 * std)
                outliers = diff[selector].index.tolist()
                results[label] = {}
                for outlier in outliers:
                    results[label][outlier] = {
                        columns[i]: int(rankings[columns[i]].loc[outlier]),
                        columns[j]: int(rankings[columns[j]].loc[outlier])
                    }
        return results

    def get_mean_diff(self, rankings):
        columns = rankings.columns

        results = {}
        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                label = '{} vs {}'.format(columns[i], columns[j])
                diff = rankings[columns[i]] - rankings[columns[j]]
                diff = diff.abs()

                results[label] = {
                    'mean': diff.values.mean().round(2),
                    'std': diff.values.std(ddof=1).round(2)
                }
        return results


    def save_diff_histograms(self, rankings, output):
        columns = rankings.columns

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                label = '{} vs {}'.format(labels_map[columns[i]],
                                          labels_map[columns[j]])
                diff = rankings[columns[i]] - rankings[columns[j]]
                diff = diff.abs()

                diff.groupby(diff).count().hist(bins=20, color='black')
                plt.title(label)
                plt.xlabel('Rank difference')
                plt.ylabel('# of teams')
                plt.savefig(output + '/diff-hist-' + label.replace(' ', '_') + '.png')
                plt.cla()
                plt.clf()
                # plt.show()

    def slopes(self, rankings):
        columns = rankings.columns

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                label = '{} vs {}'.format(labels_map[columns[i]],
                                          labels_map[columns[j]])
                model = LinearRegression()
                model.fit(rankings[columns[i]].values.reshape(-1, 1),
                          rankings[columns[j]].values.reshape(-1, 1))
                slope = model.coef_[0]
                print(label, slope, model.intercept_)


if __name__ == '__main__':
    import pandas as pd
    import sys
    from pprint import pprint

    rankings = pd.read_csv(sys.argv[1], index_col=0)
    analyzer = Analyzer()

    print(rankings.corr(method='spearman'))

    print('======= LR SLOPES ========')
    analyzer.slopes(rankings)

    diff = analyzer.get_mean_diff(rankings)
    print('======= AVG DIFF =======')
    pprint(diff)

    analyzer.save_diff_histograms(rankings, '~/cron/net_src')
