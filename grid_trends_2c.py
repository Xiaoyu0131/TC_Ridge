#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 11:49:52 2026

@author: xiaoyubai
"""

import xarray as xr
import numpy as np

path = '/scratch/xiaoyu/data/ERA5/daily/Z_star500/'
files = [f'{path}z_star_{year}.nc' for year in range(1977, 2025)]

ds = xr.open_mfdataset(
    files,
    combine='by_coords',
    chunks={'TIME': 365}   # requires dask
).rename({'LONGITUDE':'lon', 'LATITUDE':'lat', 'TIME':'time'})

z = ds['Z_STAR']
if (z.lat.diff('lat') < 0).all():
    z = z.sortby('lat')

# 30–80N subset
z_reg = z.sel(lat=slice(30, 80))

def seasonal_grid_series(da, months):
    # returns (year, lat, lon)
    zz = da.sel(time=da['time.month'].isin(months))
    return zz.groupby('time.year').mean('time')

# (year, lat, lon)
z_jjas = seasonal_grid_series(z_reg, [6,7,8,9])
z_ond  = seasonal_grid_series(z_reg, [10,11,12])

# z_jjas: (year, lat, lon)
z_jjas = z_jjas.chunk({'year': -1})
z_ond  = z_ond.chunk({'year': -1})

# ---- trends: slope per year at each grid point ----
fit_jjas = z_jjas.polyfit(dim='year', deg=1, skipna=True)
fit_ond  = z_ond.polyfit(dim='year', deg=1, skipna=True)

# xarray stores coefficients as polyfit_coefficients(degree, lat, lon)
slope_jjas = fit_jjas['polyfit_coefficients'].sel(degree=1) * 10.0  # per decade
slope_ond  = fit_ond['polyfit_coefficients'].sel(degree=1) * 10.0

slope_jjas.name = 'Z_STAR_JJAS_slope_decade'
slope_ond.name  = 'Z_STAR_OND_slope_decade'
slope_jjas.attrs['units'] = 'm/decade'
slope_ond.attrs['units']  = 'm/decade'
slope_jjas.attrs['description'] = 'Linear trend of JJAS seasonal-mean Z* over 30-80N'
slope_ond.attrs['description']  = 'Linear trend of OND seasonal-mean Z* over 30-80N'

out = xr.Dataset({'slope_jjas': slope_jjas, 'slope_ond': slope_ond})
out.attrs['region'] = '30N-80N'
out.attrs['source'] = 'ERA5 Z_STAR daily 1940-2024'
out.attrs['method'] = 'Seasonal mean by year, then gridpoint linear trend (polyfit), slope in GPM/decade'

out.to_netcdf('/scratch/xiaoyu/data/TC_ridge/trend/Z_STAR_30_80N_grid_trend_JJAS_OND.nc')

# %%
from scipy import stats

def slope_p(y, x):
    # y: (year,)  x: (year,)
    mask = np.isfinite(y) & np.isfinite(x)
    if mask.sum() < 3:
        return np.nan, np.nan
    res = stats.linregress(x[mask], y[mask])
    return res.slope * 10.0, res.pvalue  # per decade, p

years = z_jjas['year'].values.astype(float)

slope_jjas, p_jjas = xr.apply_ufunc(
    slope_p,
    z_jjas,
    xr.DataArray(years, dims='year'),
    input_core_dims=[['year'], ['year']],
    output_core_dims=[[], []],
    vectorize=True,
    dask='parallelized',
    output_dtypes=[float, float],
)

slope_ond, p_ond = xr.apply_ufunc(
    slope_p,
    z_ond,
    xr.DataArray(years, dims='year'),
    input_core_dims=[['year'], ['year']],
    output_core_dims=[[], []],
    vectorize=True,
    dask='parallelized',
    output_dtypes=[float, float],
)

ds_out = xr.Dataset({
    'slope_jjas_m_decade': slope_jjas,
    'p_jjas': p_jjas,
    'slope_ond_m_decade': slope_ond,
    'p_ond': p_ond,
})

ds_out.to_netcdf('/scratch/xiaoyu/data/TC_ridge/trend/Z_STAR_30_80N_grid_trend_JJAS_OND_with_p.nc')

# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# ----------------------------
# Load your trend + p-value file
# ----------------------------
fn = "/scratch/xiaoyu/data/TC_ridge/trend/Z_STAR_30_80N_grid_trend_JJAS_OND_with_p.nc"
ds = xr.open_dataset(fn)

# Expecting these names from the earlier snippet:
#   slope_jjas_m_decade, p_jjas, slope_ond_m_decade, p_ond
slope_jjas = ds["slope_jjas_m_decade"]
p_jjas     = ds["p_jjas"]

slope_ond  = ds["slope_ond_m_decade"]
p_ond      = ds["p_ond"]


# ----------------------------
# Plot helper
# ----------------------------
def plot_slope_with_pmask(
    slope_da,
    p_da,
    title,
    out_png=None,
    levels=None,
    projection=None,
):
    """
    slope_da: (lat, lon) slope in m/decade
    p_da:     (lat, lon) p-values
    mask:     p < 0.1 stippling
    """
    if projection is None:
        projection = ccrs.Robinson(central_longitude=180)

    # Choose contour levels if not provided
    if levels is None:
        vmax = np.nanpercentile(np.abs(slope_da.values), 98)
        vmax = max(vmax, 0.1)  # avoid tiny range
        levels = np.linspace(-vmax, vmax, 21)

    fig = plt.figure(figsize=(12, 5.5))
    ax = plt.axes(projection=projection)

    # Main slope field
    cf = ax.contourf(
        slope_da["lon"],
        slope_da["lat"],
        slope_da,
        levels=levels,
        cmap="RdBu_r",
        extend="both",
        transform=ccrs.PlateCarree(),
    )

    ax.coastlines(linewidth=0.8)
    ax.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=0.4, alpha=0.6)

    # p<0.1 mask as stippling (scatter)
    sig = (p_da < 0.1) & np.isfinite(p_da) & np.isfinite(slope_da)

    # Subsample for readability (adjust step as needed)
    step_lat = 3
    step_lon = 3
    lat2 = slope_da["lat"].values[::step_lat]
    lon2 = slope_da["lon"].values[::step_lon]

    sig2 = sig.values[::step_lat, ::step_lon]
    LON2, LAT2 = np.meshgrid(lon2, lat2)

    ax.scatter(
        LON2[sig2],
        LAT2[sig2],
        s=3,
        marker=".",
        transform=ccrs.PlateCarree(),
        linewidths=0,
        alpha=0.8,
        color="k",
    )

    ax.set_title(title, fontsize=14)

    cbar = plt.colorbar(cf, ax=ax, orientation="horizontal", pad=0.06, shrink=0.4)
    cbar.set_label("Z* trend (m / decade)")

    plt.tight_layout()

    if out_png is not None:
        plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.show()


# ----------------------------
# Make plots
# ----------------------------
plot_slope_with_pmask(
    slope_jjas, p_jjas,
    title="JJAS Z* trend (30–80°N) with p<0.1 stippling",
    out_png="/scratch/xiaoyu/data/TC_ridge/trend/fig_slope_JJAS_p01.png",
)

plot_slope_with_pmask(
    slope_ond, p_ond,
    title="OND Z* trend (30–80°N) with p<0.1 stippling",
    out_png="/scratch/xiaoyu/data/TC_ridge/trend/fig_slope_OND_p01.png",
)
