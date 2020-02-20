import click
import os,sys
sys.path.append(os.path.abspath('crossroads_scripts'))
from evolve_structure import get_evolved_structure

@click.command()
@click.option('--name', default='myeffect', help='name of the effect to create')
@click.argument('dryfile', type=click.Path(exists=True))
@click.argument('wetfile', type=click.Path(exists=True))
def main(name, dryfile, wetfile):
    """
    Generates an effect to make DRYFILE sound like WETFILE
    """
    click.echo('Running Crossroads for {}'.format(name))
    get_evolved_structure(name, dryfile, name + '/' + name + '.wav', wetfile)


if __name__ == '__main__':
    main()
