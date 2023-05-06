import itertools
import pandas as pd
import numpy as np
from data_process import read_and_process_csv
import os

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

# London	Vienna	Paris	Rome	Barcelona	Berline	Amsterdam	København	Zurich	Budapest
cities = ['London', 'Vienna', 'Paris', 'Rome', 'Barcelona', 'Berlin', 'Amsterdam', 'Copenhagen', 'Zurich', 'Budapest']

def read_month_data(directory):
    data = {}
    for file_name in os.listdir(directory):
        # 仅处理 CSV 文件
        if file_name.endswith(".csv"):
            # 从文件名中提取数据类型
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

alpaha = 0.3
beta = 0.7

flight_df = flight_cost_df * alpaha + flight_time_df * beta
train_df = train_cost_df * alpaha + train_time_df * beta

start_city = cities[0]
max_flights = 10
max_trains = 10
optimal_path, min_cost, optimal_transport = tsp_bruteforce_combined(flight_df, train_df, start_city, max_flights, max_trains)

print(f"shortest path: {optimal_path}")
print(f"way or transport: {optimal_transport}")
print(f"lowest fee: {np.around(min_cost*1000)}")
