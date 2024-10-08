"""command line interface"""

import click
import numpy as np

from visrad import plot_dbz, read_sweep, read_odim_source


@click.command()
@click.option('-o', '--output', metavar='FILE', help='output file')
@click.argument('file')
@click.version_option()
def visrad(output, file):
    """plot radar data"""
    ds = read_sweep(file, group="sweep_0")
    dbz = ds['DBZH']
    ax = plot_dbz(dbz)
    if not output:
        output = file.replace(".h5", ".png")
    fig = ax.get_figure()
    nod = read_odim_source(file)['NOD']
    # set title
    t = dbz.time.values[0]
    timestamp = str(np.datetime_as_string(t, unit='m'))
    title = f"{nod} {timestamp}"
    ax.set_title(title)
    fig.savefig(output)