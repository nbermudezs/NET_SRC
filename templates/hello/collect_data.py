__author__ = "Nestor Bermudez"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "nab6@illinois.edu"
__status__ = "Development"


import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns
import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


YEAR = int(os.environ.get('YEAR', '2019'))
N_TEAMS = int(os.environ.get('N_TEAMS', '353'))


# template:
# pos 0: year
# pos 1: metric type (rpi-predict, rpi-live, rpi-live2, net)
warren_nolan_base_url = 'http://warrennolan.com/basketball/{}/{}'

# template
# pos 0: year
espn_base_url = 'http://www.espn.com/mens-college-basketball/bpi/_/view/bpi/season/{}/page/{}'

# template
# pos 0: year
pomeroy_base_url = 'https://kenpom.com/index.php?y={}'


ncaa_base_url = 'https://www.ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings'

# template
# pos 0: year
sagarin_base_url = 'https://www.usatoday.com/sports/ncaab/sagarin/{}/team/'

def cleanup_warren_nolan_data(data):
    team = data[0]
    pos = team.rfind('\n')
    if pos > 0:
        team = team[:team.rfind('\n')].replace('\n', '')
    else:
        team = team.replace('\n', '')
    data[0] = str(team)
    return data


name_map = {
    'Alabama St.': 'Alabama State',
    'Albany-NY': 'Albany',
    'Albany (NY)': 'Albany',
    'Alcorn St.': 'Alcorn State',
    'Alcorn': 'Alcorn State',
    'American U.': 'American',
    'Appalachian St.': 'Appalachian State',
    'Arizona St.': 'Arizona State',
    'Arkansas Pine Bluff': 'Arkansas-Pine Bluff',
    'Ark.-Pine Bluff': 'Arkansas-Pine Bluff',
    'Arkansas St.': 'Arkansas State',
    'Army West Point': 'Army',
    'A&M-Corpus Christi': 'Texas A&M-Corpus Christi',
    'Ball St.': 'Ball State',
    'Bethune Cookman': 'Bethune-Cookman',
    'Binghamton-NY': 'Binghamton',
    'Boise St.': 'Boise State',
    'Boston U.': 'Boston University',
    'CS Bakersfield': 'Cal State Bakersfield',
    'CSU Bakersfield': 'Cal State Bakersfield',
    'Cal St. Bakersfield': 'Cal State Bakersfield',
    'Call State Bakersfield': 'Cal State Bakersfield',
    'CS Fullerton': 'Cal State Fullerton',
    'CSU Fullerton': 'Cal State Fullerton',
    'Cal St. Fullerton': 'Cal State Fullerton',
    'CS Northridge': 'Cal State Northridge',
    'CSU Northridge': 'Cal State Northridge',
    'Cal St. Northridge': 'Cal State Northridge',
    'Call State Northridge': 'Cal State Northridge',
    'Cal Baptist': 'California Baptist',
    'Cal Poly-SLO': 'Cal Poly',
    'Central Ark.': 'Central Arkansas',
    'Central Connecticut St.': 'Central Connecticut',
    'Central Connecticut State': 'Central Connecticut',
    'Central Conn. State': 'Central Connecticut',
    'Central Florida(UCF)': 'UCF',
    'Central Mich.': 'Central Michigan',
    'Charleston So.': 'Charleston Southern',
    'Chicago St.': 'Chicago State',
    'Cleveland St.': 'Cleveland State',
    'Coastal Caro.': 'Coastal Carolina',
    'College of Charleston': 'Charleston',
    'Col. of Charleston': 'Charleston',
    'Colorado St.': 'Colorado State',
    'Coppin St.': 'Coppin State',
    'CSUN': 'Cal State Northridge',
    'Delaware St.': 'Delaware State',
    'Detroit Mercy': 'Detroit',
    'East Tennessee St.': 'East Tennessee State',
    'East Tennessee State(ETS': 'East Tennessee State',
    'Eastern Ky.': 'Eastern Kentucky',
    'Eastern Ill.': 'Eastern Illinois',
    'Eastern Mich.': 'Eastern Michigan',
    'Eastern Wash.': 'Eastern Washington',
    'ETSU': 'East Tennessee State',
    'Florida Atlantic': 'FAU',
    'Fla. Atlantic': 'FAU',
    'Florida Gulf Coast': 'FGCU',
    'Florida International': 'FIU',
    'Fla. International': 'FIU',
    'Florida St.': 'Florida State',
    'Fort Wayne(PFW)': 'Purdue Fort Wayne',
    'Fresno St.': 'Fresno State',
    'Gardner Webb': 'Gardner-Webb',
    'Georgia St.': 'Georgia State',
    'Ga. Southern': 'Georgia Southern',
    'Grambling St.': 'Grambling',
    'Grambling State': 'Grambling',
    "Hawai'i": 'Hawaii',
    'Idaho St.': 'Idaho State',
    'Illinois Chicago': 'UIC',
    'Illinois-Chicago': 'UIC',
    'Iona College': 'Iona',
    'Kansas City(UMKC)': 'UMKC',
    'La.-Monroe': 'ULM',
    'Lamar University': 'Lamar',
    'LIU Brooklyn': 'Long Island',
    'Long Island U.(LIU)': 'Long Island',
    'Louisiana Monroe': 'ULM',
    'Loyola Chicago': 'Loyola-Chicago',
    'Loyola Marymount': 'Loyola-Marymount',
    'Loyola MD': 'Loyola-Maryland',
    'Loyola (MD)': 'Loyola-Maryland',
    'Loyola Maryland': 'Loyola-Maryland',
    'MVSU(Miss. Valley State)': 'Mississippi Valley State',
    'McNeese': 'McNeese State',
    'Maryland-Eastern Shore': 'Maryland Eastern Shore',
    'Massachusetts': 'UMass',
    'Md.-Eastern Shore(UMES)': 'Maryland Eastern Shore',
    'Miami FL': 'Miami (FL)',
    'Miami-Florida': 'Miami (FL)',
    'Miami': 'Miami (FL)',
    'Miami-Ohio': 'Miami (OH)',
    'Miami OH': 'Miami (OH)',
    'Middle Tenn.': 'Middle Tennessee',
    'Mississippi': 'Ole Miss',
    u'MVSU(Miss. Valley State)': 'Mississippi Valley State',
    'Mississippi Val.': 'Mississippi Valley State',
    'Monmouth-NJ': 'Monmouth',
    u'Mount State Mary\'s': "Mount Saint Mary's",
    u'Mt. State Mary\'s': "Mount Saint Mary's",
    'NJIT(New Jersey Tech)': 'NJIT',
    'Nebraska Omaha': 'Omaha',
    'NC A&T': 'North Carolina A&T',
    'NC Asheville': 'UNC Asheville',
    'NC Wilmington': 'UNCW',
    'NC Central': 'North Carolina Central',
    'N.C. Central': 'North Carolina Central',
    'NC Greensboro': 'UNCG',
    'NC State': 'North Carolina State',
    'N.C. State': 'North Carolina State',
    'N.C. A&T': 'North Carolina A&T',
    'Nicholls': 'Nicholls State',
    'North Florida(UNF)': 'North Florida',
    'North Ala.': 'North Alabama',
    'Northern Ariz.': 'Northern Arizona',
    'Northern Colo.': 'Northern Colorado',
    'Northern Ky.': 'Northern Kentucky',
    'Northern Ill.': 'Northern Illinois',
    'Oakland-Mich.': 'Oakland',
    'Omaha(Neb.-Omaha)': 'Omaha',
    'Pennsylvania': 'Penn',
    'Prairie View': 'Prairie View A&M',
    'Presbyterian': 'Presbyterian College',
    'SC State': 'South Carolina State',
    'SE Missouri State(SEMO)': 'Southeast Missouri',
    'Se Missouri St': 'Southeast Missouri',
    'St. Bonaventura': 'Saint Bonaventure',
    'St Bonaventura': 'Saint Bonaventure',
    'St. Bonaventure': 'Saint Bonaventure',
    u'San Jos\xe9 St': 'San Jose State',
    'St. Francis (PA)': 'Saint Francis (PA)',
    'St. Francis PA': 'Saint Francis (PA)',
    'Saint Francis-Pa.': 'Saint Francis (PA)',
    'St. Francis-NY': 'Saint Francis (NY)',
    'St. Francis NY': 'Saint Francis (NY)',
    'St. Francis (BKN)': 'Saint Francis (NY)',
    'St. Francis Brooklyn': 'Saint Francis (NY)',
    "Saint Joseph's-Pa.": "Saint Joseph's",
    "Saint Mary's-Cal.": "Saint Mary's College",
    "Saint Mary's": "Saint Mary's College",
    "Saint Mary's (CA)": "Saint Mary's College",
    'Seattle': 'Seattle University',
    'Seattle U': 'Seattle University',
    'SIU-Edwardsville': 'SIUE',
    'SIU Edwardsville': 'SIUE',
    'South Fla.': 'South Florida',
    'Southern U.': 'Southern',
    'Southern California': 'USC',
    'Southern Ill.': 'Southern Illinois',
    'Southern Miss.': 'Southern Miss',
    'Southeast Mo. State': 'Southeast Missouri',
    'Southeast Missouri State': 'Southeast Missouri',
    'Southeast Missouri St.': 'Southeast Missouri',
    'Southeastern La.': 'Southeastern Louisiana',
    'SE Missouri St': 'Southeast Missouri',
    'SE Louisiana': 'Southeastern Louisiana',
    'SFA': 'Stephen F. Austin',
    'Stony Brook-NY': 'Stony Brook',
    "St. John's": "Saint John's",
    "St. John's (NY)": "Saint John's",
    'Texas San Antonio': 'UTSA',
    'Texas A&M-CorpusChristi': 'Texas A&M-Corpus Christi',
    'Texas A&M Corpus Chris': 'Texas A&M-Corpus Christi',
    'Texas A&M-CC': 'Texas A&M-Corpus Christi',
    'UConn': 'Connecticut',
    'UL Monroe': 'ULM',
    'UMass Lowell': 'UMass-Lowell',
    'UMES': 'Maryland Eastern Shore',
    'UNC Greensboro': 'UNCG',
    'UNC Wilmington': 'UNCW',
    'UNI': 'Northern Iowa',
    'USC Upstate': 'South Carolina Upstate',
    'UT Rio Grande Valley': 'UTRGV',
    'UT Arlington': 'UTA',
    'UT Martin': 'Tennessee-Martin',
    'Tennessee Martin': 'Tennessee-Martin',
    'VCU(Va. Commonwealth)': 'VCU',
    'Western Ky.': 'Western Kentucky',
    'Western Ill.': 'Western Illinois',
    'Western Mich.': 'Western Michigan',
    'Western Caro.': 'Western Carolina',
    'Xavier-Ohio': 'Xavier'
}
def cleanup_team_name(name):
    if ' St.' in name:
        name = name.replace(' St.', ' State')
    if name in name_map:
        return name_map[name]
    return name


