import itertools
import pandas as pd
import numpy as np


def combined_cost_and_transport(path, flight_df, train_df, max_flights, max_trains):
    total_cost = 0
    transport = []
    flight_count = 0
    train_count = 0
    for i in range(len(path) - 1):
        flight_cost = flight_df.loc[path[i], path[i + 1]]
        train_cost = train_df.loc[path[i], path[i + 1]]
        if flight_count < max_flights and (train_count >= max_trains or flight_cost < train_cost):
            total_cost += flight_cost
            transport.append("Airplane")
            flight_count += 1
        elif train_count < max_trains:
            total_cost += train_cost
            transport.append("Train")
            train_count += 1
        else:
            return float('inf'), transport
    return total_cost, transport


def tsp_bruteforce_combined(flight_data, train_data, start, max_flights, max_trains):
    cities = flight_data.columns.tolist()
    cities.remove(start)
    min_cost = float('inf')
    min_path = None
    min_transport = None

    for path in itertools.permutations(cities):
        path = (start,) + path + (start,)
        cost, transport = combined_cost_and_transport(path, flight_data, train_data, max_flights, max_trains)
        if cost < min_cost:
            min_cost = cost
            min_path = path
            min_transport = transport

    return min_path, min_cost, min_transport


num = 10
all_cities = ['London', 'Paris', 'Berlin', 'Madrid', 'Rome', 'Vienna', 'Bucharest', 'Warsaw', 'Budapest', 'Hamburg']
cities = np.random.choice(all_cities, num, replace=False)

np.random.seed(42)
flight_costs = np.random.randint(500, 600, size=(num, num))
np.fill_diagonal(flight_costs, 0)
train_costs = np.random.randint(500, 700, size=(num, num))
np.fill_diagonal(train_costs, 0)

flight_df = pd.DataFrame(flight_costs, columns=cities, index=cities)
train_df = pd.DataFrame(train_costs, columns=cities, index=cities)

start_city = cities[0]
max_flights = 10
max_trains = 10
optimal_path, min_cost, optimal_transport = tsp_bruteforce_combined(flight_df, train_df, start_city, max_flights,
                                                                    max_trains)

print(f"shortest path: {optimal_path}")
print(f"way or transport: {optimal_transport}")
print(f"lowest fee: {min_cost}")
