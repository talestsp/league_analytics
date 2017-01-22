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

	def test_rankings(self):
		eng_dao_16_17 = DAO(country="england", season="16-17", cols="sport_cols")
		eng_league = League(eng_dao_16_17)
		eng_league_anl = LeagueAnalysis(league=eng_league)

		n_round = 18

		five_dates = [eng_league.date_by_round(round_n) for round_n in range(n_round - 4, n_round + 1)]
		
		date1 = five_dates[0]
		date2 = five_dates[-1]
		
		df1 = eng_league.table(to_date=date1)
		df2 = eng_league.table(to_date=date2)

		#               df1		df2
		#1          Chelsea		Chelsea
		#2          Arsenal		Liverpool
		#3        Liverpool		Man City
		#4         Man City		Arsenal
		#5        Tottenham		Tottenham

		ranking1, ranking2 = eng_league_anl.rankings(df1, df2, n_head=5)

		self.assertEqual(ranking1.tolist(), [1,2,3,4,5])
		self.assertEqual(ranking2.tolist(), [1,4,2,3,5])

	def test_ranking_corr_by_dates(self):
		eng_dao_16_17 = DAO(country="england", season="16-17", cols="sport_cols")
		eng_league = League(eng_dao_16_17)
		eng_league_anl = LeagueAnalysis(league=eng_league)
		n_round = 18

		date1 = "2016-12-28"
		table_df1 = eng_league.table(to_date=date1)

		corr1 = eng_league_anl.ranking_corr_by_dates(df_tables=[table_df1, table_df1], method="spearman", n_head=10)
		self.assertLess(0.98, corr1[0])

		date2 = "2016-12-05"
		table_df2 = eng_league.table(to_date=date2)

		corr2 = eng_league_anl.ranking_corr_by_dates(df_tables=[table_df1, table_df2], method="spearman", n_head=5)
		self.assertLess(0.675, corr2[0])
		self.assertGreater(0.701, corr2[0])
		
