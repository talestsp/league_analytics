import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from pandas import Series
from plot.plot import PlotDataMultiLine
from plot.plot_data import PlotData

class LeaguePlot:

	def plot_cumulative_points(league, to_date, clubs_positions=[1,2,3,4,5], width=1000, height=700, max_y=None, plot=True):
		multi_plot_data = []
		league_table = league.table(to_date=to_date)

		for team in league_table["Team"].loc[clubs_positions]:
			team_points = league.team_history_points(team, to_date=to_date)["Points"].cumsum()
			#every team starts with zero points
			team_points = Series([0]).append(team_points)
			x = list(map(str, range(0, len(team_points))))
			multi_plot_data.append(PlotData(x=range(0, len(team_points)), y=team_points, legend=team))

		pl = PlotDataMultiLine(plot_data_list=multi_plot_data, x_label="match no", y_label="points", 
							   title=league.country + " " + league.season + " cumulative points")

		max_x = len(team_points)

		if max_y is None:
			max_points = max([y for y in multi_plot_data[0].y])
		else:
			max_points = max_y

		pl.plot(max_x=max_x, max_y=max_points * 1.05, fig_width=width, fig_height=height, plot=plot)

if __name__ == "__main__":
	lp = LeaguePlot(country="england", n_round=19, season="16-17")
	lp.plot_cumulative_points()


