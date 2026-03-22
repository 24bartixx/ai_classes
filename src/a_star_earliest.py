import heapq
import math

import pandas as pd
from time import perf_counter

try:
    from .graph import Graph
except ImportError:
    from src.graph import Graph
    
try:
    from .utils import reconstruct_path
except ImportError:
    from src.utils import reconstruct_path
    


def a_star(start, finish, mode, time, graph=None, start_time_seconds=None, names_passed=False):    
    
    start_perf = perf_counter()
    
    date = time.date()
    if start_time_seconds is None:
        start_time_seconds = time.hour * 3600 + time.minute * 60 + time.second
        
    if start == finish:
        # No travel needed
        path = [{
            'from_stop_name': start,
            'to_stop_name': start,
            'arr_time': start_time_seconds,
            'dep_time': start_time_seconds,
            'line_name': '---'
        }]
        minimized_value = 0
        minimized_unit = 'seconds' if mode == 't' else 'transfers'
        exec_time = perf_counter() - start_perf
        return date, path, minimized_value, minimized_unit, exec_time

    if time >= pd.Timestamp('2026-12-13'):
        exec_time = perf_counter() - start_perf
        return date, [], float('inf'), 'seconds' if mode == 't' else 'transfers', exec_time

    if mode == 't':
        date, path, minimized_value = a_star_arr_time(start, finish, date, start_time_seconds, graph, names_passed)
        minimized_unit = 'seconds'
    elif mode == 'p':
        date, path, minimized_value = a_star_transfer(start, finish, date, start_time_seconds, graph, names_passed)
        minimized_unit = 'transfers'
    else:
        date, path, minimized_value = a_star_arr_time(start, finish, date, start_time_seconds, graph, names_passed)
        minimized_unit = 'seconds'

    exec_time = perf_counter() - start_perf
    return date, path, minimized_value, minimized_unit, exec_time

    
def a_star_arr_time(start, finish, date, start_time_seconds, graph = None, names_passed=False):
    
    def get_h(stop_id, finish_id, graph):    
        node = graph.graph[stop_id][0]
        finish = graph.graph[finish_id][0]
        
        lat1, lon1 = node['from_lat'], node['from_lon']
        lat2, lon2 = finish['from_lat'], finish['from_lon']

        avg_lat_rad = math.radians((lat1 + lat2) / 2.0)

        d_lat = lat2 - lat1
        d_lon = (lon2 - lon1) * math.cos(avg_lat_rad)
        
        km_distance = (d_lat**2 + d_lon**2)**0.5 * 111.32 
        
        # 160 km/h - max KD spped
        return (km_distance / 160) * 3600
    
    if graph is None:
        try:
            graph = Graph(date, with_locations=True)
        except FileNotFoundError:
            return (date, [], float('inf'))
        
    if names_passed:
        start_id = graph.stop_names_dict.get(start)
        finish_id = graph.stop_names_dict.get(finish)
    else:
        start_id = start
        finish_id = finish
    
    added_counter = 0
    while start_id not in graph.graph or finish_id not in graph.graph:
        if added_counter > 3:
            return (date, [], float('inf'))
        graph.load_next_day()
        added_counter += 1
        
    h_values = {}
    for node_id in graph.graph:
        h_values[node_id] = get_h(node_id, finish_id, graph)

    g_values = {start_id: start_time_seconds}
    f_values = {start_id: g_values[start_id] + h_values[start_id]}
    # (f_value, node)
    opened = [(f_values[start_id], start_id)]
    closed = set()
    came_from = {start_id: None}
    
    while True:
        while len(opened) > 0:
            _, node = heapq.heappop(opened)

            if node == finish_id:
                path = reconstruct_path(came_from, finish_id)
                minimized_value = g_values[finish_id] - start_time_seconds if finish_id in g_values else float('inf')
                return (date, path, minimized_value)

            if node in closed:
                continue

            closed.add(node)

            for edge in graph.graph.get(node, []):
                if edge['dep_time'] >= g_values[node]:
                    next_node = edge['to']

                    added_counter = 0
                    while next_node not in graph.graph:
                        if added_counter > 3:
                            return (date, [], float('inf'))
                        graph.load_next_day()
                        added_counter += 1

                    if next_node not in h_values:
                        h_values[next_node] = get_h(next_node, finish_id, graph)

                    if next_node not in g_values or g_values[next_node] > edge['arr_time']:
                        g_values[next_node] = edge['arr_time']
                        f_values[next_node] = g_values[next_node] + h_values[next_node]
                        came_from[next_node] = (node, edge)
                        if next_node not in closed:
                            heapq.heappush(opened, (f_values[next_node], next_node))
                        else:
                            closed.remove(next_node)
                            heapq.heappush(opened, (f_values[next_node], next_node))

        if graph.load_next_day():
            # readd all closed nodes to the heap
            for node in closed:
                heapq.heappush(opened, (f_values[node], node))
            closed.clear()
        else:
            break

    return (date, [], float('inf'))
        
        
