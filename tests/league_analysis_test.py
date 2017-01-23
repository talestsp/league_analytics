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

	def test_paired_points(self):
		eng_dao_16_17 = DAO(country="england", season="16-17", cols="sport_cols")
		eng_league = League(eng_dao_16_17)
		eng_league_anl = LeagueAnalysis(league=eng_league)

		n_round = 18

		five_dates = [eng_league.date_by_round(round_n) for round_n in range(n_round - 4, n_round + 1)]
		
		date1 = five_dates[0]
		date2 = five_dates[-1]
		
		df1 = eng_league.table(to_date=date1)
		df2 = eng_league.table(to_date=date2)

        # Chelsea		34 46	Chelsea
        # Arsenal		31 40	Liverpool
        # Liverpool		30 39	Man City
        # Man City		30 37	Arsenal
        # Tottenham		27 36	Tottenham

		points1, points2 = eng_league_anl.paired_points(df1, df2, n_head=5)

		self.assertEqual(points1.tolist(), [34, 31, 30, 30, 27])
		self.assertEqual(points2.tolist(), [46, 37, 40, 39, 36])

	def test_points_corr(self):
		eng_dao_16_17 = DAO(country="england", season="16-17", cols="sport_cols")
		eng_league = League(eng_dao_16_17)
		eng_league_anl = LeagueAnalysis(league=eng_league)
		n_round = 18

		date1 = "2016-12-28"
		table_df1 = eng_league.table(to_date=date1)

		corr1 = eng_league_anl.points_corr(df_tables=[table_df1, table_df1], method="spearman", n_head=10)
		self.assertLess(0.98, corr1[0])

		date2 = "2016-12-05"
		table_df2 = eng_league.table(to_date=date2)

		corr2 = eng_league_anl.points_corr(df_tables=[table_df1, table_df2], method="spearman", n_head=5)
		self.assertLess(0.6665, corr2[0])
		self.assertGreater(0.6669, corr2[0])
		
