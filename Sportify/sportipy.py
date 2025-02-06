import os
import numpy as np
import pandas as pd
import zipfile
import json
from xml.etree import ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime
import folium
import folium.plugins as plugins
import mplleaflet
from sklearn.cluster import KMeans
from glob import glob
from folium.plugins import HeatMap


def read_runtastic_data(path):
    all_files = glob("**\*.json", recursive=True)
    # Use glob to find all JSON files in subdirectories for Runtastic sessions
    json_files = glob(os.path.join(path,"*.json"), recursive=True)
    
    # Extract session names
    A_Sessions = []
    for name in json_files:
        session = name.split("\\")[-1].split("_")[-1].split(".")[0]
        A_Sessions.append(session)
    
    
    
    # Use glob to find all JSON files in subdirectories for Runtastic sessions
    json_files = glob(os.path.join(path,"Heart-rate-data/*.json"), recursive=True)
    
    # Extract session names
    H_Sessions = []
    for name in json_files:
        session = name.split("\\")[-1].split("_")[-1].split(".")[0]
        H_Sessions.append(session)
    
    # Use glob to find all JSON files in subdirectories for Runtastic sessions
    json_files = glob(os.path.join(path,"GPS-data/*.json"), recursive=True)
    
    # Extract session names
    G_Sessions = []
    for name in json_files:
        session = name.split("\\")[-1].split("_")[-1].split(".")[0]
        G_Sessions.append(session)\
        
            
    # Convert the session lists to sets
    A_Set = set(A_Sessions)
    H_Set = set(H_Sessions)
    G_Set = set(G_Sessions)
    
    # Find the common sessions
    common_sessions = A_Set.intersection(H_Set, G_Set)
    
    # Convert the result back to a list if needed
    common_sessions_list = list(common_sessions)
    
    
    files_gps = []
    files_hr = []
    for fname in all_files:
        for cs in common_sessions_list:
            if cs in fname and "GPS-data" in fname:
                files_gps.append(fname)
                
            if cs in fname and "Heart-rate-data" in fname:
                files_hr.append(fname)
        
    
    # Initialize an empty DataFrame to store GPS data
    gps_data_combined = pd.DataFrame()
    
    # Iterate over all GPS data files
    for file in files_gps:
        with open(file, 'r') as json_file:
            sessions = json.load(json_file)
            df = pd.DataFrame(sessions)
            df['session'] = file.split("_")[-1].split(".")[0]
            gps_data_combined = pd.concat([gps_data_combined, df], ignore_index=True)
            
    
    
    # Initialize an empty DataFrame to store GPS data
    HR_data_combined = pd.DataFrame()
    
    # Iterate over all HR data files
    for file in files_hr:
        with open(file, 'r') as json_file:
            sessions = json.load(json_file)
            df = pd.DataFrame(sessions)
            df['session'] = file.split("_")[-1].split(".")[0]
            HR_data_combined = pd.concat([HR_data_combined, df], ignore_index=True)
                
                
    combines_data = pd.concat([gps_data_combined,HR_data_combined["heart_rate"]],axis = 1)
    combines_data = combines_data.dropna()
    combines_data['duration'] = combines_data['duration']/1000
    combines_data['timestamp'] = pd.to_datetime(combines_data['timestamp'],unit='ms')
    combines_data.rename(columns={'timestamp': 'time','distance':'cumul_distance_m',"duration":"cumul_time_sec",'heart_rate':"heart_rate_bpm"}, inplace=True)
    return combines_data



def read_ticexercise_data(file_path):
    data_entries = []
    # Process each TCX file and extract relevant information
    # Adjust this part based on the actual TCX file format
    tree = ET.parse(file_path)
    root = tree.getroot()
    for trackpoint in root.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint"):
        time = trackpoint.findtext("{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time")
        longitude = float(trackpoint.findtext("{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position/{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees", 0))
        latitude = float(trackpoint.findtext("{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position/{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees", 0))
        heart_rate_bpm = trackpoint.findtext("{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}HeartRateBpm/{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value")
        cumul_distance_m = trackpoint.findtext("{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters")
        cumul_time_sec = trackpoint.findtext("{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time")


        data_entry = {
            'session': os.path.basename(file_path),
            'time': time,
            'longitude': longitude,
            'latitude': latitude,
            'heart_rate_bpm': heart_rate_bpm,
            'cumul_distance_m': cumul_distance_m,
            'cumul_time_sec': cumul_time_sec,
        }

        data_entries.append(data_entry)

    return data_entries



