#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 19:26:04 2025

@author: xiaoyubai
"""

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import seaborn as sns
from scipy.stats import ks_2samp
from statannotations.Annotator import Annotator
import numpy as np
np.float = float

# %%
data = pd.read_csv('/Users/xiaoyubai/Documents/TC_ridges/data/ridge/ridge_v2_TC_with_quadrant.csv')
p_values_inten_recur = {}
quadrants = ['South', 'North', 'Central']
# Perform KS test for 'max_inten' among quadrants
for i in quadrants:
    for j in quadrants:
        if i < j:  # This avoids self-comparison and redundant comparisons
            group1 = data[data['recur NS'] == i]['max_inten'].dropna()
            group2 = data[data['recur NS'] == j]['max_inten'].dropna()
            stat, p_value = ks_2samp(group1, group2)
            p_values_inten_recur[(i, j)] = p_value

# Print out the results for max_inten
print("\nP-values for Max Intensity comparisons among quadrants:")
for pair, p_value in p_values_inten_recur.items():
    print(f"Quadrants {pair}: p-value = {p_value:.4f}")
    
p_values_lat_recur = {}
quadrants = ['South', 'North', 'Central']
# Perform KS test for 'max_inten' among quadrants
for i in quadrants:
    for j in quadrants:
        if i < j:  # This avoids self-comparison and redundant comparisons
            group1 = data[data['recur NS'] == i]['lat_inten'].dropna()
            group2 = data[data['recur NS'] == j]['lat_inten'].dropna()
            stat, p_value = ks_2samp(group1, group2)
            p_values_lat_recur[(i, j)] = p_value

# Print out the results for max_inten
print("\nP-values for Max Intensity comparisons among quadrants:")
for pair, p_value in p_values_lat_recur.items():
    print(f"Quadrants {pair}: p-value = {p_value:.4f}")
    
p_values_lon_recur = {}
quadrants = ['West', 'East', 'Central']
# Perform KS test for 'max_inten' among quadrants
for i in quadrants:
    for j in quadrants:
        if i < j:  # This avoids self-comparison and redundant comparisons
            group1 = data[data['recur WE'] == i]['lon_inten'].dropna()
            group2 = data[data['recur WE'] == j]['lon_inten'].dropna()
            stat, p_value = ks_2samp(group1, group2)
            p_values_lon_recur[(i, j)] = p_value

# Print out the results for max_inten
print("\nP-values for Max Intensity comparisons among quadrants:")
for pair, p_value in p_values_lon_recur.items():
    print(f"Quadrants {pair}: p-value = {p_value:.4f}")
    

# %%
fig, axs = plt.subplots(1, 3, figsize=(15, 6))
ax1, ax2, ax3 = axs.flatten()
# plt.rcParams['axes.labelsize'] = 16  # Axis labels
# plt.rcParams['axes.titlesize'] = 16  # Axis title size
# plt.rcParams['xtick.labelsize'] = 12 # X tick label size
# plt.rcParams['ytick.labelsize'] = 12 # Y tick label size
# plt.rcParams['legend.fontsize'] = 22 # Legend font size
plt.rcParams['font.size'] = 16       # Default text size

pairs = [('South', 'North'), ('South', 'Central'), ('North', 'Central')]
quadrants = ['South', 'Central', 'North']

color_mapping = {
    'North': '#2166ac',
    'South': '#b2182b',
    'Central': '#ffffbf'
}
palette = [color_mapping[quadrant] for quadrant in quadrants]

sns.violinplot(x='recur NS', y='max_inten', data=data,
            palette=palette, order=quadrants,
            inner='quartile',
            ax=ax1)
ax1.set_title('(c) Ridge Intensity', fontsize = 18)
ax1.set_xlabel('')
ax1.set_ylabel('Intensity (GPM)')

annot = Annotator(ax1, pairs, x='recur NS', y='max_inten', order=quadrants, data=data, plot='violinplot')

# p_values = [0.009 if p < 0.1 else np.nan for p in list(p_values_inten.values())]
p_values = list(p_values_inten_recur.values())

annot.new_plot(ax=ax1, pairs=pairs,
                x='recur NS', y='max_inten', order=quadrants, data=data,
                )
(annot
  .configure(test=None, alpha=0.1, text_format="simple")
  .set_pvalues(pvalues=p_values)
  .annotate())

sns.violinplot(x='recur NS', y='lat_inten', data=data,
            palette=palette, order=quadrants,
            inner='quartile',
            ax=ax2)
# Calculate sample sizes for each category
sample_sizes = data.groupby('recur NS')['lat_inten'].size()

# Annotate each violin with its sample size
for i, (category, size) in enumerate(sample_sizes.items()):
    # Make sure the x positions match your 'order' of categories if used
    ax2.text(i, data['lat_inten'].min() - (data['lat_inten'].max() - data['lat_inten'].min()) * 0.22,  # Adjust position as needed
             f'n={size}', color='black', ha='center', va='center')

ax2.set_title('(d) Ridge Centroid Laitude', fontsize = 18)
ax2.set_xlabel('')
ax2.set_ylabel('Degrees North')

annot = Annotator(ax2, pairs, x='recur NS', y='lat_inten', order=quadrants, data=data, plot='violinplot')

# p_values = [0.009 if p < 0.1 else np.nan for p in list(p_values_inten.values())]
p_values = list(p_values_lat_recur.values())

annot.new_plot(ax=ax2, pairs=pairs,
                x='recur NS', y='lat_inten', order=quadrants, data=data,
                )
(annot
  .configure(test=None, alpha=0.1, text_format="simple")
  .set_pvalues(pvalues=p_values)
  .annotate())

pairs = [('East', 'West'), ('East', 'Central'), ('West', 'Central')]
quadrants = ['West', 'Central', 'East']
color_mapping = {
    'West': '#8c510a',
    'East': '#01665e',
    'Central': '#ffffbf'
}
palette = [color_mapping[quadrant] for quadrant in quadrants]
sns.violinplot(x='recur WE', y='lon_inten', data=data,
            palette=palette, order=quadrants,
            inner='quartile',
            ax=ax3)
ax3.set_title('(e) Ridge Centroid Longitude', fontsize = 18)
ax3.set_xlabel('')
ax3.set_ylabel('Degrees East')
# Calculate sample sizes for each category
sample_sizes = data.groupby('recur WE')['lon_inten'].size()

# Annotate each violin with its sample size
for i, (category, size) in enumerate(sample_sizes.items()):
    # Make sure the x positions match your 'order' of categories if used
    ax3.text(i, data['lon_inten'].min() - (data['lon_inten'].max() - data['lon_inten'].min()) * 0.25,  # Adjust position as needed
             f'n={size}', color='black', ha='center', va='center')


annot = Annotator(ax3, pairs, x='recur WE', y='lon_inten', order=quadrants, data=data, plot='violinplot')

# p_values = [0.009 if p < 0.1 else np.nan for p in list(p_values_inten.values())]
p_values = list(p_values_lon_recur.values())

annot.new_plot(ax=ax3, pairs=pairs,
                x='recur WE', y='lon_inten', order=quadrants, data=data,
                )
(annot
  .configure(test=None, alpha=0.1, text_format="simple")
  .set_pvalues(pvalues=p_values)
  .annotate())
plt.savefig(f'/Users/xiaoyubai/Documents/TC_ridges/figures/new_non_TC/all_TC_violin.png', dpi=300, bbox_inches="tight")
plt.show()