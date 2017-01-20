from dao.dao import DAO
from grouped_stats import GroupedStats
from table import Table
from dates import next_day
from analysis import Analysis, CORRELATION_H1_H2, CORRELATION_H1_FULL, CORRELATION_H2_FULL

dao = DAO(country="england", season="15-16", cols="sport_cols")
stats = GroupedStats(dao.get_data())

print("")

table = Table(dao)
points = table.points()
print ("Final table")
print (points)
print()

### FIRST HALF LEAGUE
half_league_date = table.half_league_date()
print(half_league_date)

eng_points_h1 = table.points(to_date=half_league_date)
eng_points_h2 = table.points(from_date=next_day(half_league_date))

print("England First Half")
print(eng_points_h1.sort_values(by="Points", ascending=False))
print()
print("England Second Half")
print(eng_points_h2.sort_values(by="Points", ascending=False))
print()

print("Correlation between first half and second half points")
print("Corr pearson: ", eng_points_h1["Points"].corr(eng_points_h2["Points"], method="pearson"))
print("Corr spearman:", eng_points_h1["Points"].corr(eng_points_h2["Points"], method="spearman"))
print()

print("Correlation between first half and full league")
print("Corr pearson: ", eng_points_h1["Points"].corr(points["Points"], method="pearson"))
print("Corr spearman:", eng_points_h1["Points"].corr(points["Points"], method="spearman"))
print()

print("Correlation between second half and full league")
print("Corr pearson: ", eng_points_h2["Points"].corr(points["Points"], method="pearson"))
print("Corr spearman:", eng_points_h2["Points"].corr(points["Points"], method="spearman"))
print()

# #goals scored 
# data["FTHG"].mean()
# data["FTAG"].mean()

# #shots
# data["HS"].mean()
# data["AS"].mean()

# #shots on target
# data["HST"].mean()
# data["AST"].mean()

# #rate shots on target / shots
# data["HST"].sum() / data["HS"].sum()
# data["AST"].sum() / data["AS"].sum()

# #rate goals / shots
# data["FTHG"].sum() / data["HS"].sum()
# data["FTAG"].sum() / data["AS"].sum()

# #rate goals / shots on target
# data["FTHG"].sum() / data["HST"].sum()
# data["FTAG"].sum() / data["AST"].sum()