def warren_nolan_html_to_df(year, metric, cols, col_offset=0):
    results = []
    header = None
    href = warren_nolan_base_url.format(year, metric)
    print(href)
    soup = BeautifulSoup(urlopen(href), 'lxml')
    table = soup.find('div', class_='datatable').find('table')
    for row in table.find_all('tr'):
        if row.find('th'):
            if len(results) == 0:
                header = ['Year'] + [
                    x.get_text().replace('\n', '').strip()
                    for i, x in enumerate(row.find_all('th'))
                    if i >= col_offset]
            continue
        data = [col.get_text() for i, col in enumerate(row.find_all('td')) if i >= col_offset]
        data = cleanup_warren_nolan_data(data)
        results.append([str(year)] + data)

    df = pd.DataFrame.from_records(results, columns=header)
    return df[cols].set_index('Team')


def collect_net(year):
    req = Request(ncaa_base_url, headers={'User-Agent': 'Mozilla/5.0'})
    results = []
    print(ncaa_base_url)
    soup = BeautifulSoup(urlopen(req), 'lxml')
    table = soup.find('article', class_='rankings-content').find('table')
    for row in table.find_all('tr'):
        if row.find('th'):
            continue
        data = [col.get_text() for i, col in enumerate(row.find_all('td')) if i in [0, 2]]
        data[1] = cleanup_team_name(data[1])
        results.append([str(year)] + data)
    df = pd.DataFrame.from_records(results, columns=['Year', 'NET Rank', 'Team'])
    return df.set_index('Team')


