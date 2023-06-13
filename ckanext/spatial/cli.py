# encoding: utf-8
import click
import logging

from prometheus_flask_exporter import PrometheusMetrics

from bin import ckan_pycsw
import ckanext.spatial.util as util


log = logging.getLogger(__name__)

def get_commands():
    return [
        spatial,
        spatial_validation,
        spatial_csw
    ]


@click.group(u"spatial-validation", short_help=u"Spatial formats validation commands")
def spatial_validation():
    pass


@spatial_validation.command()
@click.argument('pkg', required=False)
def report(pkg):
    """
    Performs validation on the harvested metadata, either for all
    packages or the one specified.
    """

    return util.report(pkg)


@spatial_validation.command('report-csv')
@click.argument('filepath')
def report_csv(filepath):
    """
    Performs validation on all the harvested metadata in the db and
    writes a report in CSV format to the given filepath.
    """
    return util.report_csv(filepath)


@spatial_validation.command('file')
@click.argument('filepath')
def validate_file(filepath):
    """Performs validation on the given metadata file."""
    return util.validate_file(filepath)


@click.group(short_help=u"Performs spatially related operations.")
def spatial():
    pass


@spatial.command()
@click.argument('srid', required=False)
def initdb(srid):
    """
    Creates the necessary tables. You must have PostGIS installed
    and configured in the database.
    You can provide the SRID of the geometry column. Default is 4326.
    """
    return util.initdb(srid)


@spatial.command('extents')
def update_extents():
    """
    Creates or updates the extent geometry column for datasets with
    an extent defined in the 'spatial' extra.
    """

    return util.update_extents()


@click.group(u"ckan-pycsw", short_help=u"Spatial CSW commands")
def spatial_csw():
    """Manages the CKAN-pycsw integration
    """
    pass


@spatial_csw.command()
@click.option(
    "-p",
    "--pycsw_config",
    default='default.cfg',
    help="pycsw config file to use.",
)
def setup(pycsw_config):
    '''Manages the CKAN-pycsw integration

    ckan ckan-pycsw setup [-p]
        Setups the necessary pycsw table on the db.

All commands require the pycsw configuration file. By default it will try
to find a file called 'default.cfg' in the same directory, but you'll
probably need to provide the actual location with the -p option.

    ckan ckan-pycsw setup -p /etc/ckan/default/pycsw.cfg

    '''
    config = ckan_pycsw._load_config(pycsw_config)
    ckan_pycsw.setup_db(config)

    from flask import current_app

    if not hasattr(current_app, '_metrics'):
        metrics = PrometheusMetrics(current_app, excluded_paths=['/metrics', '/healthcheck'])
        current_app._metrics = metrics


@spatial_csw.command()
@click.option(
    "-p",
    "--pycsw_config",
    default='default.cfg',
    help="pycsw config file to use.",
)
def clear(pycsw_config):
    '''Manages the CKAN-pycsw integration

    ckan ckan-pycsw clear [-p]
        Removes all records from the pycsw table.

All commands require the pycsw configuration file. By default it will try
to find a file called 'default.cfg' in the same directory, but you'll
probably need to provide the actual location with the -p option.

    ckan ckan-pycsw setup -p /etc/ckan/default/pycsw.cfg

    '''
    config = ckan_pycsw._load_config(pycsw_config)
    ckan_pycsw.clear(config)


@spatial_csw.command()
@click.option(
    "-p",
    "--pycsw_config",
    default='default.cfg',
    help="pycsw config file to use.",
)
@click.option(
    "-u",
    "--ckan_url",
    default='http://localhost',
    help="CKAN instance to import the datasets from.",
)
def load(pycsw_config, ckan_url):
    '''Manages the CKAN-pycsw integration

    ckan ckan-pycsw load [-p] [-u]
        Loads CKAN datasets as records into the pycsw db.

All commands require the pycsw configuration file. By default it will try
to find a file called 'default.cfg' in the same directory, but you'll
probably need to provide the actual location with the -p option.

The load command requires a CKAN URL from where the datasets will be pulled.
By default it is set to 'http://localhost', but you can define it with the -u
option:

    ckan ckan-pycsw load -p /etc/ckan/default/pycsw.cfg -u http://ckan.instance.org

    '''
    config = ckan_pycsw._load_config(pycsw_config)
    ckan_url = ckan_url.rstrip('/') + '/'
    ckan_pycsw.load(config, ckan_url)


@spatial_csw.command()
@click.option(
    "-p",
    "--pycsw_config",
    default='default.cfg',
    help="pycsw config file to use.",
)
@click.option(
    "-u",
    "--ckan_url",
    default='http://localhost',
    help="CKAN instance to import the datasets from.",
)
def set_keywords(pycsw_config, ckan_url):
    '''Manages the CKAN-pycsw integration

    ckan ckan-pycsw set-keywords [-p] [-u]
        Sets pycsw server metadata keywords from CKAN site tag list.

All commands require the pycsw configuration file. By default it will try
to find a file called 'default.cfg' in the same directory, but you'll
probably need to provide the actual location with the -p option.

    ckan ckan-pycsw set-keywords -p /etc/ckan/default/pycsw.cfg

The set_keywords command requires a CKAN URL from where the datasets will be pulled.
By default it is set to 'http://localhost', but you can define it with the -u
option:

    ckan ckan-pycsw set-keywords -p /etc/ckan/default/pycsw.cfg -u http://ckan.instance.org

    '''
    config = ckan_pycsw._load_config(pycsw_config)
    ckan_url = ckan_url.rstrip('/') + '/'
    ckan_pycsw.set_keywords(pycsw_config, config, ckan_url)
