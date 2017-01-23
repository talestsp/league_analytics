from pandas import DataFrame, Series, merge, to_datetime
from dates import next_day, previous_day
from grouped_stats import GroupedStats

WIN_POINTS = 3
DRAW_POINTS = 1


class League:

	def __init__(self, dao):
		self.dao = dao
		self.country = dao.country
		self.season = dao.season

	def table(self, from_date=None, to_date=None):
		'''
		Returns the league table with the global basic information.
		'''
		played = self.played_matches(from_date, to_date)

		points = self.points(from_date, to_date)
		points = Series(points["Points"].tolist(), index=points["Team"].tolist())

		matches = self.matches(from_date, to_date)
		
		home_grouped = matches.groupby(["HomeTeam"]).apply(lambda df_group: len(df_group[df_group["FTHG"] > df_group["FTAG"]]))
		away_grouped = matches.groupby(["AwayTeam"]).apply(lambda df_group: len(df_group[df_group["FTAG"] > df_group["FTHG"]]))
		won = home_grouped + away_grouped

		home_grouped = matches.groupby(["HomeTeam"]).apply(lambda df_group: len(df_group[df_group["FTHG"] == df_group["FTAG"]]))
		away_grouped = matches.groupby(["AwayTeam"]).apply(lambda df_group: len(df_group[df_group["FTAG"] == df_group["FTHG"]]))
		draw = home_grouped + away_grouped

		home_grouped = matches.groupby(["HomeTeam"]).apply(lambda df_group: len(df_group[df_group["FTHG"] < df_group["FTAG"]]))
		away_grouped = matches.groupby(["AwayTeam"]).apply(lambda df_group: len(df_group[df_group["FTAG"] < df_group["FTHG"]]))
		lost = home_grouped + away_grouped

		home_grouped = matches.groupby(["HomeTeam"]).apply(lambda df_group: sum(df_group["FTHG"]))
		away_grouped = matches.groupby(["AwayTeam"]).apply(lambda df_group: sum(df_group["FTAG"]))
		goals_for = home_grouped + away_grouped
		
		home_grouped = matches.groupby(["HomeTeam"]).apply(lambda df_group: sum(df_group["FTAG"]))
		away_grouped = matches.groupby(["AwayTeam"]).apply(lambda df_group: sum(df_group["FTHG"]))
		goals_aga = home_grouped + away_grouped
		
		table = DataFrame(dict(Points=points, Played=played, Won=won, Draw=draw, Lost=lost, GF=goals_for, GA=goals_aga, GD=goals_for - goals_aga)).reset_index()
		table = table.rename(columns={"index": "Team"})
		table = table[["Points", "Team", "Played", "Won", "Draw", "Lost", "GF", "GA", "GD"]].sort_values(by=["Points", "GD"], ascending=False).reset_index()
		table.index = range(1,len(table)+1)
		del table["index"]
		return table

	def teams(self):
		'''
		Returns the league teams
		'''
		return self.dao.teams()

	def points(self, from_date=None, to_date=None):
		'''
		Returns the points conquered for each team.
		'''
		points_df = merge(self.points_home(from_date, to_date), self.points_away(from_date, to_date), on="Team")

		points_df["Points"] = points_df["PointsHome"] + points_df["PointsAway"]
		points_df = points_df.sort_values(by="Team").reset_index(drop=True)

		return points_df.sort_values(by="Points", ascending=False)

	def points_away(self, from_date=None, to_date=None):
		'''
		Returns the points conquered playing away.
		'''
		data = self.dao.slice_data_by_date(from_date, to_date)
		points_df = DataFrame()

		for team in data["AwayTeam"].drop_duplicates().tolist():
			team_points = 0
			team_data = data[data["AwayTeam"] == team]
			
			for match_row in team_data.iterrows():
				index, match = match_row
				
				if match["FTAG"] > match["FTHG"]:
					team_points += WIN_POINTS
				elif match["FTAG"] == match["FTHG"]:
					team_points += DRAW_POINTS
			
			points_df = points_df.append(DataFrame([{"Team": team, "PointsAway": team_points}]))

		return points_df[["Team", "PointsAway"]].sort_values(by="PointsAway", ascending=False)

	def points_home(self, from_date=None, to_date=None):
		'''
		Returns the points conquered playing home.
		'''
		data = self.dao.slice_data_by_date(from_date, to_date)
		points_df = DataFrame()

		for team in data["HomeTeam"].drop_duplicates().tolist():
			team_points = 0
			team_data = data[data["HomeTeam"] == team]
			
			for match_row in team_data.iterrows():
				index, match = match_row
				
				if match["FTHG"] > match["FTAG"]:
					team_points += WIN_POINTS
				elif match["FTHG"] == match["FTAG"]:
					team_points += DRAW_POINTS
			
			points_df = points_df.append(DataFrame([{"Team": team, "PointsHome": team_points}]))

		return points_df[["Team", "PointsHome"]].sort_values(by="PointsHome", ascending=False)


	def matches(self, from_date=None, to_date=None):
		'''
		Returns the date and score details for each league match.
		'''
		data = self.dao.slice_data_by_date(from_date, to_date)
		return data[["Date", "HomeTeam", "FTHG", "AwayTeam", "FTAG"]]

	def played_matches(self, from_date=None, to_date=None):
		'''
		Return the number of matchers played for each team.
		'''
		use_data = self.dao.slice_data_by_date(from_date, to_date)

		home_matches = use_data["HomeTeam"].value_counts()
		away_matches = use_data["AwayTeam"].value_counts()

		return home_matches + away_matches

	def remaining_matches(self, from_date):
		'''
		Returns the number of remaining_matches for each team.
		'''

		if isinstance(from_date, str):
			from_date = to_datetime(from_date, dayfirst=True)

		next_date = next_day(from_date)

		if next_date >= self.end_league_date():
			teams = self.dao.get_data()["HomeTeam"]
			teams = teams.append(self.dao.get_data()["AwayTeam"])
			teams = teams.drop_duplicates()
			values = [0] * len(teams)
			remaining_matches = Series(values)
			teams = teams.sort_values()
			remaining_matches.index = teams
			return remaining_matches

		if from_date < self.start_league_date():
			teams = self.dao.get_data()
			home_remaining_matches = teams["HomeTeam"].value_counts()
			away_remaining_matches = teams["AwayTeam"].value_counts()

			return home_remaining_matches + away_remaining_matches

		matches_played_data = self.dao.slice_data_by_date(from_date=None, to_date=from_date)

		home_remaining_matches = matches_played_data["HomeTeam"].value_counts()
		away_remaining_matches = matches_played_data["AwayTeam"].value_counts()
		matches_played = home_remaining_matches + away_remaining_matches

		full_league_data = self.dao.slice_data_by_date(from_date=None, to_date=None)

		home_full_matches = full_league_data["HomeTeam"].value_counts()
		away_full_matches = full_league_data["AwayTeam"].value_counts()
		full_matches = home_full_matches + away_full_matches

		return full_matches - matches_played

	def date_by_round(self, n_round):
		'''
		Returns the lowest date on which all teams have accomplishd <n_round> matches
		'''	
		dates = self.matches()["Date"].drop_duplicates()

		for date in dates:
			played_matches = self.played_matches(to_date=date)
			if min(played_matches) == n_round:
				break 

		return date
		
	def half_league_date(self):
		#TO BE FIXED - it must consider the on going league data
		'''
		Returns the date that the teams played half league
		'''
		half_data = self.dao.half_league_data(half=1)
		return max(half_data["Date"])

	def start_league_date(self):
		'''
		Returns the date of the first match
		'''
		data = self.dao.get_data()
		return min(data["Date"])

	def end_league_date(self):
		#TO BE FIXED - it must consider the on going league data
		'''
		Returns the date that the last match
		'''
		data = self.dao.get_data()
		return max(data["Date"])

	def home_away_matches(self, team):
		'''
		Args:
			team: a team to get its matches

		Returns:
			a pandas.DataFrame with columns
				Team: selected team, 
				TeamHG: team goals scored playing in home,
				AigAG: ainganst team goals scored in away,
				AigHG: ainganst team goals scored in home,
				TeamAG: team goals scored playing in away,
				Aiganst: team that played matches ainganst selected team
		'''
		matches = self.matches()
		home_team_data = matches[matches["HomeTeam"] == team]
		away_team_data = matches[matches["AwayTeam"] == team]

		home_away_matches = merge(left=home_team_data, right=away_team_data, left_on="AwayTeam", right_on="HomeTeam", how="outer")

		columns = ['HomeTeam_x', 'FTHG_x', 'FTAG_x', 'FTHG_y', 'FTAG_y', 'AwayTeam_x']
		home_away_matches = home_away_matches[columns]
		home_away_matches = home_away_matches.rename(columns={'HomeTeam_x': 'Team', 'AwayTeam_x': 'Aiganst', "FTHG_x": "TeamHG", "FTAG_x": "AigAG", "FTHG_y": "AigHG", "FTAG_y": "TeamAG"})

		return home_away_matches

	def team_history_goals(self, team, from_date=None, to_date=None):
		'''
		Args:
			team: a team to get the data

		Returns:
			the goals scored in all matches
		'''
		data = self.dao.slice_data_by_date(from_date, to_date)

		home_data = data[data["HomeTeam"] == team][["Date", "FTHG"]]
		away_data = data[data["AwayTeam"] == team][["Date", "FTAG"]]

		homeaway_data = home_data.append(away_data)
		homeaway_data["Team"] = [team] * len(homeaway_data)
		homeaway_data["Goals"] = (homeaway_data["FTHG"].fillna(0) + homeaway_data["FTAG"].fillna(0)).astype(int)

		homeaway_data = homeaway_data.sort_values(by="Date")

		return homeaway_data[["Date", "Team", "Goals"]]

	def team_history_points(self, team, from_date=None, to_date=None):
		'''
		Args:
			team: a team to get the data

		Returns:
			the points won in all matches
		'''
		data = self.dao.slice_data_by_date(from_date, to_date)

		home_data = data[data["HomeTeam"] == team][["Date", "FTHG", "FTAG"]]
		home_data["Points"] = home_data.apply(
			lambda row: 3 if (row["FTHG"] > row["FTAG"]) else 1 if (row["FTHG"] == row["FTAG"]) else 0, 
			axis=1)

		away_data = data[data["AwayTeam"] == team][["Date", "FTAG", "FTHG"]]
		away_data["Points"] = away_data.apply(
			lambda row: 3 if (row["FTAG"] > row["FTHG"]) else 1 if (row["FTAG"] == row["FTHG"]) else 0, 
			axis=1)

		homeaway_data = home_data.append(away_data)
		homeaway_data = homeaway_data.sort_values(by="Date")
		homeaway_data["Team"] = [team] * len(homeaway_data)

		return homeaway_data[["Date", "Team", "Points"]].sort_values(by="Date")

	def team_shots(self, team):
		'''
		Returns: 
				the stats about shots, shots on target and goals
		Args:
				team: stats about this team
				side: "for" for this team, "aig" aiganst this teams
		'''

		data = self.dao.get_data()[["HomeTeam", "HS", "HST", "FTHG", "AwayTeam", "AS", "AST", "FTAG"]]

		home_data = data[data["HomeTeam"] == team]
		away_data = data[data["AwayTeam"] == team]

		home_shots = home_data["HS"].sum()
		home_shots_t = home_data["HST"].sum()
		home_goals = home_data["FTHG"].sum()

		away_shots = away_data["AS"].sum()
		away_shots_t = away_data["AST"].sum()
		away_goals = away_data["FTAG"].sum()

		return {"home": {"shots": home_shots, "shots_target": home_shots_t, "goals": home_goals}, 
				"away": {"shots": away_shots, "shots_target": away_shots_t, "goals": away_goals}}