import random


try:
    from .graph import build_graph
except ImportError:
    from src.graph import build_graph
    
def evaluate_solution(solution, graph, start_time_seconds):
    ...

def tabu_a(start, stops, _, time):
    
    date = time.date()
    start_time_seconds = time.hour * 3600 + time.minute * 60 + time.second
    graph = build_graph(date, with_locations=True)
    
    best_solution = stops
    
    no_change_count = 0
    
    while no_change_count < 100:
        
        # swap
        new_solution = best_solution[:]
        i, j = random.sample(range(len(stops)), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        
        # evaluate
    
    