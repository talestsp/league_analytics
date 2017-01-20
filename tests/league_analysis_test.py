import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from league_analysis import LeagueAnalysis
from dao.dao import DAO
from league import League

class table_analysis_test(unittest.TestCase):

	def setUp(self):
		#testing reference http://www.zerozero.pt/edition.php?jornada_in=19&id_edicao=86785&fase=81592
		eng_dao_15_16 = DAO(country="england", season="15-16", cols="sport_cols")
		league = League(eng_dao_15_16)
		self.league_anl = LeagueAnalysis(league=league)


	def test_home_away_match_performance(self):
		chel_perf = self.league_anl.home_away_match_performance("Chelsea")
		leic_perf = self.league_anl.home_away_match_performance("Leicester")
		crpl_perf = self.league_anl.home_away_match_performance("Crystal Palace")

		self.assertEqual(7, chel_perf)
		self.assertEqual(10, leic_perf)
		self.assertEqual(7, crpl_perf)

	def test_ranking_correlation(self):
		self.league_anl.ranking_correlation(rounds=[15,16])