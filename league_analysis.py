from pandas import merge, Series

from dao.dao import DAO
from league import League
from util.util import mean_deviation

class LeagueAnalysis:

	def __init__(self, league):
		self.league = league

	def ranking_correlation(self, rounds):
		print()
		print("ranking_correlation")
		to_date = self.league.date_by_round(19)
		print(to_date)
		t1 = self.league.table(to_date=to_date).head()
		print(t1)

		to_date = self.league.date_by_round(20)
		print(to_date)
		t2 = self.league.table(to_date=to_date).head()
		print(t2)

		to_date = self.league.date_by_round(21)
		print(to_date)
		t3 = self.league.table(to_date=to_date).head()
		print(t3)

		print()

		print(t1["Team"].tolist())
		print(t2["Team"].tolist())
		print(t3["Team"].tolist())
		print()

		print(t1["Team"].corr(t2["Team"], method="spearman"))
		print(t2["Team"].corr(t3["Team"], method="spearman"))
		print(Series(["a", "b", "c", "d", "x"]).corr(Series(["a", "b", "c", "d", "y"]), method="spearman"))
		print()

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
		


		 
