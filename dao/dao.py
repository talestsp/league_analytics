import pandas as pd
from util.util import league_progress_by_date
from pandas import to_datetime
from os.path import exists

DATA_DIR = "data/"
SPORT_COLS = ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'Attendance', 'Referee', 'HS', 'AS', 'HST', 'AST', 'HHW', 'AHW', 'HC', 'AC', 'HF', 'AF', 'HO', 'AO', 'HY', 'AY', 'HR', 'AR', 'HBP', 'ABP']
BETTING_COLS = ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'BSH', 'BSD', 'BSA', 'BWH', 'BWD', 'BWA', 'GBH', 'GBD', 'GBA', 'IWH', 'IWD', 'IWA', 'LBH', 'LBD', 'LBA', 'PSH', 'PSD', 'PSA', 'SOH', 'SOD', 'SOA', 'SBH', 'SBD', 'SBA', 'SJH', 'SJD', 'SJA', 'SYH', 'SYD', 'SYA', 'VCH', 'VCD', 'VCA', 'WHH', 'WHD', 'WHA', 'Bb1X2', 'BbMxH', 'BbAvH', 'BbMxD', 'BbAvD', 'BbMxA', 'BbAvA', 'BbOU', 'BbMx>2.5', 'BbAv>2.5', 'BbMx<2.5', 'BbAv<2.5', 'GB>2.5', 'GB<2.5', 'B365>2.5', 'B365<2.5', 'BbAH', 'BbAHh', 'BbMxAHH', 'BbAvAHH', 'BbMxAHA', 'BbAvAHA', 'GBAHH', 'GBAHA', 'GBAH', 'LBAHH', 'LBAHA', 'LBAH', 'B365AHH', 'B365AHA', 'B365AH', 'PSCH', 'PSCD', 'PSCA']

class DAO:

	def __init__(self, country, season, cols="all"):
		self.country = country
		self.season = season
		self.data = self.load_data(country, season, cols=cols)

	def load_data(self, country, season, cols):
		data_path = DATA_DIR + country + "-" + season + ".csv"

		if not exists(data_path):
			raise Exception("Data file not found:", str(data_path))

		data = pd.read_csv(data_path)
		data = self.date_to_datetime(data)

		if cols == "all":
			return data

		elif cols == "sport_cols":
			#not all data has all columns
			columns = set(SPORT_COLS).intersection(set(data.columns))
			return data[list(columns)]

		elif cols == "betting_cols":
			columns = set(BETTING_COLS).intersection(set(data.columns))
			return data[list(columns)]

	def get_data(self, cols="all"):
		columns = set(self.data.columns.tolist())

		data = self.data

		if cols == "sport_cols":
			columns = set(SPORT_COLS).intersection(set(data.columns))
			return self.data[list(columns)]

		elif cols == "betting_cols":
			columns = set(BETTING_COLS).intersection(set(data.columns))
			return self.data[list(columns)]

		elif cols == "all":
			return data

	def half_league_data(self, half):
		median_date = self.search_percentil_date(percentile=0.5)

		if half == 1:
			return self.data[self.data["Date"] <= median_date]
		elif half == 2:
			return self.data[self.data["Date"] > median_date]

	def search_percentil_date(self, percentile=0.5):
		#TODO - performance could be better

		dates = self.data["Date"].drop_duplicates().sort_values().tolist()
		best_date, best_diff = None, 100

		for date in dates:
			league_progress = league_progress_by_date(self.data, date)
			if abs(percentile - league_progress) < best_diff:
				best_date = date
				best_diff = abs(league_progress - percentile)

		return best_date

	def date_to_datetime(self, data):
		data["Date"] = pd.to_datetime(data["Date"], dayfirst=True)
		return data

	def slice_data_by_date(self, from_date, to_date):
		full_data = self.get_data()

		if from_date is None:
			from_date = min(full_data["Date"])

		elif isinstance(from_date, str):
			from_date = to_datetime(from_date, dayfirst=True)

		if to_date is None:
			to_date = max(full_data["Date"])

		elif isinstance(to_date, str):
			to_date = to_datetime(to_date, dayfirst=True)

		if from_date > to_date:
			raise Exception("from_date is higher than to_date")

		data = full_data[(full_data["Date"] >= from_date) & (full_data["Date"] <= to_date)]

		return data

	def teams(self):
		return self.get_data()["HomeTeam"].append(self.get_data()["AwayTeam"]).drop_duplicates().tolist()


