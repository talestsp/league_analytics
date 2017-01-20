from pandas import DataFrame, merge

def series_to_dataframe(series, colname):
	index = series.index
	values = series.values

	return DataFrame({series.index.name: index, colname: values})[[series.index.name, colname]]

def merge_series(series_list, on, how):
	series_merged = series_to_dataframe(series=series_list[0]["series"], colname=series_list[0]["colname"])

	for series in series_list[1:]:
		df = series_to_dataframe(series=series["series"], colname=series["colname"])
		series_merged = merge(series_merged, df, on=on, how=how)

	return series_merged

def league_progress_by_date(data, date):
	if isinstance(date, str):
		date = to_datetime(date, dayfirst=True)

	total = float(len(data))
	return len(data[data["Date"] <= date]) / total

def mean_deviation(series):
	mean = series.mean()
	deviation = series.apply(lambda value: abs(value - mean))
	return deviation.mean()