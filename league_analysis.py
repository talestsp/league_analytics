from pandas import merge, Series, DataFrame

from dao.dao import DAO
from league import League
from util.util import mean_deviation

class LeagueAnalysis:

	def __init__(self, league):
		self.league = league

	def ranking_corr_by_dates(self, df_tables, method="spearman", n_head=None):
		'''
		Args:
			df_tables: list of table dataframes
			method: ranking correlation method: 'spearman' or 'kendall'
			n_head: n firsts position for the table, if None all position will be considered

		Returns:
			an array with the correlations between consecutive dates in dates_list 
		for the <n_head> firsts positions in the table from that date.
		'''

		if n_head is None:
			n_head = len(self.league.teams())

		correlations = []

		for i in range(len(df_tables) - 1):
			df1 = df_tables[i]
			df2 = df_tables[i + 1]
			
			ranking1, ranking2 = self.rankings(df1=df1, df2=df2, n_head=n_head)
			corr = ranking1.corr(ranking2, method=method)
			correlations.append(corr)
			
		return correlations		


	def rankings(self, df1, df2, n_head):
		df1_rankings = df1.head(n_head).index.tolist()
		df1_teams = df1.head(n_head)["Team"].tolist()

		df2_rankings = []

		for team in df1_teams:
			mapping_rank1_rank2 = df2[df2["Team"] == team].index.item()
			df2_rankings.append(mapping_rank1_rank2)

		return Series(df1_rankings), Series(df2_rankings)

	def home_away_match_performance(self, team):
		'''
		Args:
			team:
				compute performance for this team

		Returns:
			how frequent is for a team to win in away match the same points 
			as in home match, aiganst the same team
		'''

		matches = self.league.home_away_matches(team=team)

		stability_series = matches.apply(lambda row: self.home_away_stability(row), axis=1)
		stability = stability_series.value_counts()[True]

		return stability

	def home_away_stability(self, row):
		if row["TeamHG"] > row["AigAG"]:
			points_home = 3
		elif row["TeamHG"] == row["AigAG"]:
			points_home =  1
		else:
			points_home =  0

		if row["TeamAG"] > row["AigHG"]:
			points_away = 3
		elif row["TeamAG"] == row["AigHG"]:
			points_away =  1
		else:
			points_away =  0

		return points_home == points_away

	def match_level(self, team):
		matches = self.league.home_away_matches(team=team)
		points = self.league.points()

		match_points = merge(left=matches, right=points, left_on="Aiganst", right_on="Team", how='inner')

		print()
		print(points[["Team", "Points"]])
		print(match_points)

		victories = self.oponnet_defeated_points(match_points)
		print(round(victories["home"].mean()), (victories["home"]).tolist())
		
		ties = self.oponnet_tied_points(match_points)
		print(round(ties["home"].mean()), (ties["home"]).tolist())
		
		looses = self.oponnet_wins_points(match_points)
		print(round(looses["home"].mean()), (looses["home"]).tolist())
		
		return None


	def oponnet_defeated_points(self, match_points):
		home_wins_oponnent_pts = match_points[match_points['TeamHG'] > match_points['AigAG']]
		away_wins_oponnent_pts = match_points[match_points['TeamAG'] > match_points['AigHG']]

		return {"home": home_wins_oponnent_pts["Points"], "away": away_wins_oponnent_pts["Points"]}

	def oponnet_tied_points(self, match_points):
		home_wins_oponnent_pts = match_points[match_points['TeamHG'] == match_points['AigAG']]
		away_wins_oponnent_pts = match_points[match_points['TeamAG'] == match_points['AigHG']]

		return {"home": home_wins_oponnent_pts["Points"], "away": away_wins_oponnent_pts["Points"]}

	def oponnet_wins_points(self, match_points):
		home_wins_oponnent_pts = match_points[match_points['TeamHG'] < match_points['AigAG']]
		away_wins_oponnent_pts = match_points[match_points['TeamAG'] < match_points['AigHG']]

		return {"home": home_wins_oponnent_pts["Points"], "away": away_wins_oponnent_pts["Points"]}
		


		 
