import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from pandas import to_datetime
from league import League
from dao.dao import DAO
from dates import next_day, previous_day

class league_test(unittest.TestCase):

	def setUp(self):
		#testing reference http://www.zerozero.pt/edition.php?jornada_in=19&id_edicao=86785&fase=81592
		eng_dao_15_16 = DAO(country="england", season="15-16", cols="sport_cols")
		self.league = League(eng_dao_15_16)

		spa_dao_15_16 = DAO(country="spain", season="15-16", cols="sport_cols")
		self.league_spa = League(spa_dao_15_16)

	def test_table(self):

		half_league_date = self.league.date_by_round(19)
		league_table = self.league.table(to_date=half_league_date)
		self.assertEqual(19, min(league_table["Played"]))
		
		self.assertEqual(20, len(league_table))
		self.assertEqual(20, len(self.league.table()))
		
		self.assertEqual("Leicester", self.league.table().loc[1]["Team"])
		self.assertEqual("Arsenal", self.league.table().loc[2]["Team"])

		self.assertEqual("Leicester", league_table.loc[2]["Team"])
		self.assertEqual("Arsenal", league_table.loc[1]["Team"])



	def test_played_matches(self):
		played_matches = self.league.played_matches()

		self.assertEqual(38, played_matches.iloc[0])
		self.assertEqual(38, played_matches["Man United"])
		self.assertEqual(38, min(played_matches))
		self.assertEqual(38, min(played_matches))

		half_league_date = self.league.half_league_date()
		played_matches_h1 = self.league.played_matches(to_date=half_league_date)

		self.assertEqual(19 * 20, sum(played_matches_h1))

		half_league_date_next_day = next_day(half_league_date)
		played_matches_h2 = self.league.played_matches(to_date=half_league_date_next_day)
		self.assertEqual(19 * 20, sum(played_matches_h2))

		firsts_5_rounds = self.league.played_matches(to_date="14/09/2015")
		self.assertEqual(5, (firsts_5_rounds.mean()))


	def test_points(self):
		full_league_points = self.league.points()

		leicester_full = full_league_points[full_league_points["Team"] == "Leicester"]
		self.assertEqual(81, leicester_full["Points"].item())

		aston_villa_full = full_league_points[full_league_points["Team"] == "Aston Villa"]
		self.assertEqual(17, aston_villa_full["Points"].item())

		chelsea_full = full_league_points[full_league_points["Team"] == "Chelsea"]
		self.assertEqual(50, chelsea_full["Points"].item())

		firsts_5_rounds = self.league.points(to_date="14/09/2015")

		arsenal_5_rounds = firsts_5_rounds[firsts_5_rounds["Team"] == "Arsenal"]
		self.assertEqual(10, arsenal_5_rounds["Points"].item())

	def test_remaining_matches(self):
		#remaining matches after league completion
		end_date = self.league.end_league_date()

		full_league_remaining_matches = self.league.remaining_matches(from_date=end_date)
		self.assertEqual(0, min(full_league_remaining_matches))
		self.assertEqual(0, max(full_league_remaining_matches))

		#print(full_league_remaining_matches)
		#print("\n\n\n\n")

		#remaining matches after half league
		half_league_date_previous_day = previous_day(self.league.half_league_date())
		half_league_remaining_matches = self.league.remaining_matches(from_date=half_league_date_previous_day)
		#median because maybe sometimes a time could end the first half league with 1 more match
		# or a match less
		self.assertEqual(19, half_league_remaining_matches.median())

		#print(half_league_remaining_matches)
		#print("\n\n\n\n")

		#remaining matches before league beginning
		start_league_date_previous_day = previous_day(self.league.start_league_date())
		before_league_remaining_matches = self.league.remaining_matches(from_date=start_league_date_previous_day)

		self.assertEqual(38, min(before_league_remaining_matches))
		self.assertEqual(38, max(before_league_remaining_matches))

		#print(before_league_remaining_matches)
		#print("\n\n\n\n")

		remainig_after_25_10_2015 = self.league.remaining_matches(from_date="25/10/2015")

		#print(self.league.remaining_matches(from_date="25/10/2015"))
		#print("\n\n\n\n")

		self.assertEqual(28, remainig_after_25_10_2015["Tottenham"])

		remainig_after_24_10_2015 = self.league.remaining_matches(from_date="24/10/2015")

		#print(self.league.remaining_matches(from_date="24/10/2015"))
		#print("\n\n\n\n")

		self.assertEqual(29, remainig_after_24_10_2015["Man United"])

	def test_matches(self):
		matches = self.league.matches()

		self.assertEqual(20 * 19, len(matches))

		self.assertEqual(19, len(matches[matches["HomeTeam"] == "Everton"]))
		self.assertEqual(19, len(matches[matches["AwayTeam"] == "Watford"]))

		self.assertEqual(to_datetime("2015-08-08"), min(matches["Date"]))
		self.assertEqual(to_datetime("2016-05-17"), max(matches["Date"]))

		match = matches[(matches["Date"] == to_datetime("2015-08-22")) & (matches["HomeTeam"] == "West Ham")]
		self.assertEqual(match["HomeTeam"].item(), "West Ham")
		self.assertEqual(match["AwayTeam"].item(), "Bournemouth")
		self.assertEqual(match["FTHG"].item(), 3)
		self.assertEqual(match["FTAG"].item(), 4)

	def test_home_away_matches(self):
		manutd_played_matches = self.league.home_away_matches(team="Man United")

		manutd_everton = manutd_played_matches[manutd_played_matches["Aiganst"] == "Everton"]
		self.assertEqual(0, manutd_everton["AigHG"].item())
		self.assertEqual(3, manutd_everton["TeamAG"].item())
		self.assertEqual(1, manutd_everton["TeamHG"].item())
		self.assertEqual(0, manutd_everton["AigAG"].item())


		livp_played_matches = self.league.home_away_matches(team="Liverpool")

		livp_norw = livp_played_matches[livp_played_matches["Aiganst"] == "Norwich"]
		self.assertEqual(4, livp_norw["AigHG"].item())
		self.assertEqual(5, livp_norw["TeamAG"].item())
		self.assertEqual(1, livp_norw["TeamHG"].item())
		self.assertEqual(1, livp_norw["AigAG"].item())

	def test_team_history_goals(self):
		self.league.team_history_goals(team="Leicester")
		#TODO

	def test_team_history_points(self):
		hp = self.league.team_history_points(team="Leicester", to_date="2016-05-08")
		self.assertEqual(37, len(hp))

		self.assertEqual(3, hp.iloc[0]["Points"])
		self.assertEqual(1, hp.iloc[3]["Points"])
		self.assertEqual(0, hp.iloc[6]["Points"])
		self.assertEqual(1, hp.iloc[8]["Points"])
		self.assertEqual(1, hp.iloc[21]["Points"])
		self.assertEqual(0, hp.iloc[25]["Points"])		

	def test_team_shots(self):
		team_shots = self.league_spa.team_shots(team="Real Madrid")
		home = team_shots["home"]
		away = team_shots["away"]

		# print()	
		# print(home["shots"], home["shots_target"], home["goals"])
		# print(float(home["goals"]) / home["shots_target"])
		# print(away["shots"], away["shots_target"], away["goals"])
		# print(float(away["goals"]) / away["shots_target"])

		team_shots = self.league_spa.team_shots(team="Barcelona")
		home = team_shots["home"]
		away = team_shots["away"]
	
		# print()
		# print(home["shots"], home["shots_target"], home["goals"])
		# print(float(home["goals"]) / home["shots_target"])
		# print(away["shots"], away["shots_target"], away["goals"])
		# print(float(away["goals"]) / away["shots_target"])
		# print ()

	def test_date_by_round(self):
		n_round = 20
		self.assertEqual("2016-01-03 00:00:00", str(self.league.date_by_round(n_round)))

		