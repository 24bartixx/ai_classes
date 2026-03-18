from math import comb
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
    
def evaluate_solution_arr_time(solution, graph, time, should_log=False, names_passed=False):
    
    start_seconds = time.hour * 3600 + time.minute * 60 + time.second
    last_arr_time = start_seconds
    
    for i in range(len(solution) - 1):
        start_id = solution[i]
        finish_id = solution[i + 1]
        
        result = a_star(start_id, finish_id, 't', time, graph, last_arr_time, names_passed=names_passed)
        
        if not result or not result[1]:
            return pd.Timestamp("2300-12-12")
        
        date, path = result

        last_arr_time = path[-1]['arr_time']
        
        if should_log:
            dep_time = time + pd.Timedelta(seconds=path[-1]['dep_time'] - start_seconds)
            arr_time = time + pd.Timedelta(seconds=last_arr_time - start_seconds)

            print(f"Path from {start_id} to {finish_id}, {date} {dep_time} - {arr_time}")
        
    return time + pd.Timedelta(seconds=last_arr_time - (time.hour * 3600 + time.minute * 60 + time.second))


def get_neighbors(solution):
    n = len(solution)
    
    if n < 3:
        return {}
    
    valid_indices = list(range(1, n - 1))
    total_possible = comb(len(valid_indices), 2)
    neighbors_count = max(1, int(total_possible * 0.2))
    
    selected_pairs = set()
    while len(selected_pairs) < neighbors_count:
        i, j = sorted(random.sample(valid_indices, 2))
        selected_pairs.add((i, j))
    
    neighbors = {}
    for i, j in selected_pairs:
        new_solution = solution[:]
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        neighbors[(i, j)] = new_solution
        
    return neighbors

def tabu_a(start, stops, mode, time, names_passed=False):
    if start not in stops:
        print("Start stop is not in the list of stops.")
        return
        
    # move start to the beginning
    stops[stops.index(start)], stops[0] = stops[0], stops[stops.index(start)]
    
    # ensure the last stop is the same as the start
    if stops[-1] != start:
        stops.append(start)
    
    # initialize graph
    try:
        graph = Graph(time, with_locations=True)
    except FileNotFoundError:
        print("Graph file not found. Returning no solution.")
        return None, None
    
    best_solution = stops
    best_score = evaluate_solution_arr_time(best_solution, graph, time, should_log=False, names_passed=names_passed)
    
    if(best_score > pd.Timestamp("2026-12-13")):
        print(best_score)
        return None, None
    
    tabu = []
    tabu_tabu_size = len(stops) * 2
    
    no_change_count = 0
    counter  = 0
    
    while no_change_count < 10:
        locally_best_score = evaluate_solution_arr_time(best_solution, graph, time, should_log=False, names_passed=names_passed)
        locally_best_solution = best_solution
            
        i = 0
        while i < 7:
            counter += 1
            print(counter)
            
            neighbors = get_neighbors(best_solution)
            
            to_tabu = None
            best_neighbor = None
            best_neighbor_score = pd.Timestamp("2300-12-12")
            
            for changed_indexes, neighbor in neighbors.items():
                
                neighbor_score = evaluate_solution_arr_time(neighbor, graph, time, should_log=False, names_passed=names_passed)
                
                if neighbor_score < best_neighbor_score:
                    if changed_indexes not in tabu or neighbor_score < best_score:
                        best_neighbor = neighbor
                        best_neighbor_score = neighbor_score
                        to_tabu = changed_indexes                   
                  
            if to_tabu is not None:  
                tabu.append(to_tabu)
                if len(tabu) > tabu_tabu_size:
                    tabu.pop(0)
                
            if best_neighbor_score < locally_best_score:
                locally_best_score = best_neighbor_score
                locally_best_solution = best_neighbor
                
            i += 1
                
        no_change_count += 1
        
        if locally_best_score < best_score:
            best_score = locally_best_score
            best_solution = locally_best_solution
            no_change_count = 0
            
    paths = []
    for i in range(len(best_solution) - 1):
        a_star_result = a_star(best_solution[i], best_solution[i + 1], 't', time, graph, names_passed=names_passed)
        paths.append(a_star_result)
                
    return best_solution, best_score, paths