def a_star_transfer(start, finish, date, start_time_seconds, graph = None, names_passed=False):
    
    def get_h(stop_id, finish_id, graph, stops_lines_dict):    
        node = graph[stop_id][0]
        finish = graph[finish_id][0]
        
        lat1, lon1 = node['from_lat'], node['from_lon']
        lat2, lon2 = finish['from_lat'], finish['from_lon']

        avg_lat_rad = math.radians((lat1 + lat2) / 2.0)

        d_lat = lat2 - lat1
        d_lon = (lon2 - lon1) * math.cos(avg_lat_rad)
        
        km_distance = (d_lat**2 + d_lon**2)**0.5 * 111.32 
        
        # 160 km/h - max KD spped
        time = (km_distance / 160) * 3600

        s_lines = stops_lines_dict.get(stop_id, [])
        f_lines = stops_lines_dict.get(finish_id, [])
        transfer_h = 0 if set(s_lines).intersection(f_lines) else 1
            
        return (transfer_h, time)
    
    if graph is None:
        try:
            graph = Graph(date, with_locations=True, include_stops_lines_dict=True)
        except FileNotFoundError:
            return (date, [], float('inf'))
        
    if names_passed:
        start_id = graph.stop_names_dict.get(start)
        finish_id = graph.stop_names_dict.get(finish)
    else:
        start_id = start
        finish_id = finish

    start_state = (start_id, None, None, start_time_seconds)
    
    g_values = {start_state: (0, start_time_seconds)}
    h_values = {start_state: (get_h(start_id, finish_id, graph.graph, graph.stops_lines_dict))}
    f_values = {start_state: (g_values[start_state][0] + h_values[start_state][0], g_values[start_state][1] + h_values[start_state][1])}
    
    tie_breaker = 0
    opened = [(f_values[start_state], tie_breaker, start_state)]
    closed = set()
    
    came_from = {start_state: None}
    
    while True:
        while len(opened) > 0:
            _, _, current_state = heapq.heappop(opened)
                
            node_id, last_line, last_trip_id, current_time = current_state

            if node_id == finish_id:
                path = reconstruct_path(came_from, current_state)
                minimized_value = g_values[current_state][0] if current_state in g_values else float('inf')
                return (date, path, minimized_value)

            if current_state in closed:
                continue

            closed.add(current_state)

            for edge in graph.graph.get(node_id, []):
                if edge['dep_time'] >= current_time:
                    next_node = edge['to']
                    current_line = edge['line_name']
                    current_trip_id = edge.get('trip_id')
                    next_state = (next_node, current_line, current_trip_id, edge['arr_time'])

                    transfer_cost = 1
                    if last_trip_id is None:
                        transfer_cost = 0
                    elif current_line == last_line and current_trip_id == last_trip_id:
                        transfer_cost = 0

                    new_g_transfers = g_values[current_state][0] + transfer_cost
                    new_g_time = edge['arr_time']
                    new_g = (new_g_transfers, new_g_time)

                    if next_state not in opened or new_g < g_values.get(next_state, (float('inf'), float('inf'))):
                        
                        g_values[next_state] = new_g
                        h = get_h(next_node, finish_id, graph.graph, graph.stops_lines_dict)
                        h_values[next_state] = h
                        f_values[next_state] = (new_g[0] + h[0], new_g[1] + h[1])
                        came_from[next_state] = (current_state, edge)
                        tie_breaker += 1
                        heapq.heappush(opened, (f_values[next_state], tie_breaker, next_state))
                        if next_state in closed:
                            closed.remove(next_state)

        if graph.load_next_day():
            for state in list(closed):
                tie_breaker += 1
                heapq.heappush(opened, (f_values[state], tie_breaker, state))
            heapq.heapify(opened)
            closed.clear()
        else:
            break

    return (date, [], float('inf'))