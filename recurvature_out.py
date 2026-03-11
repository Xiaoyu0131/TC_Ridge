#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 13:44:50 2025

@author: xiaoyubai
"""

import pandas as pd
import numpy as np

path = '/Users/xiaoyubai/Documents/TC_ridges_surface/data/adding_2324/'

df = pd.read_csv(f'{path}TC_51_24_all_month.csv', low_memory = False)
# dff = df.loc[df['data_category'] >= 3]
# dff.to_csv('/Users/xiaoyubai/Documents/TC_ridges_surface/data/tidy_csv/TC_51M-24O_TS&up.csv', index = None)
# da = pd.read_csv('/Users/xiaoyubai/Documents/Ridges/analysis_v4/csv/tidy_1940_2022_intensity_no_nan.csv')

# # Combine year, month, and day into a date column
# da['date'] = pd.to_datetime(da[['year', 'month', 'day']])

# # If you want the date as a string in 'year-month-day' format
# da['date'] = da['date'].dt.strftime('%Y-%m-%d')
# da['date'] = pd.to_datetime(da['date'])

# df['date'] = df['data_time'].apply(format_data_time)
df['date'] = pd.to_datetime(df['date'])

df['data_latitude'] = df['data_latitude']/10
df['data_longitude'] = df['data_longitude']/10

# Shift the latitude and longitude to compare with the previous and next rows
df['prev_latitude'] = df.groupby('header_ID')['data_latitude'].shift(1)
df['next_latitude'] = df.groupby('header_ID')['data_latitude'].shift(-1)
df['prev_longitude'] = df.groupby('header_ID')['data_longitude'].shift(1)
df['next_longitude'] = df.groupby('header_ID')['data_longitude'].shift(-1)

# df.to_csv(f'{path}test_precision.csv')

# r = df[
#     np.isclose(df['data_latitude'], 17.6, atol=1e-6) &
#     np.isclose(df['prev_latitude'], 17.4, atol=1e-6) &
#     np.isclose(df['next_latitude'], 18.1, atol=1e-6)
# ]
# print(r)
# %%
# row = df.loc[48027]

# print("Row 22763 values after /10:")
# print("data_latitude :", row['data_latitude'])
# print("prev_latitude :", row['prev_latitude'])
# print("next_latitude :", row['next_latitude'])
# print("data_longitude:", row['data_longitude'])
# print("prev_longitude:", row['prev_longitude'])
# print("next_longitude:", row['next_longitude'])

# print("\nSub-condition checks:")
# print("lat check 1 (data > prev):",
#       row['data_latitude'] > row['prev_latitude'] or 
#       np.isclose(row['data_latitude'], row['prev_latitude'], atol=1e-6))

# print("lon check (data <= prev):",
#       row['data_longitude'] < row['prev_longitude'] or 
#       np.isclose(row['data_longitude'], row['prev_longitude'], atol=1e-6))

# print("lat check 2 (next > data):",
#       row['next_latitude'] > row['data_latitude'] or 
#       np.isclose(row['next_latitude'], row['data_latitude'], atol=1e-6))

# print("lon check 2 (next > data):",
#       row['next_longitude'] > row['data_longitude'] or 
#       np.isclose(row['next_longitude'], row['data_longitude'], atol=1e-6))

# print("\nSub-condition checks:")
# print("lat check 1 (data > prev):",
#       row['data_latitude'] > row['prev_latitude'])

# print("lon check (data <= prev):",
#       row['data_longitude'] < row['prev_longitude'])

# print("lat check 2 (next > data):",
#       row['next_latitude'] > row['data_latitude'])

# print("lon check 2 (next > data):",
#       row['next_longitude'] > row['data_longitude'])
# %%
# Define conditions for recurvature
conditions = (
    (df['data_latitude'] > df['prev_latitude']) &
    (df['data_longitude'] <= df['prev_longitude']) &
    (df['next_latitude'] > df['data_latitude']) &
    (df['next_longitude'] > df['data_longitude'])
)

# Apply category conditions
category_conditions = (
    (df['data_category'] >= 3) & (df['data_category'] <= 5) | (df['data_category'] == 9)
)

# Combine all conditions
final_conditions = conditions & category_conditions
df['is_recurvature'] = final_conditions  # This will add a True/False column to df

# Filter header_IDs with specific category conditions
header_ids_with_5 = df[df['data_category'] == 5]['header_ID'].unique()
header_ids_with_6 = df[df['data_category'] == 6]['header_ID'].unique()
valid_header_ids = np.intersect1d(header_ids_with_5, header_ids_with_6)

# Further filter for latitude >= 30
header_ids_latitude_30 = df[df['data_latitude'] >= 30]['header_ID'].unique()
final_valid_header_ids = np.intersect1d(valid_header_ids, header_ids_latitude_30)

ogg = df[df['header_ID'].isin(final_valid_header_ids)]
og =ogg.groupby('header_ID').first().reset_index()
og.to_csv(f'{path}TC_og.csv')

# %%

# Select only rows that are from valid header IDs and meet the recurvature condition
valid_recurvature_points = df[df['header_ID'].isin(final_valid_header_ids) & df['is_recurvature']]

# df.to_csv(f'{path}test.csv', index=None)
# Get the first occurrence of recurvature for each header_ID
first_recurvature_per_id = valid_recurvature_points.groupby('header_ID').first().reset_index()

# Saving the results
first_recurvature_per_id.to_csv(f'{path}TC_first_recurve.csv', index=None)



# Group by header_ID and find the entry with the smallest longitude (westernmost recurvature)
westernmost_recurvature_per_id = valid_recurvature_points.loc[valid_recurvature_points.groupby('header_ID')['data_longitude'].idxmin()].reset_index(drop=True)

# Saving the results
westernmost_recurvature_per_id.to_csv(f'{path}TC_westmost_recurve.csv', index=None)


# Filter recurvature_points to keep only those entries that have a header_ID in final_valid_header_ids
# final_recurvature_points = recurvature_points[recurvature_points['header_ID'].isin(final_valid_header_ids)]
# final_recurvature = final_recurvature_points.groupby('header_ID').first().reset_index()

# # Find the first occurrence where data_latitude is >= 30 for these header_IDs
first_valid_latitude_30 = df[df['header_ID'].isin(valid_recurvature_points['header_ID']) & (df['data_latitude'] >= 30)]
first_valid_latitude_30 = first_valid_latitude_30.groupby('header_ID').first().reset_index()

first_valid_latitude_30.to_csv(f'{path}TC_30N_all_month.csv', index = None)
