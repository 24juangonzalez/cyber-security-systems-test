"""Small constructor checks that never echo supplied values in errors."""

import re
from datetime import datetime
from enum import Enum
from unicodedata import category

_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{0,127}\Z")


def identifier(value: str, field: str) -> None:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"{field} must be a valid identifier of 1 to 128 characters")


def text(value: str, field: str, limit: int = 512) -> None:
    if (
        not isinstance(value, str)
        or not value.strip()
        or len(value) > limit
        or any(category(character).startswith("C") for character in value)
    ):
        raise ValueError(f"{field} must be nonblank text without control characters")


def enum_value(value: Enum, expected: type[Enum], field: str) -> None:
    if not isinstance(value, expected):
        raise ValueError(f"{field} must be a {expected.__name__} member")


def timestamp(value: datetime, field: str) -> None:
    if not isinstance(value, datetime) or value.utcoffset() is None:
        raise ValueError(f"{field} must be a timezone-aware datetime")


def text_tuple(values: tuple[str, ...], field: str) -> None:
    if not isinstance(values, tuple):
        raise ValueError(f"{field} must be an immutable tuple")
    for value in values:
        text(value, field)


def identifiers(values: tuple[str, ...], field: str) -> None:
    if not isinstance(values, tuple):
        raise ValueError(f"{field} must be an immutable tuple")
    for value in values:
        identifier(value, field)
    if len(values) != len(set(values)):
        raise ValueError(f"{field} must not contain duplicate identifiers")
