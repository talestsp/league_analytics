import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from pandas import to_datetime
import unittest
from grouped_stats import GroupedStats
from dao.dao import DAO

class grouped_stats_test(unittest.TestCase):

	def setUp(self):
		#testing reference http://www.zerozero.pt/edition.php?jornada_in=19&id_edicao=86785&fase=81592
		dao = DAO(country="england", season="15-16", cols="sport_cols")
		self.grouped_stats = GroupedStats(dao)

	def test_goals(self):
		home_301216 = self.grouped_stats.goals(to_date="30/12/2015")
		self.assertEqual(26, home_301216[home_301216["Team"] == "Southampton"]["Goals_F"].item())
		self.assertEqual(23, home_301216[home_301216["Team"] == "Southampton"]["Goals_A"].item())

		home_301216 = self.grouped_stats.goals(from_date="02/10/2015", to_date="30/12/2015")
		self.assertEqual(9, home_301216[home_301216["Team"] == "Southampton"]["HomeGoals_F"].item())
		self.assertEqual(6, home_301216[home_301216["Team"] == "Southampton"]["HomeGoals_A"].item())
		self.assertEqual(7, home_301216[home_301216["Team"] == "Southampton"]["AwayGoals_F"].item())
		self.assertEqual(8, home_301216[home_301216["Team"] == "Southampton"]["AwayGoals_A"].item())


		home_030216 = self.grouped_stats.goals(to_date="03/02/2016")
		self.assertEqual(30, home_030216[home_030216["Team"] == "Liverpool"]["Goals_F"].item())
		self.assertEqual(34, home_030216[home_030216["Team"] == "Liverpool"]["Goals_A"].item())


		away_140915 = self.grouped_stats.goals(to_date="14/09/2015")
		self.assertEqual(7, away_140915[away_140915["Team"] == "Swansea"]["Goals_F"].item())
		self.assertEqual(5, away_140915[away_140915["Team"] == "Swansea"]["Goals_A"].item())

		data = self.grouped_stats.goals()

		self.assertEqual(data["Goals_F"].sum(), data["Goals_A"].sum())

	def test_shots(self):
		data = self.grouped_stats.shots()
		man_united_shots = data[data["Team"] == "Man United"]

		self.assertEqual(248, man_united_shots["HS_F"].item())
		self.assertEqual(182, man_united_shots["AS_F"].item())
		self.assertEqual(158, man_united_shots["HS_A"].item())
		self.assertEqual(253, man_united_shots["AS_A"].item())

		self.assertEqual(data["S_F"].sum(), data["S_A"].sum())

	def test_shots_on_target(self):
		data = self.grouped_stats.shots_on_target()

		self.assertEqual(210, data[data["Team"] == "Man City"]["ST_F"].item())
		self.assertEqual(178, data[data["Team"] == "Newcastle"]["ST_A"].item())

		self.assertEqual(data["ST_F"].sum(), data["ST_A"].sum())
