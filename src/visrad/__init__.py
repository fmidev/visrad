# SPDX-FileCopyrightText: 2024-present Jussi Tiira <jussi.tiira@fmi.fi>
#
# SPDX-License-Identifier: MIT

import os

import xarray as xr
import matplotlib.pyplot as plt
    

def read_sweep(filename, group="sweep_0", engine="odim"):
    """open_dataset xradar wrapper"""
    return xr.open_dataset(filename, group=group, engine=engine).xradar.georeference()


def plot_ppi(da, ax=None, **kws):
    """plot PPI"""
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()
    da.plot(ax=ax, x="x", y="y", **kws)
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