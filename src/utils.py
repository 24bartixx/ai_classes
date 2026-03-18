from importlib.resources import path
from unittest import result

import pandas as pd


def time_to_seconds(time_str: str) -> int:
	hours, minutes, seconds = map(int, time_str.split(":"))
	return hours * 3600 + minutes * 60 + seconds

def seconds_to_time(seconds: int) -> str:
	hours, remainder = divmod(seconds, 3600)
	minutes, secs = divmod(remainder, 60)
	return f"{hours%24:02}:{minutes:02}:{secs:02}"

def print_path(result, should_print_optimal_time=True):
	if not result:
		print("No connection found")
		return

	date, path = result

	if not path:
		print(f"No available connections for given time")
		return

	if should_print_optimal_time:
		print(f"Optimal path: {seconds_to_time(path[0]['dep_time'])} - {seconds_to_time(path[-1]['arr_time'])}\n")

	for step in path:
		print(f'Line:\t\t{step["line_name"]}')
		print(f'Stops:\t\t{step["from_stop_name"]} ---> {step["to_stop_name"]}')
		print(f'Dates:\t\t{date + pd.Timedelta(days=(step["dep_time"] // 86400))} - {date + pd.Timedelta(days=(step["arr_time"] // 86400))}')
		print(f'Times:\t\t{seconds_to_time(step["dep_time"])} - {seconds_to_time(step["arr_time"])}')
		print()
  
def print_paths(result, should_print_path=False):
    
	best_solution, best_score, paths = result
 
	print("Fastest arrival: " + str(best_score))
 
	print("\nBest city order:")
	for i, stop in enumerate(best_solution):
		print(f"\t{i+1}. {stop}")
  
	if should_print_path:
		for path in paths:
			print(F"\n===== {path[1][0]['from_stop_name']} =====\n")
			print_path(path, should_print_optimal_time=False)
	
  
  
def print_lines(result):
	if not result:
		print("No connection found")
		return

	_, path = result

	if not path:
		print(f"No available connections for given time")
		return

	print(f"Optimal path: {seconds_to_time(path[0]['dep_time'])} - {seconds_to_time(path[-1]['arr_time'])}\n")

	lines = []

	for step in path:
		if step['line_name'] not in lines:
			lines.append(step['line_name'])
   
	print("Lines used: " + ", ".join(lines))
  
def reconstruct_path(come_from, finish):
    path = []
    current = finish
    while current is not None:
        entry = come_from[current]
        if entry is None:
            break
        prev_node, edge = entry
        path.append(edge)
        current = prev_node
    path.reverse()

    return path