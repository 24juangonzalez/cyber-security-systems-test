"""Bounded offline JSON ingestion. No URL fetching, dynamic code, or SDK calls."""

import hashlib
import json
import os
import stat
from dataclasses import fields, replace
from datetime import datetime
from pathlib import Path
from typing import Any

from cyber_security_systems.domain import (
    PARSER_VERSION,
    SCHEMA_VERSION,
    Completeness,
    Criticality,
    Effect,
    Entity,
    EntityType,
    Evidence,
    ObservationState,
    Policy,
    Provenance,
    Relationship,
    RelationshipType,
    SanitizationState,
    Scope,
    Sensitivity,
    Snapshot,
    SourceType,
)

MAX_BYTES = 4 * 1024 * 1024
MAX_ENTITIES = 2000
MAX_RELATIONSHIPS = 10000
MAX_EVIDENCE = 10000


class FixtureError(ValueError):
    """A safe error message that does not disclose imported values or paths."""


def _object(value: Any, allowed: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or not set(value) <= allowed:
        raise FixtureError("expected an object with supported fields")
    return dict(value)


def _record(value: Any, model: type) -> dict[str, Any]:
    return _object(value, {field.name for field in fields(model)})


def _time(value: Any) -> datetime:
    if not isinstance(value, str):
        raise FixtureError("timestamp must be an ISO 8601 string")
    return datetime.fromisoformat(value)


def _array(value: Any, limit: int) -> list:
    if not isinstance(value, list) or len(value) > limit:
        raise FixtureError("expected an array within the supported size limit")
    return value


def _scope(value: Any) -> Scope:
    data = _record(value, Scope)
    for key in ("observed_from", "observed_until"):
        data[key] = _time(data[key])
    data["completeness"] = Completeness(data["completeness"])
    data["issues"] = tuple(_array(data.get("issues", []), 100))
    return Scope(**data)


def _entity(value: Any) -> Entity:
    data = _record(value, Entity)
    data["kind"] = EntityType(data["kind"])
    for name, enum in (("criticality", Criticality), ("sensitivity", Sensitivity)):
        if name in data:
            data[name] = enum(data[name])
    return Entity(**data)


def _evidence(value: Any) -> Evidence:
    data = _record(value, Evidence)
    data["observed_at"] = _time(data["observed_at"])
    data["source_type"] = SourceType(data["source_type"])
    data["sanitization"] = SanitizationState(data["sanitization"])
    data["completeness"] = Completeness(data["completeness"])
    if (
        data["source_type"] is not SourceType.SYNTHETIC_FIXTURE
        or data["sanitization"] is not SanitizationState.SYNTHETIC
    ):
        raise FixtureError("this adapter accepts declared synthetic evidence only")
    provenance = _record(data["provenance"], Provenance)
    provenance["collected_at"] = _time(provenance["collected_at"])
    data["provenance"] = Provenance(**provenance)
    if data["provenance"].permitted_use != "synthetic_demo":
        raise FixtureError("unsupported permitted use")
    record = Evidence(**data)
    digest = hashlib.sha256((record.value or "").encode()).hexdigest()
    if record.provenance.integrity_reference != "sha256:" + digest:
        raise FixtureError("evidence value integrity mismatch")
    return record


def _relationship(value: Any) -> Relationship:
    data = _record(value, Relationship)
    data["kind"] = RelationshipType(data["kind"])
    data["observation"] = ObservationState(data["observation"])
    data["evidence_ids"] = tuple(_array(data["evidence_ids"], 100))
    data["conditions"] = tuple(_array(data.get("conditions", []), 100))
    if data.get("policy") is not None:
        policy = _record(data["policy"], Policy)
        policy["effect"] = Effect(policy["effect"])
        if policy.get("expires_at") is not None:
            policy["expires_at"] = _time(policy["expires_at"])
        data["policy"] = Policy(**policy)
    # Preserve missing references as incomplete evidence, never verified absence.
    if not data["evidence_ids"]:
        data["observation"] = ObservationState.UNKNOWN
    return Relationship(**data)


def _unique(records: tuple) -> None:
    if len({record.id for record in records}) != len(records):
        raise FixtureError("duplicate record identifiers")


def parse_fixture(raw: Any) -> Snapshot:
    """Validate a decoded JSON object; missing evidence stays assessably incomplete."""
    try:
        data = _object(
            raw,
            {
                "schema_version",
                "parser_version",
                "scope",
                "entities",
                "evidence",
                "relationships",
            },
        )
        if (
            data["schema_version"] != SCHEMA_VERSION
            or data["parser_version"] != PARSER_VERSION
        ):
            raise FixtureError("unsupported schema or parser version")
        scope = _scope(data["scope"])
        entities = tuple(
            _entity(item) for item in _array(data["entities"], MAX_ENTITIES)
        )
        evidence = tuple(
            _evidence(item) for item in _array(data["evidence"], MAX_EVIDENCE)
        )
        relationships = tuple(
            _relationship(item)
            for item in _array(data["relationships"], MAX_RELATIONSHIPS)
        )
        for records in (entities, evidence, relationships):
            _unique(records)
        ids = {entity.id for entity in entities}
        if any(
            edge.source_id not in ids or edge.destination_id not in ids
            for edge in relationships
        ):
            raise FixtureError("relationship endpoint is missing")
        digest = hashlib.sha256(
            json.dumps(raw, sort_keys=True, allow_nan=False).encode()
        ).hexdigest()
        return Snapshot(
            scope=scope,
            entities=entities,
            evidence=evidence,
            relationships=relationships,
            input_sha256=digest,
        )
    except FixtureError:
        raise
    except (KeyError, TypeError, ValueError, OverflowError, RecursionError):
        raise FixtureError("invalid fixture field, type, or required value") from None


def _pairs(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise FixtureError("duplicate JSON object key")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise FixtureError("non-finite JSON numbers are unsupported")


def load_fixture_bytes(payload: bytes) -> Snapshot:
    """Validate bounded uploaded bytes with the same contract as local files."""
    try:
        if len(payload) > MAX_BYTES:
            raise FixtureError("input exceeds the size limit")
        raw = json.loads(payload, object_pairs_hook=_pairs, parse_constant=_constant)
        snapshot = parse_fixture(raw)
        return replace(snapshot, input_sha256=hashlib.sha256(payload).hexdigest())
    except FixtureError:
        raise
    except (ValueError, RecursionError):
        raise FixtureError("unable to read a supported JSON fixture") from None


def load_fixture(path: Path) -> Snapshot:
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_BYTES:
            raise FixtureError("input must be a regular file within the size limit")
        flags = os.O_RDONLY
        for name in ("O_NONBLOCK", "O_NOFOLLOW", "O_BINARY"):
            flags |= getattr(os, name, 0)
        descriptor = os.open(path, flags)
        with os.fdopen(descriptor, "rb") as stream:
            info = os.fstat(stream.fileno())
            # Check identity before reading, including where O_NOFOLLOW is absent.
            after = path.lstat()
            if (
                not stat.S_ISREG(after.st_mode)
                or not os.path.samestat(before, info)
                or not os.path.samestat(after, info)
            ):
                raise FixtureError("input changed while opening")
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                raise FixtureError("input must be a regular file within the size limit")
            payload = stream.read(MAX_BYTES + 1)
        return load_fixture_bytes(payload)
    except FixtureError:
        raise
    except (OSError, ValueError, RecursionError):
        raise FixtureError("unable to read a supported JSON fixture") from None
