from importlib.resources import path


def time_to_seconds(time_str: str) -> int:
	hours, minutes, seconds = map(int, time_str.split(":"))
	return hours * 3600 + minutes * 60 + seconds

def seconds_to_time(seconds: int) -> str:
	hours, remainder = divmod(seconds, 3600)
	minutes, secs = divmod(remainder, 60)
	return f"{hours:02}:{minutes:02}:{secs:02}"

def print_path(path):

	print(f"Optimal path: {seconds_to_time(path[0]['dep_time'])} - {seconds_to_time(path[-1]['arr_time'])}\n")
	

	for step in path:
		print(f'{step["line_name"]}\t{seconds_to_time(step["dep_time"])} - {seconds_to_time(step["arr_time"])}\t{step["from_stop_name"]} ---> {step["to_stop_name"]}')