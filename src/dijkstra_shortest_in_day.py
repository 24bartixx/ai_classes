import heapq

try:
    from .graph import get_graph_for_date
except ImportError:
    from src.graph import get_graph_for_date


def dijkstra(start, finish, _, time):
    
    date = time.date()
    start_time_seconds = time.hour * 3600 + time.minute * 60 + time.second
    graph = get_graph_for_date(date)
    
    d_durations = {node: float('inf') for node in graph}
    d_durations[start] = 0
    
    p_values = {node: None for node in graph}
    
    # (duration, arrival time, node)
    Q = [(0, start_time_seconds, start)]
    
    while Q:
        duration, arrival_time, u = heapq.heappop(Q)

        for edge in graph.get(u, []):
            if edge['dep_time'] >= arrival_time:
                v = edge['to']
                
                if u == start:
                    cost = edge['arr_time'] - edge['dep_time']
                else:
                    cost = edge['arr_time'] - arrival_time
                
                newDuration = duration + cost
                
                if newDuration < d_durations[v]:
                    d_durations[v] = newDuration
                    p_values[v] = (u, edge)
                    heapq.heappush(Q, (newDuration, edge['arr_time'], v))

    path = []
    current = finish
    while current is not None:
        entry = p_values[current]
        if entry is None:
            break
        prev_node, edge = entry
        path.append(edge)
        current = prev_node
    path.reverse()

    return date, path
    