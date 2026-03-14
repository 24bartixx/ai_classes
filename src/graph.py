from datetime import date
from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_data_path(file_path: str | Path) -> Path:
	path = Path(file_path)
	if path.is_absolute():
		return path

	# First respect caller's CWD, then fall back to project-root-relative paths.
	cwd_path = Path.cwd() / path
	if cwd_path.exists():
		return cwd_path

	return PROJECT_ROOT / path

try:
    from .utils import time_to_seconds
except ImportError:
    from src.utils import time_to_seconds


# ===== DATA LOADING FUNCTIONS =====

def load_calendar_data(file_path: str | Path = "data/calendar.txt") -> pd.DataFrame:

	path = resolve_data_path(file_path)
	if not path.exists():
		raise FileNotFoundError(f"Calendar file not found: {path}")

	calendar_df = pd.read_csv(path)
	calendar_df["start_date"] = pd.to_datetime(
		calendar_df["start_date"], format="%Y%m%d", errors="coerce"
	)
	calendar_df["end_date"] = pd.to_datetime(
		calendar_df["end_date"], format="%Y%m%d", errors="coerce"
	)
	return calendar_df

def load_calendar_exceptions_data(file_path: str | Path = "data/calendar_dates.txt") -> pd.DataFrame:
	path = resolve_data_path(file_path)
	if not path.exists():
		raise FileNotFoundError(f"Calendar file not found: {path}")

	calendar_exceptions_df = pd.read_csv(path)
 
	calendar_exceptions_df["date"] = pd.to_datetime(
		calendar_exceptions_df["date"], format="%Y%m%d", errors="coerce"
	)
 
	return calendar_exceptions_df

def load_trips_data(file_path: str | Path = "data/trips.txt") -> pd.DataFrame:

	path = resolve_data_path(file_path)
	if not path.exists():
		raise FileNotFoundError(f"Trips file not found: {path}")

	trips_df = pd.read_csv(path)
 
	return trips_df

def load_stop_times_data(file_path: str | Path = "data/stop_times.txt") -> pd.DataFrame:

	path = resolve_data_path(file_path)
	if not path.exists():
		raise FileNotFoundError(f"Stop times file not found: {path}")

	stop_times_df = pd.read_csv(path)
 
	return stop_times_df

def load_stop_data(file_path: str | Path = "data/stops.txt") -> pd.DataFrame:

	path = resolve_data_path(file_path)
	if not path.exists():
		raise FileNotFoundError(f"Stops file not found: {path}")

	stops_df = pd.read_csv(path)
 
	return stops_df

def load_routes_data(file_path: str | Path = "data/routes.txt") -> pd.DataFrame:

	path = resolve_data_path(file_path)
	if not path.exists():
		raise FileNotFoundError(f"Routes file not found: {path}")

	routes_df = pd.read_csv(path)
 
	return routes_df

def build_parent_station_map(stops_df: pd.DataFrame) -> dict:
	parent_map = {}
	if "stop_id" not in stops_df.columns or "parent_station" not in stops_df.columns:
		return parent_map

	for _, row in stops_df[["stop_id", "parent_station"]].iterrows():
		stop_id = row["stop_id"]
		parent_station = row["parent_station"]
		if pd.isna(stop_id) or pd.isna(parent_station):
			continue
		parent_map[int(stop_id)] = int(parent_station)

	return parent_map

def build_line_ids_map(trips_df: pd.DataFrame, routes_df: pd.DataFrame) -> dict:
	trip_to_route = trips_df.set_index("trip_id")["route_id"].to_dict()
	route_to_line = routes_df.set_index("route_id")["route_short_name"].to_dict()
	return {trip_id: route_to_line.get(route_id) for trip_id, route_id in trip_to_route.items()}

# ===== GRAPH BUILDING FUNCTIONS =====

def filter_calendar_by_date(calendar_df: pd.DataFrame, date: pd.Timestamp) -> pd.DataFrame:
	date = pd.Timestamp(date)
	day_column = date.day_name().lower()

	if day_column not in calendar_df.columns:
		raise KeyError(f"Missing weekday column: {day_column}")

	active_on_day = calendar_df[day_column] == 1
	within_date_range = (calendar_df["start_date"] <= date) & (calendar_df["end_date"] >= date)

	return calendar_df.loc[active_on_day & within_date_range].copy()

def get_day_services(calendar_df: pd.DataFrame) -> pd.DataFrame:
	return calendar_df["service_id"].tolist()

def filter_calendar_exceptions_by_date(calendar_exceptions_df: pd.DataFrame, date: pd.Timestamp) -> pd.DataFrame:
	date = pd.Timestamp(date)
	return calendar_exceptions_df[calendar_exceptions_df["date"] == date].copy()

def get_active_services_for_date(day_services, exception_services):
    services = set(day_services)
    
    for _, row in exception_services.iterrows():
        if row["exception_type"] == 1:
            services.add(row["service_id"])
        elif row["exception_type"] == 2:
            services.discard(row["service_id"])
            
    return list(services)

	# return [service for service in day_services if service not in exception_services]

