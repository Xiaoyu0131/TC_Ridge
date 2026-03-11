#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 19:26:37 2025

@author: xiaoyubai
"""

import statsmodels.stats.api as sms
import statsmodels.api as sm
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import ks_2samp
from statannotations.Annotator import Annotator
from statsmodels.graphics.mosaicplot import mosaic

# plt.rcParams['pdf.fonttype'] = 42
# plt.rcParams['ps.fonttype'] = 42
# %%
df = pd.read_csv('/Users/xiaoyubai/Documents/TC_ridges/data/ridge/ridge_v2_TC_with_quadrant.csv')

def add_2d_kde(ax, data, x, y, color, filled=False):
    sns.kdeplot(
        data=data, x=x, y=y, ax=ax,
        levels=6, thresh=0.05,
        fill=filled, alpha=0.25 if filled else 1.0,
        linewidths=1.2, color=color, common_norm=False
    )

# %%
fig, axs = plt.subplots(2, 3, figsize=(34, 18))
ax1, ax2, ax3, ax4, ax5, ax6 = axs.flatten()
plt.rcParams['axes.labelsize'] = 24  # Axis labels
plt.rcParams['axes.titlesize'] = 24  # Axis title size
plt.rcParams['xtick.labelsize'] = 22 # X tick label size
plt.rcParams['ytick.labelsize'] = 22 # Y tick label size
plt.rcParams['legend.fontsize'] = 22 # Legend font size
plt.rcParams['font.size'] = 20       # Default text size

# %%
season = 'summer'
data = df.loc[df['nh season'] == season]
# out = data[['header_ID', 'date']]
# out.to_csv('/Users/xiaoyubai/Documents/TC_ridges/data/TC_days/TC_30N_summer_days.csv')
# %%

sns.regplot(x='recur_latitude', y='max_inten', data=data, ci = 90,
            ax=ax1, color = '#e7298a')
ax1.set_title('Ridge Intensity', fontsize=26)
ax1.text(0.95, 0.95, '(a)', transform=ax1.transAxes, fontsize=26, verticalalignment='top', horizontalalignment='right')
ax1.set_xlim(5, 45)
ax1.set_ylim(50,500)


sns.regplot(x='recur_latitude', y='lat_inten', data=data, ci = 90,
            ax=ax2, color = '#e7298a')

ax2.set_title('Ridge Centroid Laitude', fontsize=26)
ax2.text(0.95, 0.95, '(b)', transform=ax2.transAxes, fontsize=26, verticalalignment='top', horizontalalignment='right')
ax2.set_xlim(5, 45)
ax2.set_ylim(30,80)


sns.regplot(x='recur_latitude', y='lon_inten', data=data, ci = 90,
            ax=ax3, color = '#e7298a')
ax3.set_title('Ridge Centroid Longitude', fontsize=26)
ax3.text(0.95, 0.95, '(c)', transform=ax3.transAxes, fontsize=26, verticalalignment='top', horizontalalignment='right')
ax3.set_xlim(5, 45)
ax3.set_ylim(180, 270)



sns.regplot(x='recur_longitude', y='max_inten', data=data, ci = 90,
            ax=ax4, color = '#e7298a')
# ax4.set_title('Ridge Intensity', fontsize=26)
ax4.text(0.95, 0.95, '(d)', transform=ax4.transAxes, fontsize=26, verticalalignment='top', horizontalalignment='right')
ax4.set_xlim(110, 180)
ax4.set_ylim(50,500)




sns.regplot(x='recur_longitude', y='lat_inten', data=data, ci = 90,
            ax=ax5, color = '#e7298a')
# ax5.set_title('Ridge Centroid Latitude', fontsize=26)
ax5.text(0.95, 0.95, '(e)', transform=ax5.transAxes, fontsize=26, verticalalignment='top', horizontalalignment='right')
ax5.set_xlim(110, 180)
ax5.set_ylim(30,80)


sns.regplot(x='recur_longitude', y='lon_inten', data=data, ci = 90,
            ax=ax6, color = '#e7298a')
# ax6.set_title('Ridge Longitude', fontsize=26)
ax6.text(0.95, 0.95, '(f)', transform=ax6.transAxes, fontsize=26, verticalalignment='top', horizontalalignment='right')
ax6.set_xlim(110, 180)
ax6.set_ylim(180,270)


def annotate_regression(ax, x, y, data):
    import statsmodels.api as sm

    # Add a constant to the data for the intercept
    X = sm.add_constant(data[x])
    y = data[y]

    # Fit the OLS model
    model = sm.OLS(y, X).fit()

    # Get p-value and coefficient
    p_value = model.pvalues[x]
    coef = model.params[x]

    # Choose fontweight based on p-value
    fontweight = 'bold' if p_value < 0.1 else 'normal'

    # Annotate the plot
    ax.text(
        0.05, 0.95,
        f'Peak Season\nCoef: {coef:.2f}\nP-value: {p_value:.2f}',
        color='#e7298a',
        transform=ax.transAxes,
        fontsize=20,
        fontweight=fontweight,
        verticalalignment='top',
        horizontalalignment='left'
    )


# Loop through each subplot and apply the function
subplots = [(ax1, 'recur_latitude', 'max_inten'),
            (ax2, 'recur_latitude', 'lat_inten'),
            (ax3, 'recur_latitude', 'lon_inten'),
            (ax4, 'recur_longitude', 'max_inten'),
            (ax5, 'recur_longitude', 'lat_inten'),
            (ax6, 'recur_longitude', 'lon_inten')]

for ax, x_var, y_var in subplots:
    annotate_regression(ax, x_var, y_var, data)
# %%
season = 'winter'
data = df.loc[df['nh season'] == season]
    
# %%
sns.regplot(x='recur_latitude', y='max_inten', data=data, ci = 90, color='blue',
            ax=ax1)
# ax4.set_title('(d) Ridge Intensity', fontsize=26)
ax1.set_xlabel('TC Recurvature Latitude ')
ax1.set_ylabel('Intensity (GPM)')
add_2d_kde(ax1, df[df['nh season']=='summer'], 'recur_latitude', 'max_inten', '#e7298a', filled=True)
add_2d_kde(ax1, df[df['nh season']=='winter'], 'recur_latitude', 'max_inten', 'blue', filled=True)


sns.regplot(x='recur_latitude', y='lat_inten', data=data, ci = 90, color='blue',
            ax=ax2)

ax2.set_xlabel('TC Recurvature Latitude')
ax2.set_ylabel('Ridge Laitude (Degrees North)')
add_2d_kde(ax2, df[df['nh season']=='summer'], 'recur_latitude', 'lat_inten', '#e7298a', filled=True)
add_2d_kde(ax2, df[df['nh season']=='winter'], 'recur_latitude', 'lat_inten', 'blue', filled=True)

sns.regplot(x='recur_latitude', y='lon_inten', data=data, ci = 90, color='blue',
            ax=ax3)
ax3.set_xlabel('TC Recurvature Latitude')
ax3.set_ylabel('Ridge Longitude (Degrees East)')
add_2d_kde(ax3, df[df['nh season']=='summer'], 'recur_latitude', 'lon_inten', '#e7298a', filled=True)
add_2d_kde(ax3, df[df['nh season']=='winter'], 'recur_latitude', 'lon_inten', 'blue', filled=True)



sns.regplot(x='recur_longitude', y='max_inten', data=data, ci = 90, color='blue',
            ax=ax4)
ax4.set_xlabel('TC Recurvature Longitude')
ax4.set_ylabel('Intensity (GPM)')
add_2d_kde(ax4, df[df['nh season']=='summer'], 'recur_longitude', 'max_inten', '#e7298a', filled=True)
add_2d_kde(ax4, df[df['nh season']=='winter'], 'recur_longitude', 'max_inten', 'blue', filled=True)

sns.regplot(x='recur_longitude', y='lat_inten', data=data, ci = 90, color='blue',
            ax=ax5)
# ax6.set_title('(f) Ridge Longitude', fontsize=26)
ax5.set_xlabel('TC Recurvature Longitude')
ax5.set_ylabel('Ridge Laitude (Degrees North)')
add_2d_kde(ax5, df[df['nh season']=='summer'], 'recur_longitude', 'lat_inten', '#e7298a', filled=True)
add_2d_kde(ax5, df[df['nh season']=='winter'], 'recur_longitude', 'lat_inten', 'blue', filled=True)

sns.regplot(x='recur_longitude', y='lon_inten', data=data, ci = 90, color='blue',
            ax=ax6)
# ax6.set_title('(f) Ridge Longitude', fontsize=26)
ax6.set_xlabel('TC Recurvature Longitude')
ax6.set_ylabel('Ridge Longitude (Degrees East)')
add_2d_kde(ax6, df[df['nh season']=='summer'], 'recur_longitude', 'lon_inten', '#e7298a', filled=True)
add_2d_kde(ax6, df[df['nh season']=='winter'], 'recur_longitude', 'lon_inten', 'blue', filled=True)

def annotate_regression(ax, x, y, data):
    import statsmodels.api as sm

    # Add a constant to the data for the intercept
    X = sm.add_constant(data[x])
    y = data[y]

    # Fit the OLS model
    model = sm.OLS(y, X).fit()

    # Get p-value and coefficient
    p_value = model.pvalues[x]
    coef = model.params[x]

    # Choose fontweight based on p-value
    fontweight = 'bold' if p_value < 0.1 else 'normal'

    # Annotate the plot
    ax.text(
        0.95, 0.05,
        f'Late Season\nCoef: {coef:.2f}\nP-value: {p_value:.2f}',
        color='blue',
        transform=ax.transAxes,
        fontsize=20,
        fontweight=fontweight,
        verticalalignment='bottom',
        horizontalalignment='right'
    )

# Loop through each subplot and apply the function
subplots = [(ax1, 'recur_latitude', 'max_inten'),
            (ax2, 'recur_latitude', 'lat_inten'),
            (ax3, 'recur_latitude', 'lon_inten'),
            (ax4, 'recur_longitude', 'max_inten'),
            (ax5, 'recur_longitude', 'lat_inten'),
            (ax6, 'recur_longitude', 'lon_inten')]

for ax, x_var, y_var in subplots:
    annotate_regression(ax, x_var, y_var, data)


# %%
plt.savefig(f'/Users/xiaoyubai/Documents/TC_ridges/figures/new_non_TC/reg_panel_ridge_char_summer_winter_90.png', dpi=300, bbox_inches="tight")
plt.show()