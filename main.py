from src.graph import load_calendar_data


if __name__ == "__main__":
	df = load_calendar_data()
	print(df.head())
