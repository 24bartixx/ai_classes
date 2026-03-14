import heapq
import math

try:
    from .graph import Graph
except ImportError:
    from src.graph import Graph
    
try:
    from .utils import reconstruct_path
except ImportError:
    from src.utils import reconstruct_path
    
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
    
    g_values = {start: start_time_seconds}
    h_values = {start: get_h(start, finish, graph.graph)}
    f_values = {start: g_values[start] + h_values[start]}
    
    opened = [start]
    closed = []
    
    came_from = {start: None}
    
    while True:
        while len(opened) > 0:
            node = min(opened, key=lambda x: f_values.get(x, float('inf')))
            
            if node == finish:
                return (date, reconstruct_path(came_from, finish))
            
            opened.remove(node)
            closed.append(node)
            
            for edge in graph.graph.get(node, []):
                if edge['dep_time'] >= g_values[node]:
                    next_node = edge['to']

                    if next_node not in opened and next_node not in closed:
                        opened.append(next_node)
                        g_values[next_node] = edge['arr_time']
                        h_values[next_node] = get_h(next_node, finish, graph.graph)
                        f_values[next_node] = g_values[next_node] + h_values[next_node]
                        came_from[next_node] = (node, edge)

                    else:
                        if g_values[next_node] > edge['arr_time']:
                            g_values[next_node] = edge['arr_time']
                            f_values[next_node] = g_values[next_node] + h_values[next_node]
                            came_from[next_node] = (node, edge)

                            if next_node in closed:
                                closed.remove(next_node)
                                opened.append(next_node)
                                
        if graph.load_next_day():
            opened = closed
            closed = []
        else:
            break
        
    return (date, [])
        
        
def a_star_transfer(start, finish, date, start_time_seconds):
    graph = Graph(date, with_locations=True)
    
    g_values = {start: start_time_seconds}
    h_values = {start: get_h(start, finish, graph.graph)}
    f_values = {start: g_values[start] + h_values[start]}
    
    opened = [start]
    closed = []
    
    came_from = {start: None}
    
    while True:
        while len(opened) > 0:
            node = min(opened, key=lambda x: f_values.get(x, float('inf')))
            
            if node == finish:
                return (date, reconstruct_path(came_from, finish))
            
            opened.remove(node)
            closed.append(node)
            
            for edge in graph.graph.get(node, []):
                if edge['dep_time'] >= g_values[node]:
                    next_node = edge['to']

                    if next_node not in opened and next_node not in closed:
                        opened.append(next_node)
                        g_values[next_node] = edge['arr_time']
                        h_values[next_node] = get_h(next_node, finish, graph.graph)
                        f_values[next_node] = g_values[next_node] + h_values[next_node]
                        came_from[next_node] = (node, edge)

                    else:
                        if g_values[next_node] > edge['arr_time']:
                            g_values[next_node] = edge['arr_time']
                            f_values[next_node] = g_values[next_node] + h_values[next_node]
                            came_from[next_node] = (node, edge)

                            if next_node in closed:
                                closed.remove(next_node)
                                opened.append(next_node)
                                
        if graph.load_next_day():
            opened = closed
            closed = []
        else:
            break
        
    return (date, [])
    
    
    