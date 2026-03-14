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
        
