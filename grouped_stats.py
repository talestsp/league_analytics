import pandas as pd
from util.util import merge_series

class GroupedStats:

	def __init__(self, dao):
		self.dao = dao

	def goals(self, from_date=None, to_date=None):
		'''
		Args:
			date: the goals will be counted untill this date (including this day). it could be a
					 string in format dd/mm/yyyy or a pandas.tslib.Timestamp
		Returns:
			the goals for and against, home and away by team 
		'''

		data = self.dao.slice_data_by_date(from_date=from_date, to_date=to_date)

		for_data_home = data.groupby("HomeTeam")["FTHG"].sum()
		for_data_away = data.groupby("AwayTeam")["FTAG"].sum()

		aig_data_home = data.groupby("HomeTeam")["FTAG"].sum()
		aig_data_away = data.groupby("AwayTeam")["FTHG"].sum()


		for_data_home_df = pd.DataFrame(for_data_home)
		for_data_home_df = for_data_home_df.reset_index()
		for_data_home_df = for_data_home_df.rename(columns={"HomeTeam": "Team", "FTHG": "HomeGoals_F"})

		for_data_away_df = pd.DataFrame(for_data_away)
		for_data_away_df = for_data_away_df.reset_index()
		for_data_away_df = for_data_away_df.rename(columns={"AwayTeam": "Team", "FTAG": "AwayGoals_F"})

		aig_data_home_df = pd.DataFrame(aig_data_home)
		aig_data_home_df = aig_data_home_df.reset_index()
		aig_data_home_df = aig_data_home_df.rename(columns={"HomeTeam": "Team", "FTAG": "HomeGoals_A"})

		aig_data_away_df = pd.DataFrame(aig_data_away)
		aig_data_away_df = aig_data_away_df.reset_index()
		aig_data_away_df = aig_data_away_df.rename(columns={"AwayTeam": "Team", "FTHG": "AwayGoals_A"})
		
		goals_df = pd.merge(for_data_home_df, for_data_away_df, on="Team", how="outer")
		goals_df = pd.merge(goals_df, aig_data_home_df, on="Team", how="outer")
		goals_df = pd.merge(goals_df, aig_data_away_df, on="Team", how="outer")

		goals_df["Goals_F"] = goals_df["HomeGoals_F"] + goals_df["AwayGoals_F"]
		goals_df["Goals_A"] = goals_df["HomeGoals_A"] + goals_df["AwayGoals_A"]


		return goals_df[["Team", "Goals_F", "Goals_A", "HomeGoals_F", "AwayGoals_F", "HomeGoals_A", "AwayGoals_A"]]

	
	def shots(self, from_date=None, to_date=None):
		data = self.dao.slice_data_by_date(from_date=from_date, to_date=to_date)

		#SHOTS
		for_data_home_shots = data.groupby("HomeTeam")["HS"].sum()
		for_data_away_shots = data.groupby("AwayTeam")["AS"].sum()

		aig_data_home_shots = data.groupby("HomeTeam")["AS"].sum()
		aig_data_away_shots = data.groupby("AwayTeam")["HS"].sum()

		for_data_home_shots_df = pd.DataFrame(for_data_home_shots)
		for_data_home_shots_df = for_data_home_shots_df.reset_index()
		for_data_home_shots_df = for_data_home_shots_df.rename(columns={"HomeTeam": "Team", "HS": "HS_F"})

		for_data_away_shots_df = pd.DataFrame(for_data_away_shots)
		for_data_away_shots_df = for_data_away_shots_df.reset_index()
		for_data_away_shots_df = for_data_away_shots_df.rename(columns={"AwayTeam": "Team", "AS": "AS_F"})

		aig_data_home_shots_df = pd.DataFrame(aig_data_home_shots)
		aig_data_home_shots_df = aig_data_home_shots_df.reset_index()
		aig_data_home_shots_df = aig_data_home_shots_df.rename(columns={"HomeTeam": "Team", "AS": "HS_A"})

		aig_data_away_shots_df = pd.DataFrame(aig_data_away_shots)
		aig_data_away_shots_df = aig_data_away_shots_df.reset_index()
		aig_data_away_shots_df = aig_data_away_shots_df.rename(columns={"AwayTeam": "Team", "HS": "AS_A"})

		shots_df = pd.merge(for_data_home_shots_df, for_data_away_shots_df, on="Team", how="outer")
		shots_df = pd.merge(shots_df, aig_data_home_shots_df, on="Team", how="outer")
		shots_df = pd.merge(shots_df, aig_data_away_shots_df, on="Team", how="outer")

		shots_df["S_F"] = shots_df["HS_F"] + shots_df["AS_F"]
		shots_df["S_A"] = shots_df["HS_A"] + shots_df["AS_A"]


		return shots_df[["Team", "S_F", "S_A", "HS_F", "AS_F", "HS_A", "AS_A"]]		


	def shots_on_target(self, from_date=None, to_date=None):
		data = self.dao.slice_data_by_date(from_date=from_date, to_date=to_date)

		#SHOTS
		for_data_home_shots = data.groupby("HomeTeam")["HST"].sum()
		for_data_away_shots = data.groupby("AwayTeam")["AST"].sum()

		aig_data_home_shots = data.groupby("HomeTeam")["AST"].sum()
		aig_data_away_shots = data.groupby("AwayTeam")["HST"].sum()

		for_data_home_shots_df = pd.DataFrame(for_data_home_shots)
		for_data_home_shots_df = for_data_home_shots_df.reset_index()
		for_data_home_shots_df = for_data_home_shots_df.rename(columns={"HomeTeam": "Team", "HST": "HST_F"})

		for_data_away_shots_df = pd.DataFrame(for_data_away_shots)
		for_data_away_shots_df = for_data_away_shots_df.reset_index()
		for_data_away_shots_df = for_data_away_shots_df.rename(columns={"AwayTeam": "Team", "AST": "AST_F"})

		aig_data_home_shots_df = pd.DataFrame(aig_data_home_shots)
		aig_data_home_shots_df = aig_data_home_shots_df.reset_index()
		aig_data_home_shots_df = aig_data_home_shots_df.rename(columns={"HomeTeam": "Team", "AST": "HST_A"})

		aig_data_away_shots_df = pd.DataFrame(aig_data_away_shots)
		aig_data_away_shots_df = aig_data_away_shots_df.reset_index()
		aig_data_away_shots_df = aig_data_away_shots_df.rename(columns={"AwayTeam": "Team", "HST": "AST_A"})

		shots_df = pd.merge(for_data_home_shots_df, for_data_away_shots_df, on="Team", how="outer")
		shots_df = pd.merge(shots_df, aig_data_home_shots_df, on="Team", how="outer")
		shots_df = pd.merge(shots_df, aig_data_away_shots_df, on="Team", how="outer")

		shots_df["ST_F"] = shots_df["HST_F"] + shots_df["AST_F"]
		shots_df["ST_A"] = shots_df["HST_A"] + shots_df["AST_A"]


		return shots_df[["Team", "ST_F", "ST_A", "HST_F", "AST_F", "HST_A", "AST_A"]]		

	# def stats_for(self, playing=None):
	# 	goals = self.goals(side="for", playing=playing)
	# 	shots_on_target = self.shots_on_target(side="for", playing=playing)
	# 	shots = self.shots(side="for", playing=playing)

	# 	series_list = [{"colname": "Goals_F", "series": goals}, {"colname": "ShotsTarget_F", "series": shots_on_target}, {"colname": "Shots_F", "series": shots}]

	# 	attacking_stats = merge_series(series_list, on="Team", how="outer")

	# 	return attacking_stats.sort_values(by="Goals_F", ascending=False)

	# def stats_against(self, playing=None):
	# 	goals = self.goals(side="against", playing=playing)
	# 	shots_on_target = self.shots_on_target(side="against", playing=playing)
	# 	shots = self.shots(side="against", playing=playing)

	# 	series_list = [{"colname": "Goals_A", "series": goals}, {"colname": "ShotsTarget_A", "series": shots_on_target}, {"colname": "Shots_A", "series": shots}]

	# 	attacking_stats = merge_series(series_list, on="Team", how="outer")

	# 	return attacking_stats.sort_values(by="Goals_A", ascending=False)