def collect_from_warren_nolan():
    # net = warren_nolan_html_to_df(YEAR, 'net', ['Year', 'Team', 'NET Rank'], col_offset=1)
    rpi = warren_nolan_html_to_df(YEAR, 'rpi-live', ['Year', 'Team', 'RPI'], col_offset=2)
    return rpi
    # return pd.concat([rpi, net], axis=1).T.drop_duplicates().T


def collection_from_espn():
    results = []
    header = ['Year', 'BPI_RK', 'Team', 'BPI', 'Conf']
    href = espn_base_url.format(YEAR, 1)
    print(href)
    soup = BeautifulSoup(urlopen(href), 'lxml')
    li = soup.find('ul', class_='pagination').find_all('li')
    if len(li) > 0:
        # last one is the next button
        pages = int(li[-2].get_text())
    else:
        pages = 1

    teams = set()
    while len(teams) != N_TEAMS:
        print(len(teams))
        for page in range(1, pages + 1):
            href = espn_base_url.format(YEAR, page)
            soup = BeautifulSoup(urlopen(href), 'lxml')
            if page == 1:
                print('Last updated ', soup.find('span', class_='bpi__updateTime').get('data-date'))
                print('=' * 80)
            print('page: ', page)
            table = soup.find('table', class_='bpi__table')
            for row in table.find('tbody').find_all('tr'):
                rk = row.find_all('td')[0].get_text()
                team = cleanup_team_name(row.find_all('td')[1].find('span', class_='team-names').get_text())
                conf = row.find_all('td')[2].get_text()
                if team in teams:
                    continue
                print(team, len(teams))
                teams.add(team)
                bpi = row.find_all('td')[6].get_text()
                results.append([YEAR, rk, team, bpi, conf])
    df = pd.DataFrame.from_records(results, columns=header)
    return df.set_index('Team').drop_duplicates()


