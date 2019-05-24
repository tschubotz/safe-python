import pytest
from click.testing import CliRunner


@pytest.fixture(scope='module')
def runner(request):
    return CliRunner()
