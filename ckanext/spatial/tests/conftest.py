# -*- coding: utf-8 -*-

import pytest

import ckanext.harvest.model as harvest_model

# to prevent all tables from being deleted
model.repo.tables_created_and_initialised = True


@pytest.fixture
def harvest_setup():
    harvest_model.setup()