def collect_from_pomeroy():
    results = []
    header = ['Year', 'Pomeroy_RK', 'Team']

    href = pomeroy_base_url.format(YEAR)
    soup = BeautifulSoup(urlopen(href), 'lxml')
    print(href)

    table = soup.find('table', id='ratings-table')
    for body in table.find_all('tbody'):
        for row in body.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 0:
                continue
            rk = cols[0].get_text()
            team = cleanup_team_name(cols[1].get_text())
            results.append([YEAR, rk, team])
    df = pd.DataFrame.from_records(results, columns=header)
    return df.set_index('Team').drop_duplicates()


def collect_from_sagarin():
    results = []
    header = ['Year', 'Sagarin_RK', 'Team']

    href = sagarin_base_url.format(YEAR)
    soup = BeautifulSoup(urlopen(href), 'lxml')
    print(href)

    table = soup.find('div', class_='sagarin-page')
    schools = table.find_all('br')
    for school in schools:
        school = school.nextSibling
        if (u' =' in str(school) or 'East Tennessee State' in str(school)) and u'__' not in str(school):
            name = re.search('[A-Z][^=]*', str(school)).group(0).strip()
            raw_name = name.replace('&amp;', '&')
            name = cleanup_team_name(raw_name)
            # import pdb; pdb.set_trace()
            rk = school.get_text().replace('&nbsp', '').replace(raw_name, '').replace('=', '').strip()
            results.append([YEAR, rk, name])
            if len(results) == N_TEAMS:
                # this is the number of teams in 2018-2019 season
                break
    df = pd.DataFrame.from_records(results, columns=header)
    return df.set_index('Team').drop_duplicates()


def collect_rankings():
    import numpy as np
    net_data = collect_net(YEAR)
    print(net_data.shape, np.unique(net_data.index).shape)
    sagarin_data = collect_from_sagarin()
    print(sagarin_data.shape, np.unique(sagarin_data.index).shape)
    pomeroy_data = collect_from_pomeroy()
    print(pomeroy_data.shape, np.unique(pomeroy_data.index).shape)
    bpi_data = collection_from_espn()
    print(set(sagarin_data.index) - set(bpi_data.index))
    print(bpi_data.shape, np.unique(bpi_data.index).shape)
    rpi_data = collect_from_warren_nolan()
    print(rpi_data.shape, np.unique(rpi_data.index).shape)

    all_df = pd.concat([sagarin_data, pomeroy_data, bpi_data, rpi_data, net_data], axis=1)
    all_df = all_df[['Year', 'Sagarin_RK', 'Pomeroy_RK', 'BPI_RK', 'RPI', 'NET Rank', 'Conf']]
    all_df = all_df.drop('Year', axis=1).astype({
        'Sagarin_RK': int,
        'Pomeroy_RK': int,
        'BPI_RK': int,
        'RPI': int,
        'NET Rank': int,
        'Conf': str
    })
    all_df['RPI - NET'] = all_df['RPI'] - all_df['NET Rank']
    all_df = all_df.sort_values(by='RPI - NET', ascending=True)

    return all_df


if __name__ == '__main__':
    all_df = collect_rankings()
    print(all_df.corr(method='spearman'))
    sns.pairplot(all_df,
                 vars=['Sagarin_RK', 'Pomeroy_RK', 'BPI_RK', 'RPI', 'NET Rank'])
    plt.savefig('comparison.png')
