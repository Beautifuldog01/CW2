import itertools
import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import csv

def read_and_process_csv(file_name):
    matrix = []

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            new_row = [np.nan if cell == '' else float(cell) for cell in row]
            matrix.append(new_row)

    matrix = np.array(matrix, dtype=float)
    n = matrix.shape[0]
    matrix[np.isnan(matrix)] = 0

    for i in range(n):
        for j in range(i+1, n):
            matrix[i, j] = matrix[j, i]

    # matrix_nonzero = matrix[matrix > 0]
    # matrix_min = np.min(matrix_nonzero)
    # matrix_max = np.max(matrix_nonzero)
    # matrix[matrix > 0] = (matrix[matrix > 0] - matrix_min) / (matrix_max - matrix_min)

    matrix[matrix == 0] = 1000

    return matrix


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

    # 修改此处，使用tqdm包装itertools.permutations
    for path in tqdm(list(itertools.permutations(cities)), desc="Calculating progress"):
        path = (start,) + path + (start,)
        cost, transport = combined_cost_and_transport(path, flight_data, train_data, max_flights, max_trains)
        if cost < min_cost:
            min_cost = cost
            min_path = path
            min_transport = transport

    return min_path, min_cost, min_transport

# London	Vienna	Paris	Rome	Barcelona	Berline	Amsterdam	København	Zurich	Budapest
cities = ['London', 'Vienna', 'Paris', 'Rome', 'Barcelona', 'Berlin', 'Amsterdam', 'Copenhagen', 'Zurich', 'Budapest']

def read_month_data(directory):
    data = {}
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            data_type = file_name[:-4]
            file_path = os.path.join(directory, file_name)
            data[data_type] = read_and_process_csv(file_path)
    return data

july_data_path = "/Users/badudu/Documents/MTH203/CW2/code/data/July"
august_data_path = "/Users/badudu/Documents/MTH203/CW2/code/data/August"

july_data = read_month_data(july_data_path)
august_data = read_month_data(august_data_path)

flight_cost_df = pd.DataFrame(july_data['flight_costs'], columns=cities, index=cities)
train_cost_df = pd.DataFrame(july_data['train_costs'], columns=cities, index=cities)
flight_time_df = pd.DataFrame(july_data['flight_time'], columns=cities, index=cities)
train_time_df = pd.DataFrame(july_data['train_time'], columns=cities, index=cities)

def read_original_data(file_name):
    data = []

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            new_row = [np.nan if cell == '' else float(cell) for cell in row]
            data.append(new_row)

    data_df = pd.DataFrame(data, columns=cities, index=cities)

    # 复制对角线元素
    n = data_df.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            data_df.iloc[i, j] = data_df.iloc[j, i]

    return data_df


flight_cost_original_df = read_original_data(os.path.join(july_data_path, 'flight_costs.csv'))
train_cost_original_df = read_original_data(os.path.join(july_data_path, 'train_costs.csv'))
flight_time_original_df = read_original_data(os.path.join(july_data_path, 'flight_time.csv'))
train_time_original_df = read_original_data(os.path.join(july_data_path, 'train_time.csv'))

def get_cost_and_time(optimal_path, optimal_transport, flight_cost_matrix, train_cost_matrix, flight_time_matrix, train_time_matrix):
    cost_list = []
    time_list = []

    for i in range(len(optimal_path) - 1):
        city1 = optimal_path[i]
        city2 = optimal_path[i + 1]
        transport = optimal_transport[i]

        if transport == "Airplane":
            cost = flight_cost_matrix.loc[city1, city2]
            time = flight_time_matrix.loc[city1, city2]
        else:  # transport == "Train"
            cost = train_cost_matrix.loc[city1, city2]
            time = train_time_matrix.loc[city1, city2]

        cost_list.append(cost)
        time_list.append(time)

    return cost_list, time_list

from functools import lru_cache
def held_karp_modified(flight_df, train_df, start_city, max_flights, max_trains):
    cities = flight_df.columns.tolist()
    cities.remove(start_city)
    cities_set = frozenset(cities)

    @lru_cache(maxsize=None)
    def dp(city, visited_cities, remaining_flights, remaining_trains):
        if visited_cities == cities_set:
            if remaining_flights > 0:
                return flight_df.loc[city, start_city], [start_city]
            else:
                return train_df.loc[city, start_city], [start_city]

        min_cost = float('inf')
        min_path = []

        for next_city in cities:
            if next_city not in visited_cities:
                new_visited_cities = visited_cities | {next_city}
                flight_cost = flight_df.loc[city, next_city]
                train_cost = train_df.loc[city, next_city]

                if remaining_flights > 0:
                    cost_flight, path_flight = dp(next_city, new_visited_cities, remaining_flights - 1, remaining_trains)
                    cost_flight += flight_cost

                    if cost_flight < min_cost:
                        min_cost = cost_flight
                        min_path = path_flight + [next_city]

                if remaining_trains > 0:
                    cost_train, path_train = dp(next_city, new_visited_cities, remaining_flights, remaining_trains - 1)
                    cost_train += train_cost

                    if cost_train < min_cost:
                        min_cost = cost_train
                        min_path = path_train + [next_city]

        return min_cost, min_path

    min_cost, optimal_path = dp(start_city, frozenset(), max_flights, max_trains)
    optimal_path = [start_city] + optimal_path[::-1]

    # Determine transport mode
    transport = []
    for i in range(len(optimal_path) - 1):
        if max_flights > 0 and (flight_df.loc[optimal_path[i], optimal_path[i+1]] <= train_df.loc[optimal_path[i], optimal_path[i+1]] or max_trains == 0):
            transport.append("Airplane")
            max_flights -= 1
        else:
            transport.append("Train")
            max_trains -= 1

    return optimal_path, min_cost, transport

alpaha = 0
beta = 1 - alpaha
flight_df = flight_cost_df * alpaha + flight_time_df * beta
train_df = train_cost_df * alpaha + train_time_df * beta
start_city = cities[0]
max_flights = 10
max_trains = 10

optimal_path, min_cost, optimal_transport = tsp_bruteforce_combined(flight_df, train_df, start_city, max_flights, max_trains)

cost_list, time_list = get_cost_and_time(optimal_path, optimal_transport, flight_cost_original_df, train_cost_original_df, flight_time_original_df, train_time_original_df)

print("Optimal path:", optimal_path)
print("Transportation mode:", optimal_transport)
print("Costs for each segment:", cost_list)
print("Times for each segment:", time_list)
print("cost all", sum(cost_list))
print("time all", np.round(sum(time_list)))