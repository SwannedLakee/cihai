import os
import typing as t
import zipfile

import pytest

import sqlalchemy

from cihai.data.unihan.constants import UNIHAN_FILES


if t.TYPE_CHECKING:
    from .types import UnihanOptions


@pytest.fixture
def fixture_path() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))


@pytest.fixture
def test_config_file(fixture_path: str) -> str:
    return os.path.join(fixture_path, "test_config.yml")


@pytest.fixture
def zip_path(tmpdir: str) -> str:
    return tmpdir.join("Unihan.zip")


@pytest.fixture
def zip_file(zip_path: str, fixture_path: str) -> zipfile.ZipFile:
    _files = []
    for f in UNIHAN_FILES:
        _files += [os.path.join(fixture_path, f)]
    zf = zipfile.ZipFile(str(zip_path), "a")
    for f in _files:
        zf.write(f, os.path.basename(f))
    zf.close()
    return zf


@pytest.fixture
def unihan_options(
    zip_file: zipfile.ZipFile, zip_path: str, tmpdir: str
) -> "UnihanOptions":
    return {
        "source": str(zip_path),
        "work_dir": str(tmpdir),
        "zip_path": str(tmpdir.join("downloads").join("Moo.zip")),
    }


@pytest.fixture(scope="function")
def tmpdb_file(tmpdir: str) -> str:
    return tmpdir.join("test.db")


@pytest.fixture(scope="session")
def engine() -> sqlalchemy.Engine:
    return sqlalchemy.create_engine("sqlite:///")


@pytest.fixture(scope="session")
def metadata() -> sqlalchemy.MetaData:
    return sqlalchemy.MetaData()
