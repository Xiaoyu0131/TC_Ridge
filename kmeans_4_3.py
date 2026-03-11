#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 19:03:04 2025

@author: xiaoyubai
"""

import pandas as pd
import xarray as xr
from sklearn.cluster import KMeans
import sys
import numpy as np
# %%

output_path = '/scratch/xiaoyu/data/TC_ridge/adding2324'
seasons = ['summer', 'winter']
numbers = [4, 3]
sea = sys.argv[1]
num_cluster = numbers[int(sea)]
season = seasons[int(sea)]
# %%
TCC = pd.read_csv(f'{output_path}/TC_ridge_quadrant.csv')
TC = TCC.loc[TCC['season'] == season]

# Convert 'date' to a datetime type
TC['tran_date'] = pd.to_datetime(TC['tran_date'])

# Drop duplicates based on the 'date' column, keeping the first occurrence
TC_unique = TC.drop_duplicates(subset='tran_date', keep='first')

# %%
base_path = '/scratch/xiaoyu/data/ERA5/daily/Z_star500/'
years = TC_unique['tran_date'].dt.year.unique()
# years = range(1977, 2023)
# Prepare to load files
datasets = []  # This will store each loaded Dataset

for year in years:
    # File path for the current year's data
    file_path = f"{base_path}z_star_{year}.nc"

    # Load the dataset for the current year
    ds = xr.open_dataset(file_path)

    # Select data for the current year's dates using .sel method
    # Note: Ensure 'TIME' or similar is the correct coordinate name in your dataset for date/time
    filtered_ds = ds.sel(LATITUDE=slice(20, 75), LONGITUDE=slice(110, 260))

    # Store the filtered dataset
    datasets.append(filtered_ds)
# Concatenate all datasets along the TIME dimension
ds = xr.concat(datasets, dim='TIME')

# %%
# Generate a DataFrame with each date and its corresponding 3-7 day range
all_ranges = []
for single_date in TC_unique['tran_date']:
    # Create ranges from 3 to 7 days after each date
    expanded_dates = pd.date_range(start=single_date + pd.Timedelta(days=3), periods=5)
    for d in expanded_dates:
        all_ranges.append({'base_date': single_date, 'range_date': d})


# Convert into a DataFrame
date_df = pd.DataFrame(all_ranges)

anomalies = []
base_dates = []

for _, row in date_df.groupby('base_date'):
    base_date = row['base_date'].iloc[0]
    range_dates = row['range_date']
    base_date_list = base_date.strftime('%Y-%m-%d')
    range_dates_list = range_dates.dt.strftime('%Y-%m-%d').tolist()
    # Select the base date and range dates from the xarray dataset
    base = pd.to_datetime(base_date_list)
    ranges = pd.to_datetime(range_dates_list)
    base_value = ds.sel(TIME=base)
    range_values = ds.sel(TIME=ranges)

    # Calculate mean over the selected range dates
    range_mean = range_values.mean(dim='TIME')
    
    # Calculate anomaly (range mean minus base value)
    anomaly = range_mean - base_value
    
    # Append the anomaly and the base date to their respective lists
    anomalies.append(anomaly)
    base_dates.append(base)

# Convert the list of anomalies to xarray Dataset
anomalies_ds = xr.concat(anomalies, dim=pd.Index(base_dates, name='TIME'))

da = anomalies_ds['Z_STAR'] 

# %%
num_days = da.shape[0]
data_reshaped = da.values.reshape(num_days, -1)  # Reshape from (360, lat, lon) to (360, lat*lon)

# K-means clustering
kmeans = KMeans(n_clusters=num_cluster, n_init=100, random_state=0)
kmeans.fit(data_reshaped)
labels = kmeans.labels_

# Dictionary to hold indices for each cluster
clusters = {i: [] for i in range(num_cluster)}
for i, label in enumerate(labels):
    clusters[label].append(i)

# Write each cluster's data to a separate NetCDF file
for cluster, indices in clusters.items():
    # Select the days that belong to the current cluster
    cluster_ds = anomalies_ds.isel(TIME=indices)   
    mean = cluster_ds.mean(dim='TIME')
    # Write to a NetCDF file
    mean.to_netcdf(f'{output_path}/nc/{season}_cluster{cluster}_comp.nc')

# getting dates belonging to each cluster:
dates = pd.to_datetime(da.TIME.values)  
date_clusters = {i: [] for i in range(num_cluster)}
for i, label in enumerate(labels):
    date_clusters[label].append(dates[i])
# Convert lists in date_clusters to DataFrames
# date_dfs = {cluster: pd.DataFrame(dates, columns=['Dates']) for cluster, dates in date_clusters.items()}
date_dfs = {cluster: pd.DataFrame({"Dates": cluster_dates}) for cluster, cluster_dates in date_clusters.items()}
for cluster, df in date_dfs.items():
    df.to_csv(f'{output_path}/csv/{season}_cluster{cluster}_dates.csv', index=False)