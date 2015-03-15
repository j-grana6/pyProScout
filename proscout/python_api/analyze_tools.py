"""
This script will hold objects that have to do directly with analyzing
and presenting data.  No scraping functions are defined in this
script.
"""
from proscout.tools.player import Player
from proscout.tools.team import Team, team_codes
from matplotlib import pyplot as plt
import numpy as np

class TwoPlayerComparison(object):
    """
    Class to compare and plot performance of two players.
    Data is season totals from 2014 unless year parameter is specified
    """
    def __init__(self, player1, player2, year=2014):
        self.year=year
        self.player1 = Player(player1)
        self.player2 = Player(player2)
        
    def _get_player_data(self):
        p1data = self.player1.get_season_stats().loc[self.year]
        p2data = self.player2.get_season_stats().loc[self.year]
        return p1data, p2data

    def make_barchart(self):
        p1data, p2data = self._get_player_data()
        fig, axes = plt.subplots(2,2)
        fig.set_facecolor('#2C83A2')
        ax = axes[0][0]
        p1_interest = p1data[['1B', '2B', '3B', 'HR', 'SB', 'BB', 'RBI', 'G']]
        p2_interest = -1* p2data[['1B', '2B', '3B', 'HR', 'SB', 'BB',
            'RBI', 'G']]
        maxall = max(max(p1_interest), max(p2_interest))
        maxall = int(maxall/20 +1)*20
        p1 = ax.bar(np.arange(0,8), p1_interest, color='blue', alpha=.5)
        p2 = ax.bar(np.arange(0,8), p2_interest, color='green', alpha=.5)
        adv = ax.bar(np.arange(0,8), p1_interest+ p2_interest,
            color='black', alpha=.4) # BC ps is already negative
        ax.set_yticks(np.arange(-maxall, maxall+1, 20))
        ax.set_yticklabels([str(abs(int(x))) for x in
            ax.get_yticks()])
        ax.set_xticks(np.arange(.5,8.5, 1))
        ax.set_xticklabels(['1B', '2B', '3B', 'HR', 'SB', 'BB',
            'RBI', 'G'], fontsize=18)
        leg = ax.legend((p1[0], p2[0], adv[0]), (self.player1.name,
            self.player2.name, 'Advantage'), loc='upper center', ncol=3, fontsize=10)
        leg.get_frame().set_alpha(0.5)
        for rect in p1:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom', color='blue', alpha=1)
        for rect in p2:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., -1.05*height, '%d'%int(height),
                ha='center', va='top', color='green', alpha=1)
        ax.set_axis_bgcolor('black')
        ax.set_title('Comparison of '+ str(self.year)+ ' final stats',
            fontsize=18)

        # Second axis, per game basis
        ax = axes[0][1]
        p1_interest = p1data[['1B', '2B', '3B', 'HR', 'SB', 'BB', 'RBI']]/float(p1data[['AB']])
        p2_interest = -1* p2data[['1B', '2B', '3B', 'HR', 'SB', 'BB',
            'RBI']]/float(p2data[['AB']])
        maxall = max(max(p1_interest), max(p2_interest))
        maxall = int(maxall/20 +1)*20
        p1 = ax.bar(np.arange(0,7), p1_interest, color='blue', alpha=.5)
        p2 = ax.bar(np.arange(0,7), p2_interest, color='green', alpha=.5)
        adv = ax.bar(np.arange(0,7), p1_interest+ p2_interest,
            color='black', alpha=.4) # BC ps is already negative
        ax.set_yticks([-.5, -.4, -.3, -.2, -.1, 0, .1, .2, .3, .4, .5])
        ax.set_yticklabels([str(abs(float(x))) for x in
            ax.get_yticks()])
        ax.set_xticks(np.arange(.5,8.5, 1))
        ax.set_xticklabels(['1B', '2B', '3B', 'HR', 'SB', 'BB',
            'RBI'], fontsize=18)
        leg = ax.legend((p1[0], p2[0], adv[0]), (self.player1.name,
            self.player2.name, 'Advantage'), loc='upper center', ncol=3, fontsize=10)
        leg.get_frame().set_alpha(0.5)
        for rect in p1:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, str(height)[:5],
                ha='center', va='bottom', color='blue', alpha=1)
        for rect in p2:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., -1.05*height, str(height)[:5],
                ha='center', va='top', color='green', alpha=1)
        ax.set_axis_bgcolor('black')
        ax.set_title('Comparison of '+ str(self.year)+ ' final stats (per AB)',
            fontsize=18)


        # VS Righties
        ax = axes[1][0]
        p1_righties = self.player1.get_vs_righties()
        p2_righties = self.player2.get_vs_righties()
        p1_interest = np.asarray([float(p1_righties.sum()[x])/float(p1_righties.sum()['AB'])
                       for x in ['1B', '2B', '3B', 'HR', 'BB', 'RBI']])
        p2_interest = -1 * np.asarray([float(p2_righties.sum()[x])/float(p2_righties.sum()['AB'])
                        for x in ['1B', '2B', '3B', 'HR', 'BB', 'RBI']])
        maxall = max(max(p1_interest), max(p2_interest))
        maxall = int(maxall/20 +1)*20
        p1 = ax.bar(np.arange(0,6), p1_interest, color='blue', alpha=.5)
        p2 = ax.bar(np.arange(0,6), p2_interest, color='green', alpha=.5)
        adv = ax.bar(np.arange(0,6), p1_interest+ p2_interest,
            color='black', alpha=.4) # BC ps is already negative
        ax.set_yticks([-.5, -.4, -.3, -.2, -.1, 0, .1, .2, .3, .4, .5])
        ax.set_yticklabels([str(abs(float(x))) for x in
            ax.get_yticks()])
        ax.set_xticks(np.arange(.5,8.5, 1))
        ax.set_xticklabels(['1B', '2B', '3B', 'HR', 'BB',
            'RBI'], fontsize=18)
        leg = ax.legend((p1[0], p2[0], adv[0]), (self.player1.name,
            self.player2.name, 'Advantage'), loc='upper center', ncol=3, fontsize=10)
        leg.get_frame().set_alpha(0.5)
        for rect in p1:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, str(height)[:5],
                ha='center', va='bottom', color='blue', alpha=1)
        for rect in p2:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., -1.05*height, str(height)[:5],
                ha='center', va='top', color='green', alpha=1)
        ax.set_axis_bgcolor('black')
        ax.set_title('Comparison of Career stats (per AB) vs RHPs',
            fontsize=18)
        fig.set_size_inches(12,12)


        # VS Lefties
        ax = axes[1][1]
        p1_lefties = self.player1.get_vs_lefties()
        p2_lefties = self.player2.get_vs_lefties()
        p1_interest = np.asarray([float(p1_lefties.sum()[x])/float(p1_lefties.sum()['AB'])
                       for x in ['1B', '2B', '3B', 'HR', 'BB', 'RBI']])
        p2_interest = -1 * np.asarray([float(p2_lefties.sum()[x])/float(p2_lefties.sum()['AB'])
                        for x in ['1B', '2B', '3B', 'HR', 'BB', 'RBI']])
        maxall = max(max(p1_interest), max(p2_interest))
        maxall = int(maxall/20 +1)*20
        p1 = ax.bar(np.arange(0,6), p1_interest, color='blue', alpha=.5)
        p2 = ax.bar(np.arange(0,6), p2_interest, color='green', alpha=.5)
        adv = ax.bar(np.arange(0,6), p1_interest+ p2_interest,
            color='black', alpha=.4) # BC ps is already negative
        ax.set_yticks([-.5, -.4, -.3, -.2, -.1, 0, .1, .2, .3, .4, .5])
        ax.set_yticklabels([str(abs(float(x))) for x in
            ax.get_yticks()])
        ax.set_xticks(np.arange(.5,8.5, 1))
        ax.set_xticklabels(['1B', '2B', '3B', 'HR', 'BB',
            'RBI'], fontsize=18)
        leg = ax.legend((p1[0], p2[0], adv[0]), (self.player1.name,
            self.player2.name, 'Advantage'), loc='upper center', ncol=3, fontsize=10)
        leg.get_frame().set_alpha(0.5)
        for rect in p1:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, str(height)[:5],
                ha='center', va='bottom', color='blue', alpha=1)
        for rect in p2:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., -1.05*height, str(height)[:5],
                ha='center', va='top', color='green', alpha=1)
        ax.set_axis_bgcolor('black')
        ax.set_title('Comparison of Career stats (per AB) vs LHPs',
            fontsize=18)
        return fig, ax
        
