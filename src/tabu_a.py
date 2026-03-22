from time import perf_counter
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
    
def evaluate_solution_arr_time(solution, mode, graph, time, should_log=False, names_passed=False):
    
    start_seconds = time.hour * 3600 + time.minute * 60 + time.second
    last_arr_time = start_seconds

    # Use a_star_cache if available in graph, else fallback to no cache
    a_star_cache = getattr(graph, '_a_star_cache', None)
    if a_star_cache is None:
        a_star_cache = {}
        setattr(graph, '_a_star_cache', a_star_cache)

    for i in range(len(solution) - 1):
        start_id = solution[i]
        finish_id = solution[i + 1]
        cache_key = (start_id, finish_id, last_arr_time)
        if cache_key in a_star_cache:
            result = a_star_cache[cache_key]
        else:
            result = a_star(start_id, finish_id, mode, time, graph, last_arr_time, names_passed=names_passed)
            a_star_cache[cache_key] = result

        if not result or not result[1]:
            return pd.Timestamp("2300-12-12")

        date, path, _, _, _ = result
        last_arr_time = path[-1]['arr_time']

        if should_log:
            dep_time = time + pd.Timedelta(seconds=path[-1]['dep_time'] - start_seconds)
            arr_time = time + pd.Timedelta(seconds=last_arr_time - start_seconds)
            print(f"Path from {start_id} to {finish_id}, {date} {dep_time} - {arr_time}")

    return time + pd.Timedelta(seconds=last_arr_time - (time.hour * 3600 + time.minute * 60 + time.second))


def normalize_edge(a, b):
    return (a, b) if a < b else (b, a)


def get_neighbors(solution, sample=True, sample_ratio=0.45, min_neighbors=10):
    n = len(solution)
    if n < 4:
        return []

    valid_moves = [
        (i, j)
        for i in range(1, n - 2)
        for j in range(i + 1, n - 1)
    ]

    total_moves = len(valid_moves)
    if sample:
        neighbors_count = max(min_neighbors, int(total_moves * sample_ratio))
        neighbors_count = min(neighbors_count, total_moves)
        moves = random.sample(valid_moves, neighbors_count)
    else:
        moves = valid_moves

    neighbors = list()
    for i, j in moves:
        new_solution = solution[:]
        new_solution[i:j + 1] = reversed(new_solution[i:j + 1])
        to_tabu = (
            normalize_edge(solution[i - 1], solution[i]),
            normalize_edge(solution[j], solution[j + 1])
        )
        neighbors.append((to_tabu, new_solution))

    return neighbors

def tabu_a(
        start, 
        stops, 
        mode, 
        time, 
        names_passed=False, 
        should_log=False, 
        limited_tabu_size=False, 
        should_aspiration=False, 
        sample_neighbors=False, 
        sample_ratio=0.2,
        graph=None
    ):
    
    start_perf = perf_counter()

    if start not in stops:
        print("Start stop is not in the list of stops.")
        exec_time = perf_counter() - start_perf
        return None, None, None, None, None, exec_time

    # move start to the beginning
    stops = stops[:]
    stops[stops.index(start)], stops[0] = stops[0], stops[stops.index(start)]

    # ensure the last stop is the same as the start
    if stops[-1] != start:
        stops.append(start)
    
    if graph is None:
        try:
            if mode == 'p':
                graph = Graph(time, with_locations=False, include_stops_lines_dict=True)
            else:
                graph = Graph(time, with_locations=True)
        except FileNotFoundError:
            print("Graph file not found. Returning no solution.")
            exec_time = perf_counter() - start_perf
            return None, None, None, None, None, exec_time
    
    best_solution = stops[:]
    best_score = evaluate_solution_arr_time(best_solution, mode, graph, time, should_log=False, names_passed=names_passed)
    
    current_solution = stops[:]
    current_score = best_score
    
    if(best_score > pd.Timestamp("2026-12-13")):
        print(best_score)
        exec_time = perf_counter() - start_perf
        return None, None, None, None, None, exec_time

    tabu = []
    max_tabu_size = len(stops) * 5
        
    no_change_count = 0
    while no_change_count < 80:
        locally_best_score = current_score
        locally_best_solution = current_solution[:]
        
        neighbors_iter_count = 0
        while neighbors_iter_count < 10:
            
            best_neighbor = None
            best_neighbor_score = pd.Timestamp("2300-12-12")
            
            neighbors = get_neighbors(locally_best_solution, sample=sample_neighbors, sample_ratio=sample_ratio)
            to_tabu = None
            
            for to_tabu_candidate, neighbor in neighbors:
                neighbor_score = evaluate_solution_arr_time(neighbor, mode, graph, time, should_log=False, names_passed=names_passed)
                
                not_in_tabu = to_tabu_candidate not in tabu
                allowed_by_aspiration = should_aspiration and neighbor_score < best_score
                
                if (not_in_tabu or allowed_by_aspiration) and neighbor_score < best_neighbor_score:
                    best_neighbor = neighbor
                    best_neighbor_score = neighbor_score
                    
            
            to_tabu = to_tabu_candidate
                    
            if to_tabu is not None:
                tabu.append(to_tabu)
                if limited_tabu_size and len(tabu) > max_tabu_size:
                    tabu.pop(0)
                    
            if best_neighbor is not None:
                locally_best_score = best_neighbor_score
                locally_best_solution = best_neighbor[:]
            
            neighbors_iter_count += 1
            
        current_solution = locally_best_solution[:]
        current_score = locally_best_score
        
        # mixup if no progress
        if no_change_count % 25 == 0:
            for i in range(3):
                i = random.randint(1, len(current_solution) - 3)
                j = random.randint(i + 1, len(current_solution) - 2)
                
                while(i == j):
                    j = random.randint(i + 1, len(current_solution) - 2)
                    
                current_solution[i:j + 1] = reversed(current_solution[i:j + 1])
                current_score = evaluate_solution_arr_time(current_solution, mode, graph, time, should_log=False, names_passed=names_passed)
        
        no_change_count += 1

        if current_score < best_score:
            print(f"New best score: {current_score} at iteration with no change count: {no_change_count}")
            best_score = current_score
            best_solution = current_solution[:]

            no_change_count = 0
            
    if should_log:
        print()

    paths = []
    for i in range(len(best_solution) - 1):
        a_star_result = a_star(best_solution[i], best_solution[i + 1], mode, time, graph, names_passed=names_passed)
        paths.append(a_star_result)

    minimized_value = best_score
    minimized_unit = 'seconds'
    exec_time = perf_counter() - start_perf
    
    return best_solution, best_score, paths, minimized_value, minimized_unit, exec_time