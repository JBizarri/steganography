from shutil import rmtree
from tempfile import mkdtemp

import pytest

TMP_FOLDER = mkdtemp()


@pytest.fixture(scope="session")
def tmp_folder():
    return TMP_FOLDER


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def remove_tmp_dir():
        rmtree(TMP_FOLDER)

    request.addfinalizer(remove_tmp_dir)