def filter_trips_by_service_id(trips_df: pd.DataFrame, service_ids: list) -> pd.DataFrame:
	return trips_df[trips_df["service_id"].isin(service_ids)].copy()

def filter_stop_times_by_trip_id(stop_times_df: pd.DataFrame, filtered_trips_df: pd.DataFrame) -> pd.DataFrame:
	trip_ids = filtered_trips_df["trip_id"].tolist()
	return stop_times_df[stop_times_df["trip_id"].isin(trip_ids)].copy()

def get_stop_times_dict_by_trip_id(stop_times_df: pd.DataFrame, filtered_trips_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
	trip_ids = filtered_trips_df["trip_id"].tolist()
	filtered_stop_times = stop_times_df[stop_times_df["trip_id"].isin(trip_ids)].copy()
	filtered_stop_times = filtered_stop_times.sort_values(["trip_id", "stop_sequence"])

	return {
		trip_id: group.reset_index(drop=True)
		for trip_id, group in filtered_stop_times.groupby("trip_id", sort=False)
	}
 
def get_graph(trips_dict, parent_station_map: dict[int, int] | None = None):
	parent_station_map = parent_station_map or {}
	graph = {}
	for _, stop_times in trips_dict.items():
		stops = stop_times.to_dict(orient="records")
		for i in range(len(stops) - 1):
			from_stop = stops[i]
			to_stop = stops[i + 1]
			from_stop_id = parent_station_map.get(from_stop["stop_id"], from_stop["stop_id"])
			to_stop_id = parent_station_map.get(to_stop["stop_id"], to_stop["stop_id"])
			if from_stop_id not in graph:
				graph[from_stop_id] = []
			if to_stop_id not in graph:
				graph[to_stop_id] = []
			edge = {
				"to": to_stop_id,
				"dep_time": time_to_seconds(from_stop["departure_time"]),
				"arr_time": time_to_seconds(to_stop["arrival_time"]),
    			"time": time_to_seconds(to_stop["arrival_time"]) - time_to_seconds(from_stop["departure_time"]),
				"trip_id": from_stop["trip_id"],
			}
			graph[from_stop_id].append(edge)
	return graph

def add_stop_names_to_graph(graph: dict, stops_df: pd.DataFrame) -> dict:
	stop_name_by_id = (
		stops_df[["stop_id", "stop_name"]]
		.dropna(subset=["stop_id"])
		.drop_duplicates(subset=["stop_id"])
		.assign(stop_id=lambda df: df["stop_id"].astype(str))
		.set_index("stop_id")["stop_name"]
		.to_dict()
	)

	for from_stop_id, edges in graph.items():
		from_stop_name = stop_name_by_id.get(str(from_stop_id))
		for edge in edges:
			edge["from_stop_name"] = from_stop_name
			edge["to_stop_name"] = stop_name_by_id.get(str(edge["to"]))

	return graph

def add_line_names_to_graph(graph: dict, lines_map: dict) -> dict:
    for _, edges in graph.items():
        for edge in edges:
            edge["line_name"] = lines_map[edge["trip_id"]]

def sort_graph_by_stop_dep(graph: dict) -> dict:
	sorted_graph = {}
	for from_stop_id, edges in graph.items():
		sorted_edges = sorted(edges, key=lambda x: (x["to"], x["dep_time"]))
		sorted_graph[from_stop_id] = sorted_edges
	return sorted_graph

def convert_times(graph: dict) -> dict:
	for edges in graph.values():
		for edge in edges:
			if isinstance(edge.get("dep_time"), str):
				edge["dep_time"] = time_to_seconds(edge["dep_time"])
			if isinstance(edge.get("arr_time"), str):
				edge["arr_time"] = time_to_seconds(edge["arr_time"])
	return graph    

def add_locations_to_graph(graph: dict, stops_df: pd.DataFrame) -> dict:
	stop_location_by_id = (
		stops_df[["stop_id", "stop_lat", "stop_lon"]]
		.dropna(subset=["stop_id"])
		.drop_duplicates(subset=["stop_id"])
		.assign(stop_id=lambda df: df["stop_id"].astype(str))
		.set_index("stop_id")[["stop_lat", "stop_lon"]]
		.to_dict(orient="index")
	)

	for from_stop_id, edges in graph.items():
		from_location = stop_location_by_id.get(str(from_stop_id))
		for edge in edges:
			to_location = stop_location_by_id.get(str(edge["to"]))
			if from_location:
				edge["from_lat"] = from_location["stop_lat"]
				edge["from_lon"] = from_location["stop_lon"]
			if to_location:
				edge["to_lat"] = to_location["stop_lat"]
				edge["to_lon"] = to_location["stop_lon"]

	return graph
 
# ===== MODULE FUNCTION ===== 

def get_graph_for_date(date, with_locations=False):
	if isinstance(date, pd.Timestamp):
		date_str = date.strftime("%Y%m%d")
	elif isinstance(date, str):
		date_str = pd.Timestamp(date).strftime("%Y%m%d")
	else:
		date_str = pd.Timestamp(date).strftime("%Y%m%d")

	output_dir = PROJECT_ROOT / "data" / "json"
	location_suffix = "_with_locations" if with_locations else ""
	primary_path = output_dir / f"graph_{date_str}{location_suffix}.json"
	fallback_path = output_dir / f"graph_{date_str}.json"

	if primary_path.exists():
		file_path = primary_path
	elif fallback_path.exists():
		file_path = fallback_path
	else:
		raise FileNotFoundError(
			f"Graph JSON not found for {date_str}: checked {primary_path} and {fallback_path}"
		)

	with open(file_path, "r") as f:
		graph = json.load(f)
  
	converted_graph = {}
	for stop_id, edges in graph.items():
		try:
			converted_graph[int(stop_id)] = edges
		except (ValueError, TypeError):
			converted_graph[stop_id] = edges

	return converted_graph

def save_graph_json(graph, dat):
	if isinstance(dat, pd.Timestamp):
		date_str = dat.strftime("%Y%m%d")
	elif isinstance(dat, date):
		date_str = dat.strftime("%Y%m%d")
	elif isinstance(dat, str):
		date_str = pd.Timestamp(dat).strftime("%Y%m%d")
	else:
		raise TypeError("dat must be a pandas.Timestamp, datetime.date, or date string")

	output_dir = PROJECT_ROOT / "data" / "json"
	output_dir.mkdir(parents=True, exist_ok=True)
	filename = output_dir / f"graph_{date_str}.json"
	with open(filename, "w") as f:
		json.dump(graph, f, indent=2)
	print(f"Saved in {filename}")
  
def save_graphs(with_locations=True):
	calendar_data = load_calendar_data()
	calendar_exceptions_data = load_calendar_exceptions_data()
	trips_data = load_trips_data()
	stop_times_data = load_stop_times_data()
	stops_df = load_stop_data()
	routes_df = load_routes_data()
	parent_station_map = build_parent_station_map(stops_df)

	start_date = pd.Timestamp("2026-03-03")
	end_date = pd.Timestamp("2026-12-12")
	all_dates = pd.date_range(start=start_date, end=end_date, freq="D")

	for current_date in all_dates:
		filtered_calendar = filter_calendar_by_date(calendar_data, current_date)
		day_services = get_day_services(filtered_calendar)

		filtered_calendar_exceptions = filter_calendar_exceptions_by_date(
			calendar_exceptions_data,
			current_date,
		)
		active_services = get_active_services_for_date(day_services, filtered_calendar_exceptions)

		if not active_services:
			continue

		filtered_trips = filter_trips_by_service_id(trips_data, active_services)
		if filtered_trips.empty:
			continue

		filtered_stop_times = filter_stop_times_by_trip_id(stop_times_data, filtered_trips)
		trips_dict = get_stop_times_dict_by_trip_id(filtered_stop_times, filtered_trips)

		graph = get_graph(trips_dict, parent_station_map)
		graph_with_names = add_stop_names_to_graph(graph, stops_df)

		lines_map = build_line_ids_map(filtered_trips, routes_df)
		add_line_names_to_graph(graph_with_names, lines_map)

		sorted_graph = sort_graph_by_stop_dep(graph_with_names)
		final_graph = convert_times(sorted_graph)

		if with_locations:
			final_graph = add_locations_to_graph(final_graph, stops_df)

		save_graph_json(final_graph, current_date)
		print(f"Saved graph for {current_date.strftime('%Y-%m-%d')}")
  
class Graph:
	def __init__(self, date, with_locations=False):
		self.date = date
		self.with_locations = with_locations
		self.graph = get_graph_for_date(date, with_locations=with_locations)
		self.next_days_loaded = 0
  
	def has_next_dat(self):
		return pd.Timestamp(self.date) < pd.Timestamp("2026-12-12")
  
	def load_next_day(self):
		if not self.has_next_dat():
			return False

		next_date = pd.Timestamp(self.date) + pd.Timedelta(days=1)
		self.date = next_date
		to_add = get_graph_for_date(next_date, with_locations=self.with_locations)
  
		self.next_days_loaded += 1
  
		for edges in to_add.values():
			for edge in edges:
				edge["dep_time"] += 86400 * self.next_days_loaded
				edge["arr_time"] += 86400 * self.next_days_loaded

		for stop_id, edges in to_add.items():
			if stop_id not in self.graph:
				self.graph[stop_id] = []
			self.graph[stop_id].extend(edges)
			self.graph[stop_id].sort(key=lambda edge: (edge["to"], edge["dep_time"]))

		return True

# CLI function to save graphs: python -m src.graph
if __name__ == "__main__":
    save_graphs()