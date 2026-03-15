import heapq

try:
    from .graph import Graph
except ImportError:
    from src.graph import Graph
    
try:
    from .utils import reconstruct_path
except ImportError:
    from src.utils import reconstruct_path
    
    
def dijkstra(start, finish, mode, time):
    date = time.date()
    start_time_seconds = time.hour * 3600 + time.minute * 60 + time.second
    
    try:
        graph = Graph(date)
    except FileNotFoundError:
        return (date, [])

    if mode == 'p':
        return dijkstra_transfer(start, finish, date, start_time_seconds, graph)
    elif mode == 't':
        return dijkstra_arr_time(start, finish, date, start_time_seconds, graph)
    
    return dijkstra_arr_time(start, finish, date, start_time_seconds, graph)
    

def dijkstra_arr_time(start, finish, date, start_time_seconds, graph):
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
                        
        if not graph.load_next_day():
            break
        
        for node in visited_nodes:
            heapq.heappush(Q, (d_arr_times[node], node))
            
    return (date, [])
            

def dijkstra_transfer(start, finish, date, start_time_seconds, graph):
    start_state = (start, None)
    d_states = {start_state: (0, start_time_seconds)}
    
    came_from = {start_state: None}

    Q = [(0, start_time_seconds, start, None)]

    visited_stops = {start}

    while True:
        while Q:
            transfers, arrival_time, stop, current_line = heapq.heappop(Q)
            state = (stop, current_line)

            if (transfers, arrival_time) > d_states.get(state, (float('inf'), float('inf'))):
                continue

            if stop == finish:
                return (date, reconstruct_path(came_from, state))

            for edge in graph.graph.get(stop, []):
                if edge['dep_time'] < arrival_time:
                    continue

                next_stop = edge['to']
                next_line = edge.get('line_name')
                transfer_cost = 0 if current_line is None or current_line == next_line else 1

                next_state = (next_stop, next_line)
                next_cost = (transfers + transfer_cost, edge['arr_time'])

                if next_cost < d_states.get(next_state, (float('inf'), float('inf'))):
                    d_states[next_state] = next_cost
                    came_from[next_state] = (state, edge)
                    heapq.heappush(Q, (next_cost[0], next_cost[1], next_stop, next_line))
                    visited_stops.add(next_stop)

        if not graph.load_next_day():
            break

        for (stop, line), (transfers, arr_time) in d_states.items():
            if stop in visited_stops:
                heapq.heappush(Q, (transfers, arr_time, stop, line))

    return (date, [])
        
