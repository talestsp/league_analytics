import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from pandas import Series
from plot.plot import PlotDataMultiLine
from plot.plot_data import PlotData
from dao.dao import DAO
from league import League

class LeaguePlot:

	def __init__(self, country, season, n_round=None):
		self.country = country
		self.season = season
		self.n_round = n_round

		dao = DAO(country=country, season=season, cols="sport_cols")
		self.league = League(dao)

	def plot_cumulative_points(self, clubs_positions=[1,2,3,4,5], width=1000, height=700, plot=True):
		to_date = self.league.date_by_round(n_round=self.n_round)
		league_table = self.league.table(to_date=to_date)
		multi_plot_data = []

		for team in league_table["Team"].loc[clubs_positions]:
			team_points = self.league.team_history_points(team, to_date=to_date)["Points"].cumsum()
			#every team starts with zero points
			team_points = Series([0]).append(team_points)
			multi_plot_data.append(PlotData(x=list(map(str, range(0, len(team_points)))), y=team_points, legend=team))

		pl = PlotDataMultiLine(plot_data_list=multi_plot_data, x_label="match no", y_label="points", 
							   title=self.country + " " + self.season + " cumulative points")

		max_x = len(team_points)
		max_y = max([y for y in multi_plot_data[0].y])

		pl.plot(max_x=max_x, max_y=max_y * 1.05, fig_width=width, fig_height=height, plot=plot)

if __name__ == "__main__":
	lp = LeaguePlot(country="england", n_round=19, season="16-17")
	lp.plot_cumulative_points()


