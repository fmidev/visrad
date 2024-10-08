"""command line interface"""

import click

from visrad import plot_dbz, read_sweep


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
    ax.get_figure().savefig(output)