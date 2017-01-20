from datetime import timedelta

def next_day(date):
	return date + timedelta(days=1)

def previous_day(date):
	return date - timedelta(days=1)	