def load_data(runtastic_folder, tic_exercises_folder):
    ticexercise_data = []
    runtastic_df = read_runtastic_data(runtastic_folder)
    # Read TicExercises data
    for file_name in os.listdir(tic_exercises_folder):
        if file_name.endswith('.tcx'):
            file_path = os.path.join(tic_exercises_folder, file_name)
            ticexercise_data.extend(read_ticexercise_data(file_path))
    # Convert lists to DataFrames 
    ticexercise_df = pd.DataFrame(ticexercise_data)    
    # Merge datasets into a DataFrame
    merged_df = pd.concat([runtastic_df, ticexercise_df], ignore_index=True)

    return runtastic_df


def plot_distance_per_year(df, filename):
    # Convert 'cumul_distance_m' to numeric
    df['cumul_distance_m'] = pd.to_numeric(df['cumul_distance_m'], errors='coerce')
    # Convert time to datetime without specifying unit
    df['time'] = pd.to_datetime(df['time'])
    # Extract year from datetime
    df['year'] = df['time'].dt.year
    # Group by year and sum the distance
    distance_per_year = df.groupby('year')['cumul_distance_m'].sum()
    # Plotting
    plt.figure(figsize=(10, 6))
    distance_per_year.plot(kind='bar', color='skyblue')
    plt.title('Total Distance per Year')
    plt.xlabel('Year')
    plt.ylabel('Total Distance run (meters)')  # Adjusted label for distance unit
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def plot_distance_distribution(df, filename):
    # Convert 'cumul_distance_m' to numeric
    df['cumul_distance_m'] = pd.to_numeric(df['cumul_distance_m'], errors='coerce')
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.hist(df['cumul_distance_m'].dropna(), bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Total Distance Run')
    plt.xlabel('Distance run (meters)')
    plt.ylabel('Number of Workouts')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def plot_mean_speed_distribution(df, filename):
    # Convert 'speed' to numeric
    df['speed'] = pd.to_numeric(df['speed'], errors='coerce')
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.hist(df['speed'].dropna(), bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Average Speed per Run')
    plt.xlabel('Average Speed (km/h)')  # Adjusted label for speed unit
    plt.ylabel('Number of Workouts')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def plot_start_of_run_distribution(df, filename):
    # Convert 'time' to datetime without specifying unit
    df['time'] = pd.to_datetime(df['time'])    
    # Extract the hour of the day from the datetime
    df['start_hour'] = df['time'].dt.hour    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.hist(df['start_hour'].dropna(), bins=24, color='skyblue', edgecolor='black', alpha=0.7)    
    plt.title('Distribution of Start Times of Runs')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Runs')
    plt.xticks(range(24))    
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def trace_itineraries_with_heatmap(df, filename):
    # Filter out rows with missing latitude and longitude values
    df = df.dropna(subset=['latitude', 'longitude'])
    # Create a base map centered around the mean latitude and longitude
    base_map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)
    # Create a HeatMap layer using latitude and longitude columns
    heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(base_map)   
    
    # Save the map to a file
    base_map.save(filename)



def get_geo_clusters(df):
    # Filter out rows with missing latitude and longitude values
    df = df.dropna(subset=['latitude', 'longitude'])
    # Select latitude and longitude columns for clustering
    coordinates = df[['latitude', 'longitude']]
    # Specify the number of clusters (you can adjust this based on your requirements)
    n_clusters = 3
    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    # Add the following line to set the value of n_init explicitly
    kmeans.set_params(n_init=10)
    df['cluster_label'] = kmeans.fit_predict(coordinates)
    return df['cluster_label']
