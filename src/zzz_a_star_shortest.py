import heapq
import math

try:
    from .graph import Graph
except ImportError:
    from src.graph import Graph
    
def get_h(stop_id, finish_id, graph):
    node = graph[stop_id][0]
    finish = graph[finish_id][0]
    
    lat1, lon1 = node['from_lat'], node['from_lon']
    lat2, lon2 = finish['from_lat'], finish['from_lon']

    avg_lat_rad = math.radians((lat1 + lat2) / 2.0)

    d_lat = lat2 - lat1
    d_lon = (lon2 - lon1) * math.cos(avg_lat_rad)
    
    # Heurisic: km distance
    km_distance = (d_lat**2 + d_lon**2)**0.5 * 111.32 
    
    # 160 km/h - max KD spped
    return (km_distance / 160) * 3600

def a_star(start, finish, _, time):
    
    date = time.date()
    start_time_seconds = time.hour * 3600 + time.minute * 60 + time.second
    graph = Graph(date, with_locations=True)
    
    # (f cost, duration, arrival time, node)
    start_f = get_h(start, finish, graph.graph)
    opened = [(start_f, 0, start_time_seconds, start)]
    closed = set()

    g_costs = {node: float('inf') for node in graph.graph}
    g_costs[start] = 0
    
    came_from = {node: None for node in graph.graph}
    
    while len(opened) > 0:
        f_score, g_score, arrival_time, node  = heapq.heappop(opened)
        
        if node in closed:
            continue
    
        if node == finish:
            break
        
        closed.add(node)
        
        for edge in graph.graph.get(node, []):
            v = edge['to']
            
            if edge['dep_time'] >= arrival_time:
                
                g_score_diff = edge['arr_time'] - arrival_time if node != start else edge['arr_time'] - edge['dep_time']
                new_g_score = g_score + g_score_diff
                
                if new_g_score < g_costs[v]:
                        g_costs[v] = new_g_score
                        h_score = get_h(v, finish, graph.graph)
                        f_score = new_g_score + h_score
                        
                        came_from[v] = (node, edge)
                        heapq.heappush(opened, (f_score, new_g_score, edge['arr_time'], v))
                   
    path = []
    current = finish
    while current is not None:
        entry = came_from[current]
        if entry is None:
            break
        prev_node, edge = entry
        path.append(edge)
        current = prev_node
    path.reverse()

    return date, path
            
    