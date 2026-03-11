#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 15:11:21 2025

@author: xiaoyubai
"""

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colorbar as colorbar
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap, BoundaryNorm
import seaborn as sns
import scipy.stats as stats
from matplotlib.patches import Patch
from cmap import Colormap
from scipy.stats import mannwhitneyu
from statannotations.stats.StatTest import StatTest
from statannotations.Annotator import Annotator
np.float = float
from scipy.stats import ks_2samp
from scipy.stats import mannwhitneyu

# %%
ridge = pd.read_csv('/Users/xiaoyubai/Documents/TC_ridges/data/tidy/ridges_v2+TC.csv')
ridge['date'] = pd.to_datetime(ridge[['year', 'month', 'day']])
season = 'late'

# %%
# Function to process each cluster
def process_cluster(cluster_filename, ridge, cluster_id):
    # Reading and preparing the cluster data
    cluster = pd.read_csv(cluster_filename)
    cluster['Dates'] = pd.to_datetime(cluster['Dates'])

    # Generating all_dates
    all_dates = []
    for start_date in cluster['Dates']:
        date_range = pd.date_range(start=start_date, periods=7)
        all_dates.extend(date_range)

    # Convert to DataFrame
    all_dates_df = pd.DataFrame({'date': all_dates})

    # Creating the mapping from each date to its start date
    date_to_start_date = {date: start_date for start_date in cluster['Dates'] for date in pd.date_range(start=start_date, periods=7)}

    # Applying the mapping to create a new column in all_dates_df
    all_dates_df['start_date'] = all_dates_df['date'].map(date_to_start_date)

    # Merge with ridge data
    merged_data = pd.merge(all_dates_df, ridge, on='date', how='inner')

    # Calculate max intensity values
    inten_values = merged_data.groupby(['start_date'])['9inten_weighted'].max().reset_index()
    inten_values.rename(columns={'9inten_weighted': 'max_inten'}, inplace=True)

    # Calculate max area values
    area_values = merged_data.groupby(['start_date'])['area'].max().reset_index()
    area_values.rename(columns={'area': 'max_area'}, inplace=True)

    # Merging intensity and area values
    final_values = pd.merge(inten_values, area_values, on=['start_date'])

    # Adding the cluster identifier
    final_values['cluster'] = cluster_id

    return final_values

# List of cluster filenames and their identifiers
cluster_files_and_ids = [
    (f'/Users/xiaoyubai/Documents/TC_ridges/data/kmeans/{season}_cluster0_mid_dates.csv', '1'),
    (f'/Users/xiaoyubai/Documents/TC_ridges/data/kmeans/{season}_cluster1_mid_dates.csv', '2'),
    (f'/Users/xiaoyubai/Documents/TC_ridges/data/kmeans/{season}_cluster2_mid_dates.csv', '3'),
    (f'/Users/xiaoyubai/Documents/TC_ridges/data/kmeans/{season}_cluster3_mid_dates.csv', '4')
]

# Assuming 'ridge' DataFrame is already loaded
# ridge = pd.read_csv('path_to_ridge.csv')

# Process each cluster and collect results
results = [process_cluster(filename, ridge, cluster_id) for filename, cluster_id in cluster_files_and_ids]

# Concatenate all results
final_result = pd.concat(results, ignore_index=True)



# %%
# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Create a figure with two subplots (side by side)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))  # Adjust figsize to better fit your screen or presentation

# Create the violin plot for max_area on the first subplot
sns.violinplot(x='cluster', y='max_area', data=final_result, palette='muted', ax=ax1)
sample_sizes = final_result['cluster'].value_counts().sort_index()

# Annotate the plot with sample sizes
# Get the x coordinates for the annotations
x_coords = range(len(sample_sizes))
for x, size in zip(x_coords, sample_sizes):
    ax1.text(x, ax1.get_ylim()[0], f'n={size}', horizontalalignment='center', size='medium', color='black', weight='semibold')

ax1.set_title('TC associated Maximum Ridge Area')
ax1.set_xlabel('Cluster')
ax1.set_ylabel('Max Area (km2)')

# Create the violin plot for max_inten on the second subplot
sns.violinplot(x='cluster', y='max_inten', data=final_result, palette='muted', ax=ax2)
sample_sizes = final_result['cluster'].value_counts().sort_index()

# Annotate the plot with sample sizes
# Get the x coordinates for the annotations
x_coords = range(len(sample_sizes))
for x, size in zip(x_coords, sample_sizes):
    ax2.text(x, ax2.get_ylim()[0], f'n={size}', horizontalalignment='center', size='medium', color='black', weight='semibold')

ax2.set_title('TC associated Maximum Ridge Intensity')
ax2.set_xlabel('Cluster')
ax2.set_ylabel('Max Intensity (GPM)')

# Adjust layout for better spacing and display the plot
plt.tight_layout()
plt.savefig(f'/Users/xiaoyubai/Documents/TC_ridges/figures/kmeans/{season}_ridge_TC.png', dpi=300, bbox_inches="tight")
