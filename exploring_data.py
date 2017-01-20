import pandas as pd
from dao.dao import DAO
from table import Table

data = DAO().get_data("spain", "15-16", cols="sport_cols")
print(data.head())

table = Table(data)
table.league_progress_by_date("15/01/2016")
table.matches_played("15/01/2016")