def position_sensitivity(year=2014):
    """
    This only works for 2014 because of team names
    """
    df = None
    for key, val in team_codes.iteritems():
        if df is None:
            df = Team('any city', key).get_team_batting()
        else:
            team_line = Team('any city', key).get_team_batting()
            df = df.append(team_line, ignore_index=True)
    positions = ['1B', '2B', '3B', 'SS', 'C']
    cond = df['Pos']=='RF'
    df['Pos'][cond] = 'OF'
    cond = df['Pos']=='LF'
    df['Pos'][cond] = 'OF'
    cond = df['Pos']=='CF'
    df['Pos'][cond] = 'OF'
    df['fantasy'] = df['1B'] +2*df['2B'] + 3*df['3B'] +4*df['HR'] +df['R'] + df['RBI'] +df['SB']
    fig, ax = plt.subplots()
    colors = ['red', 'blue', 'green', 'purple', 'orange']
    i=0
    for p in positions:
        plot_data = df[df['Pos'] == p]['fantasy'].values
        plot_data.sort()
        ax.scatter(np.arange(0,len(plot_data)), plot_data[::-1]/float(plot_data[-1]), label = p, color=colors[i])
        ax.plot(np.arange(0,len(plot_data)), plot_data[::-1]/float(plot_data[-1]),  color=colors[i])
        ax.legend()
        i += 1
    return df

