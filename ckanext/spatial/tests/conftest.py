# -*- coding: utf-8 -*-

import pytest

from ckan.model import Session
from ckanext.spatial.model.package_extent import setup as spatial_db_setup
import ckanext.harvest.model as harvest_model


def _create_postgis_extension():
    Session.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    Session.commit()


def create_postgis_tables():
    _create_postgis_extension()


@pytest.fixture
def clean_postgis():
    Session.execute("DROP TABLE IF EXISTS package_extent")
    Session.execute("DROP EXTENSION IF EXISTS postgis CASCADE")
    Session.commit()

@pytest.fixture
def harvest_setup():
    harvest_model.setup()


@pytest.fixture
def spatial_setup():
    create_postgis_tables()
    spatial_db_setup()