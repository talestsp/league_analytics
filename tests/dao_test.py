import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from pandas import to_datetime

import unittest
from dao.dao import DAO

class dao_test(unittest.TestCase):

	def setUp(self):
		#testing reference http://www.zerozero.pt/edition.php?jornada_in=19&id_edicao=86785&fase=81592
		self.dao = DAO(country="england", season="15-16", cols="sport_cols")

	def test_get_data(self):
		#each team plays 19 time as HomeTeam
		self.assertEqual(20 * 19, len(self.dao.get_data()))

	def test_half_league_data(self):
		half1 = self.dao.half_league_data(half=1)

		self.assertEqual(max(half1["Date"]), to_datetime("30/12/2015", dayfirst=True))
		self.assertEqual(min(half1["Date"]), to_datetime("08/08/2015", dayfirst=True))

	def test_search_percentil_date(self):
		p05 = self.dao.search_percentil_date(percentile=0.5)
		self.assertEqual(p05, to_datetime("30/12/2015", dayfirst=True))

		p0316 = self.dao.search_percentil_date(percentile=0.316)
		self.assertEqual(p0316, to_datetime("08/11/2015", dayfirst=True))

		p06316 = self.dao.search_percentil_date(percentile=0.6316)
		self.assertEqual(p06316, to_datetime("03/02/2016", dayfirst=True))

