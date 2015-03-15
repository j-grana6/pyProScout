"""
This scrip will provide an API for accessing player data.
Unfortunately, it will be developed based on demand and therefore  
poorly designed.  However, it will serve as a template for later
releases
"""
import urllib2
from bs4 import BeautifulSoup
from collections import defaultdict
import numpy as np
import pandas as pd
from bs4 import SoupStrainer

class Player(object):
    """
    Define methods and attributes here

    player_id : str
        The baseball_reference id for a player.  Last item in path
        to player page
    """
    def __init__(self, name, url=None):
        self.name=name
        self.first_name = name.split(" ")[0]
        self.last_name = name.split(" ")[1]
        self.url = url
        self.player_page, self.player_url = \
            self._get_br_mainpage(self.url)
        self.player_id = self.player_url.split('/')[-1].split('.')[0]
        
    def _get_br_mainpage(self, url):
        """
        Navigates to the BR player's page of the player.

        If there are multiple players of the same name, it picks the one that
        is currently active.  If neither of the player's are active, it will
        throw an error.

        This function also accepts a hand coded url as an optional argumen
        """
        if url is not None:
            return BeautifulSoup(urllib2.urlopen(url).read())
        url = (r'http://www.baseball-reference.com/players/' + \
               self.last_name[0].lower() + r'/')
        last_name_index = urllib2.urlopen(url)
        soup = BeautifulSoup(last_name_index.read())
        possible_matches = soup.find_all('a', href=True, text=self.name)
        if len(possible_matches) ==1:
            player_link = url + possible_matches[0]['href'].split('/')[-1]
            return BeautifulSoup(urllib2.urlopen(player_link).read()), player_link
        else:
            hrefs = [i['href'] for i in possible_matches]
            if len(set(hrefs)) ==1:
                player_link = url + possible_matches[0]['href'].split('/')[-1]
                return BeautifulSoup(urllib2.urlopen(player_link).read()), player_link
            for player in possible_matches:
                if player.parent.name == 'b':
                    player_link = url + player['href'].split('/')[-1]

        return BeautifulSoup(urllib2.urlopen(player_link).read()), player_link

    def get_season_stats(self):
        """
        Returns a pandas DF of season by season stats.

        Source is baseball reference batting standard

        """

        
        table =self.player_page.find_all(
            'table', id='batting_standard')[0]
        header = table.find_all('thead')[0].find_all('th')
        seasondata = defaultdict(list)
        table_rows =table.find('tbody').find_all('tr')
        for row in table_rows:
            if 'hidden' not in row['class']:
                entries = row.find_all('td')
                for ix in range(len(entries)):
                    if header[ix].string not in ['Tm', 'Lg', 'Pos', 'Awards']:
                        try:
                            seasondata[header[ix].string].append(float(entries[ix].strings.next()))
                        except StopIteration:
                            seasondata[header[ix].string].append(np.nan)

        df =  pd.DataFrame(seasondata)
        # Separate lines for different teams, want to concatenate
        for year in df['Year']:
            if len(df[df['Year']==year]) > 1:
                # Get the index to drop
                ix = df[df['Year'] ==year][ df[df['Year'] ==year]['AB']<max(df[df['Year'] ==year]['AB'])].index
                df.drop(ix, inplace=True)
        df['1B'] = df['H'] - df['2B'] - df['3B'] - df['HR']
        df = df.set_index('Year')
        return df

    def get_vs_righties(self):
        """
        Function that returns a dataframe of hitter vs pitcher.
        Also includes R and L
        """
        onlytables = SoupStrainer('table')
        vs_righties = ('http://www.baseball-reference.com/play-index'
            '/batter_vs_pitcher.cgi?batter=%s&min_year_game='
            '2001&max_year_game=2014&post=1&opp_id=&throws=R&opponent_status'
            '=&c1criteria=&c1gtlt=eq&c1val=0&c2criteria=&c2gtlt=eq&c2val=0&'
            'orderby=PA&orderby_dir=desc&orderby_second=Name&orderby_dir_second'
            '=asc&ajax=1&submitter=1&_=1') %(self.player_id)
        # To get the URL, had to go to network and see what is being requested
        page = urllib2.urlopen(vs_righties)
        righties_page = BeautifulSoup(page.read(), parse_only=onlytables)
        table = righties_page.find_all('table')[0]
        df = pd.read_html(table.prettify())[0]
        df = df.drop(df.columns[-1],1).convert_objects(
            convert_numeric=True).dropna()
        columns = [col.split('\n')[1].split(' ')[-1] for col in df.columns]
        df.columns = columns
        df['1B'] = df['H'] -(df['2B'] + df['3B'] + df['HR'])
        page.close()
        return df

    def get_vs_lefties(self):
        """
        Function that returns a dataframe of hitter vs pitcher.
        Also includes R and L
        """
        vs_lefties = ('http://www.baseball-reference.com/play-index'
            '/batter_vs_pitcher.cgi?batter=%s&min_year_game='
            '2001&max_year_game=2014&post=1&opp_id=&throws=L&opponent_status'
            '=&c1criteria=&c1gtlt=eq&c1val=0&c2criteria=&c2gtlt=eq&c2val=0&'
            'orderby=PA&orderby_dir=desc&orderby_second=Name&orderby_dir_second'
            '=asc&ajax=1&submitter=1&_=1') %(self.player_id)
        page = urllib2.urlopen(vs_lefties)
        lefties_page = BeautifulSoup(page.read())
        table = lefties_page.find_all('table')[0]
        df = pd.read_html(table.prettify())[0]
        df = df.drop(df.columns[-1],1).convert_objects(
            convert_numeric=True).dropna()
        columns = [col.split('\n')[1].split(' ')[-1] for col in df.columns]
        df.columns = columns
        df['1B'] = df['H'] -(df['2B'] + df['3B'] + df['HR'])
        page.close()
        return df
