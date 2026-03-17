import random
import pandas as pd


try:
    from .graph import Graph
except ImportError:
    from src.graph import Graph
    
try:
    from .a_star_earliest import a_star
except ImportError:
    from src.a_star_earliest import a_star
    
def evaluate_solution(solution, graph, time, should_log=False):
    
    start_seconds = time.hour * 3600 + time.minute * 60 + time.second
    last_arr_time = start_seconds
    
    for i in range(len(solution) - 1):
        start_id = solution[i]
        finish_id = solution[i + 1]
        
        result = a_star(start_id, finish_id, 't', time, graph, last_arr_time)
        
        if not result or not result[1]:
            return pd.Timestamp("2300-12-12")
        
        date, path = result

        last_arr_time = path[-1]['arr_time']
        
        if should_log:
            dep_time = time + pd.Timedelta(seconds=path[-1]['dep_time'] - start_seconds)
            arr_time = time + pd.Timedelta(seconds=last_arr_time - start_seconds)

            print(f"Path from {start_id} to {finish_id}, {date} {dep_time} - {arr_time}")
        
    return time + pd.Timedelta(seconds=last_arr_time - (time.hour * 3600 + time.minute * 60 + time.second))


def tabu_a(start, stops, _, time):
    
    date = time.date()
    start_time_seconds = time.hour * 3600 + time.minute * 60 + time.second
    try:
        graph = Graph(date, with_locations=True)
    except FileNotFoundError:
        ... # handle error, e.g. return no solution
    
    best_solution = stops
    
    no_change_count = 0
    
    while no_change_count < 100:
        
        # swap
        new_solution = best_solution[:]
        i, j = random.sample(range(len(stops)), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        
        # evaluate
    
    