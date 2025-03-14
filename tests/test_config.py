"""Test configuration for cihai."""

from __future__ import annotations

import os
import pathlib
import typing as t

from appdirs import AppDirs

from cihai.config import expand_config

if t.TYPE_CHECKING:
    import pytest

    from cihai.types import UntypedDict


#: XDG App directory locations
dirs = AppDirs("cihai", "cihai team")  # appname  # app author


def test_expand_config_xdg_vars() -> None:
    """Test resolution of XDG Variables."""
    initial_dict: UntypedDict = {
        "dirs": {"cache": "{user_cache_dir}", "data": "{user_cache_dir}/data"},
    }

    expected_dict: UntypedDict = {
        "dirs": {
            "cache": pathlib.Path(dirs.user_cache_dir),
            "data": pathlib.Path(dirs.user_cache_dir) / "data",
        },
    }

    expand_config(initial_dict, dirs)
    assert initial_dict == expected_dict


def test_expand_config_user_vars() -> None:
    """Test resolution of home directory ("~")."""
    initial_dict: UntypedDict = {"dirs": {"cache": "~"}}

    expected_dict: UntypedDict = {"dirs": {"cache": pathlib.Path.home()}}

    expand_config(initial_dict, dirs)
    assert initial_dict == expected_dict


def test_expand_config_env_vars(tmpdir: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test resolution of environment variables."""
    monkeypatch.setenv("MYDIR", str(tmpdir))
    initial_dict: UntypedDict = {"dirs": {"cache": "${MYDIR}"}}

    expected_dict: UntypedDict = {
        "dirs": {"cache": pathlib.Path(str(os.environ.get("MYDIR")))},
    }

    expand_config(initial_dict, dirs)
    assert initial_dict == expected_dict
