__author__ = "Nestor Bermudez"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "nab6@illinois.edu"
__status__ = "Development"


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
