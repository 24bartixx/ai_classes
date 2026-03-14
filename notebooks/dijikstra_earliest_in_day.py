import heapq

try:
    from .graph import Graph
except ImportError:
    from src.graph import Graph
    
try:
    from .utils import reconstruct_path
except ImportError:
    from src.utils import reconstruct_path
    

def dijkstra(start, finish, _, time):
    
    date = time.date()
    start_time_seconds = time.hour * 3600 + time.minute * 60 + time.second
    graph = Graph(date)
    
    d_arr_times = {node: float('inf') for node in graph.graph}
    d_arr_times[start] = start_time_seconds
    
    p_values = {node: None for node in graph.graph}
    
    # (arrival time, node)
    Q = [(start_time_seconds, start)]
    
    visited_nodes = {start}
    
    while True:
        while Q:
            arrival_time, stop = heapq.heappop(Q)
            
            if arrival_time > d_arr_times.get(stop, float('inf')):
                continue
            
            if stop == finish:
                return (date, reconstruct_path(p_values, finish))

            for edge in graph.graph.get(stop, []):
                if edge['dep_time'] >= arrival_time:
                    next_stop = edge['to']
                    
                    if d_arr_times[next_stop] > edge['arr_time']:
                        d_arr_times[next_stop] = edge['arr_time']
                        p_values[next_stop] = (stop, edge)
                        heapq.heappush(Q, (edge['arr_time'], next_stop))
                        visited_nodes.add(next_stop)
                        
        graph.load_next_day()
        
        for node in visited_nodes:
            heapq.heappush(Q, (d_arr_times[node], node))
            

def dijkstra_transfer(start, finish, _, time):
    date = time.date()
    start_time_seconds = time.hour * 3600 + time.minute * 60 + time.second
    graph = Graph(date)

    # State: (stop_id, current_line_name)
    start_state = (start, None)

    # Cost is lexicographic: (number_of_transfers, arrival_time)
    best_cost = {start_state: (0, start_time_seconds)}
    came_from = {start_state: None}

    # (transfers, arrival_time, stop_id, current_line_name)
    Q = [(0, start_time_seconds, start, None)]

    visited_stops = {start}

    while True:
        while Q:
            transfers, arrival_time, stop, current_line = heapq.heappop(Q)
            state = (stop, current_line)

            if (transfers, arrival_time) > best_cost.get(state, (float('inf'), float('inf'))):
                continue

            if stop == finish:
                path = []
                cur = state
                while came_from[cur] is not None:
                    prev_state, edge = came_from[cur]
                    path.append(edge)
                    cur = prev_state
                path.reverse()
                return (date, path)

            for edge in graph.graph.get(stop, []):
                if edge['dep_time'] < arrival_time:
                    continue

                next_stop = edge['to']
                next_line = edge.get('line_name')
                transfer_cost = 0 if current_line is None or current_line == next_line else 1

                next_state = (next_stop, next_line)
                next_cost = (transfers + transfer_cost, edge['arr_time'])

                if next_cost < best_cost.get(next_state, (float('inf'), float('inf'))):
                    best_cost[next_state] = next_cost
                    came_from[next_state] = (state, edge)
                    heapq.heappush(Q, (next_cost[0], next_cost[1], next_stop, next_line))
                    visited_stops.add(next_stop)

        if not graph.load_next_day():
            break

        for (stop, line), (transfers, arr_time) in best_cost.items():
            if stop in visited_stops:
                heapq.heappush(Q, (transfers, arr_time, stop, line))

    return (date, [])
        
