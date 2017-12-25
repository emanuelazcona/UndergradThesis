"""
	Emanuel Azcona
	Predicting NBA Playoff Contention Using Supervised Machine Learning Algorithms
"""

import pandas as pd
import numpy as np
import collections

def gen_data(start_season, end_season):
	players = collections.OrderedDict()
	teams = collections.OrderedDict()

	for i in range(start_season, end_season):
		# create the temporary string that allows us to repeat the process
		# of the dictionaries above but allows us to append these dictionaries
		# with new NBA seasons and their corresponding players and stats
		tempStr = str(i) + "-" + str(i+1)
		play_df = pd.read_excel("player info/players"\
						+ tempStr + ".xlsx",\
						header = 0)

		# Calculate the offensive rank of each player in the NBA season
		offRank = (play_df['PTS'] - (play_df['FGA'] - play_df['FGM'])\
				- ((play_df['FTA'] - play_df['FTM'])/2)\
				+ 1.25*play_df['AS'] + play_df['OR']\
				- 1.25*play_df['TO'] - play_df['TC']) / play_df['GP']

		play_df['OffRank'] = offRank

		# Calculate the defensive rank of each player in the NBA season
		deffRank = (1.25*play_df['ST'] + (play_df['TR'] - play_df['OR'])\
				+ play_df['BK'] - 2*play_df['FF'] - play_df['PF']/2)\
				/ play_df['GP']
		play_df['DeffRank'] = deffRank

		# Calculate a player's Tendex score using Doug Stats's Tendex rating system
		TND = ( play_df['PTS'] - (play_df['FGA']-play_df['FGM']) - (play_df['FTA']\
			- play_df['FTM'])/2 + 0.5*play_df['3M'] + 1.25*play_df['ST']\
			+ 1.25*play_df['AS'] + play_df['BK'] + play_df['TR'] - 1.25*play_df['TO']\
			- play_df['TC'] - 2*play_df['FF'] - play_df['PF']/2 ) / play_df['GP']
		play_df['TND'] = TND

		# Calculate season-long overall Fielg Goal Percentage (shots made  / shots attempted)
		FG = play_df['FGM']/play_df['FGA']
		play_df['FG%'] = FG

		# same goes for the teams
		team_df = pd.read_excel("team info/teams"\
						+ tempStr + ".xlsx",\
						header = 0)
		team_df = team_df.drop('ff',1)

		# add Win% and Playoffs indicator to each player's feature matrix
		for name, win, lose, play, conf in zip(team_df['key'], team_df['won'], team_df['los'], team_df['Playoffs'], team_df['Conference']):
			play_df.loc[play_df['Team'] == name, 'Win%'] = win/(win + lose)
			play_df.loc[play_df['Team'] == name, 'Playoffs'] = play
			play_df.loc[play_df['Team'] == name, 'Conference'] = conf

			meanTND = np.mean(play_df.loc[play_df['Team'] == name]['TND'])
			play_df.loc[play_df['Team'] == name, 'Team TND'] = meanTND
			team_df.loc[team_df['key'] == name, 'Avg. TND'] = meanTND

		players[i] = play_df
		teams[i] = team_df
		play_df.to_csv("gen data/players" + tempStr + ".csv", encoding = 'utf-8')
		team_df.to_csv("gen data/teams" + tempStr + ".csv", encoding = 'utf-8')

	# #print out the player information
	# for i in range(1,len(players)+1):
	# 	tempStr = str(i) + "-" + str(i+1)
	# 	print(i)
	# 	#print( players[i].head(6) )
	#
	return players, teams
