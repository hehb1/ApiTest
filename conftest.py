import pytest

from commons.yaml_util import truncate_yaml


@pytest.fixture(scope='session', autouse=True)
def clean_yaml():
    truncate_yaml()
