#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 12:38:22 2025

@author: xiaoyubai
"""

import pandas as pd
import xarray as xr
import numpy as np
import xskillscore as xs

ds = xr.open_dataset('/scratch/xiaoyu/data/analysis_v2/TC_ridge/corr/nc/z_star_2075_110260_7722.nc')
weights2d_xr = xr.open_dataset('/scratch/xiaoyu/data/analysis_v2/TC_ridge/corr/nc/weights_2075_110260.nc')
dates = pd.read_csv('/scratch/xiaoyu/data/analysis_v2/dates/TC/reference/ridge_v2_TC_with_enso.csv')
dates['date'] = pd.to_datetime(dates['date'])


cats = ['S1', 'S2', 'S3', 'S4', 'L1', 'L2', 'L3', 'L4']

records = []

for cat in cats:
    kitty = dates.loc[dates['cluster'] == cat].reset_index(drop=True)
    T0_maps = ds.sel(TIME=kitty['date'].values)    
    T0 = T0_maps.mean(dim='TIME')
    
    # Determine season and cluster number
    if cat.startswith('S'):
        season = 'summer'
        i = int(cat[1:]) - 1 
        response = xr.open_dataset(f'/scratch/xiaoyu/data/analysis_v2/kmeans_v2/mid_summer/nc/{season}_cluster{i}_comp.nc')
    else:
        season = 'late'
        i = int(cat[1:]) - 1  # get the numeric part, e.g., 'S3' → 3
        response = xr.open_dataset(f'/scratch/xiaoyu/data/analysis_v2/kmeans_v2/mid_anom/nc/{season}_cluster{i}_mid.nc')

    
    corr_res = xs.pearson_r(T0.Z_STAR, response.Z_STAR, dim=['LATITUDE', 'LONGITUDE'], weights=weights2d_xr, skipna=True)

     # Store results
    records.append({
    'cluster': cat,
    'corr_res': corr_res.to_array().item()
    })

# Convert to DataFrame
df_corr_summary = pd.DataFrame(records)

# Save if desired
df_corr_summary.to_csv('/scratch/xiaoyu/data/analysis_v2/TC_ridge/corr/corr_response_cluster.csv', index=False)
    