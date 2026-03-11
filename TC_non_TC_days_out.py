#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 16:48:31 2025

@author: xiaoyubai
"""

import pandas as pd
path = '/Users/xiaoyubai/Documents/TC_ridges_surface/data/adding_2324'

# %%
TC = pd.read_csv('/Users/xiaoyubai/Documents/TC_ridges_surface/data/adding_2324/TC_30N_all_month.csv')
TC['date'] = pd.to_datetime(TC['date'])

# Get unique dates
unique_dates = TC['date'].dropna().unique()

# Generate 7-day windows and flatten them
all_dates = []
for d in unique_dates:
    all_dates.extend(pd.date_range(start=d, periods=7, freq='D'))

# Convert to DataFrame of unique sorted dates
unique_date_df = pd.DataFrame({'date': sorted(set(all_dates))})
tran_date = unique_date_df['date'].unique()

TC_dates = pd.read_csv('/Users/xiaoyubai/Documents/TC_ridges_surface/data/adding_2324/TC_51_24_all_month.csv', low_memory=False)
TC_dates['date'] = pd.to_datetime(TC_dates['date'])
TC_dates = TC_dates['date'].unique()


# Step 2: Combine, deduplicate, sort
combined_dates = pd.Series(list(tran_date) + list(TC_dates)).drop_duplicates()
combined_dates = combined_dates.sort_values().reset_index(drop=True)

# Step 3: Filter for year >= 1977
combined_dates = combined_dates[combined_dates.dt.year >= 1977]

# Step 4: Convert to DataFrame if needed
combined_df = pd.DataFrame({'date': combined_dates})

# %%

# Create a date range for all days from 1977 to 2024
all_dates = pd.date_range(start='1977-06-01', end='2024-12-31', freq='D')

# Filter out months 
summer_dates = all_dates[~all_dates.month.isin([1, 2, 3, 4, 5, 10, 11, 12])]

# Create the DataFrame
summer = pd.DataFrame({'date': summer_dates})

# Ensure both are datetime
summer['date'] = pd.to_datetime(summer['date'])
combined_df['date'] = pd.to_datetime(combined_df['date'])

# Summer dates that are also in TC combined_df
summer_TC_days = summer[summer['date'].isin(combined_df['date'])].reset_index(drop=True)

# Summer dates that are not in TC combined_df
summer_non_TC = summer[~summer['date'].isin(combined_df['date'])].reset_index(drop=True)

# Print results
print(f"summer days: {len(summer)}")
print(f"Summer TC days: {len(summer_TC_days)}")
print(f"Summer non-TC days: {len(summer_non_TC)}")

summer.to_csv(f'{path}/dates_summer_all.csv')
summer_TC_days.to_csv(f'{path}/dates_summer_TC.csv')
summer_non_TC.to_csv(f'{path}/dates_summer_non_TC.csv')



# %%
# Filter out months 
winter_dates = all_dates[~all_dates.month.isin([1, 2, 3, 4, 5, 6, 7, 8, 9])]

# Create the DataFrame
winter = pd.DataFrame({'date': winter_dates})

# Ensure both are datetime
winter['date'] = pd.to_datetime(winter['date'])
combined_df['date'] = pd.to_datetime(combined_df['date'])

# Summer dates that are also in TC combined_df
winter_TC_days = winter[winter['date'].isin(combined_df['date'])].reset_index(drop=True)

# winter dates that are not in TC combined_df
winter_non_TC = winter[~winter['date'].isin(combined_df['date'])].reset_index(drop=True)

# Print results
print(f"winter days: {len(winter)}")
print(f"winter TC days: {len(winter_TC_days)}")
print(f"winter non-TC days: {len(winter_non_TC)}")

winter.to_csv(f'{path}/dates_winter_all.csv')
winter_TC_days.to_csv(f'{path}/dates_winter_TC.csv')
winter_non_TC.to_csv(f'{path}/dates_winter_non_TC.csv')

# %%

