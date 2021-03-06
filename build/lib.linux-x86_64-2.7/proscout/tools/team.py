import urllib2
from bs4 import BeautifulSoup
from collections import defaultdict
import numpy as np
import pandas as pd
from bs4 import SoupStrainer

team_codes = {'diamondbacks': 'ARI',
              'braves': 'ATL',
              'orioles' : 'BAL',
              'red socks': 'BOS',
              'cubs': 'CHC',
              'white sox': 'CHW',
              'reds': 'CIN',
              'indians':'CLE',
              'rockies':'COL',
              'tigers': 'DET',
              'astros': 'HOU',
              'royals': 'KCR',
              'angels': 'LAA',
              'dodgers': 'LAD',
              'marlins': 'MIA',
              'brewers': 'MIL',
              'twins': 'MIN',
              'mets': 'NYM',
              'yankees': 'NYY',
              'athletics' : 'OAK',
              'phillies': 'PHI',
              'pirates': 'PIT',
              'padres': 'SDP',
              'giants': 'SFG',
              'mariners': 'SEA',
              'cardinals' : 'STL',
              'rays' : 'TBR',
              'rangers': 'TEX',
              'blue jays': 'TOR',
              'nationals' : 'WSN'}
              
              

class Team(object):
    def __init__(self, city, name, year=2014):
        self.city = city
        self.name = name.lower()
        #self.lineups = self.team_url +  str(year) + '-batting-orders.shtml'
        self.team_url = r'http://www.baseball-reference.com/teams/' + team_codes[self.name] +'/' + str(year) +'.shtml'
        

    def get_team_batting(self):
        page = urllib2.urlopen(self.team_url)
        soup = BeautifulSoup(page.read(), parse_only = SoupStrainer('table'))
        all_tables = soup.find_all('table')
        table = all_tables[1]
        rows = table.find_all('tr')
        all_rows = []
        columns = ['Pos', 'Name', 'Age', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI',
                       'SB', 'CS', 'BB']
        for col in rows:
            rowvals = []
            dta = col.find_all('td')
            for d in dta[1:16]:
                rowvals.append(d.text.split('*')[0])
            if len(rowvals) ==15:
                all_rows.append(rowvals)
        df = pd.DataFrame(all_rows, columns=columns)
        df= df.convert_objects(convert_numeric=True)
        df['1B'] = df['H'] - (df['2B'] + df['3B'] + df['HR'])
        df = df[df['Pos'] != '']
        return df

if __name__ == '__main__':
    dodgers = Team('Los Angeles', 'Dodgers')
