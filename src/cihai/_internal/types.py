"""Internal :term:`type annotations <annotation>`.

Notes
-----
:class:`StrPath` and :class:`StrOrBytesPath` is based on `typeshed's`_.

.. _typeshed's: https://github.com/python/typeshed/blob/5df8de7/stdlib/_typeshed/__init__.pyi#L115-L118
"""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from os import PathLike

    from typing_extensions import TypeAlias

StrPath: TypeAlias = t.Union[str, "PathLike[str]"]  # stable
""":class:`os.PathLike` or :class:`str`"""

StrOrBytesPath: TypeAlias = t.Union[
    str,
    bytes,
    "PathLike[str]",
    "PathLike[bytes]",  # stable
]
""":class:`os.PathLike`, :class:`str` or :term:`bytes-like object`"""
