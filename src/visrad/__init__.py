# SPDX-FileCopyrightText: 2024-present Jussi Tiira <jussi.tiira@fmi.fi>
#
# SPDX-License-Identifier: MIT

import os

import h5py
import xarray as xr
import xradar as xd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def read_odim_source(odimfile):
    """read odim source data as dict"""
    with h5py.File(odimfile, "r") as f:
        src = f['/what'].attrs['source'].decode()
    src = src.split(',')
    return dict([s.split(':') for s in src])


def read_sweep(filename, group="sweep_0", engine="odim"):
    """open_dataset xradar wrapper"""
    return xr.open_dataset(filename, group=group, engine=engine).xradar.georeference()


def plot_ppi(da, ax=None, **kws):
    """plot PPI"""
    proj_crs = xd.georeference.get_crs(da)
    cart_crs = ccrs.Projection(proj_crs)
    tgt_crs = ccrs.AzimuthalEquidistant(
        central_latitude=float(da.latitude),
        central_longitude=float(da.longitude),
    )
    if ax is None:
        ax = plt.axes(projection=tgt_crs)
    fig = ax.get_figure()
    da.plot(ax=ax, x="x", y="y", transform=cart_crs, **kws)
    ax.coastlines()
    fig.tight_layout()
    return ax


def plot_dbz(dbz, minv=-10, **kws):
    """plot reflectivity"""
    dbz = dbz.where(dbz >= minv)
    ax = plot_ppi(dbz, vmin=-22, vmax=60, cmap="gist_ncar", **kws)
    return ax


def plot_rings(ds, gates=(10,), **kws):
    """plot rings at given range gates"""
    rings = ds.TH.copy()
    rings.data.fill(0)
    rings.data[:, gates] = 1.0
    ax = plot_ppi(rings.where(rings > 0), colors="k", levels=[0.5], add_colorbar=False, **kws)
    return ax


if __name__ == "__main__":
    filename0 = os.path.expanduser("~/data/polar/fiuta/202208051330_radar.polar.fiuta.h5")
    dbz = read_sweep(filename0, group="sweep_0")['DBZH']
    ax = plot_dbz(dbz)
    read_odim_source(filename0)