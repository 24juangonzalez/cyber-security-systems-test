"""Immutable domain records and their invariants, independent of adapters and SDKs."""

import re
from dataclasses import dataclass, field
from datetime import datetime

from . import _validation as validate
from .enums import (
    Completeness,
    Criticality,
    Effect,
    EntityType,
    ObservationState,
    RelationshipType,
    SanitizationState,
    Sensitivity,
    SourceType,
)

SCHEMA_VERSION = "1.0"
PARSER_VERSION = "synthetic-json-1"


@dataclass(frozen=True, slots=True, kw_only=True)
class Entity:
    """A node; credential nodes describe credentials but never hold their values."""

    id: str
    kind: EntityType
    label: str = field(repr=False)
    criticality: Criticality = Criticality.UNKNOWN
    sensitivity: Sensitivity = Sensitivity.UNKNOWN

    def __post_init__(self) -> None:
        validate.identifier(self.id, "id")
        validate.enum_value(self.kind, EntityType, "kind")
        validate.text(self.label, "label")
        validate.enum_value(self.criticality, Criticality, "criticality")
        validate.enum_value(self.sensitivity, Sensitivity, "sensitivity")


@dataclass(frozen=True, slots=True, kw_only=True)
class Provenance:
    collected_at: datetime
    source_version: str
    parser_version: str
    scope_id: str
    permitted_use: str
    integrity_reference: str

    def __post_init__(self) -> None:
        validate.timestamp(self.collected_at, "collected_at")
        for name in ("source_version", "parser_version", "scope_id", "permitted_use"):
            validate.identifier(getattr(self, name), name)
        if not isinstance(self.integrity_reference, str) or not re.fullmatch(
            r"sha256:[0-9a-f]{64}", self.integrity_reference
        ):
            raise ValueError("integrity_reference must be a SHA-256 reference")


@dataclass(frozen=True, slots=True, kw_only=True)
class Scope:
    id: str
    source_id: str
    observed_from: datetime
    observed_until: datetime
    completeness: Completeness
    issues: tuple[str, ...] = field(default=(), repr=False)

    def __post_init__(self) -> None:
        validate.identifier(self.id, "scope.id")
        validate.identifier(self.source_id, "scope.source_id")
        validate.timestamp(self.observed_from, "observed_from")
        validate.timestamp(self.observed_until, "observed_until")
        if self.observed_from > self.observed_until:
            raise ValueError("scope observation window is reversed")
        validate.enum_value(self.completeness, Completeness, "completeness")
        validate.text_tuple(self.issues, "issues")
        if self.completeness is Completeness.COMPLETE and self.issues:
            raise ValueError("complete scope cannot contain issues")


@dataclass(frozen=True, slots=True, kw_only=True)
class Policy:
    context: str
    effect: Effect
    protocol: str
    port: int
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        validate.identifier(self.context, "policy.context")
        validate.enum_value(self.effect, Effect, "policy.effect")
        validate.identifier(self.protocol, "policy.protocol")
        if type(self.port) is not int or not 1 <= self.port <= 65535:
            raise ValueError("policy.port must be an integer between 1 and 65535")
        if self.expires_at is not None:
            validate.timestamp(self.expires_at, "expires_at")


@dataclass(frozen=True, slots=True, kw_only=True)
class Evidence:
    """Metadata only; sanitization is a caller assertion, not secret detection."""

    id: str
    source_type: SourceType
    source_reference: str = field(repr=False)
    observed_at: datetime
    value: str | None = field(default=None, repr=False)
    sanitization: SanitizationState = SanitizationState.UNKNOWN
    completeness: Completeness = Completeness.UNKNOWN
    collection_error: str | None = field(default=None, repr=False)
    provenance: Provenance | None = None

    def __post_init__(self) -> None:
        validate.identifier(self.id, "id")
        validate.enum_value(self.source_type, SourceType, "source_type")
        validate.text(self.source_reference, "source_reference")
        validate.timestamp(self.observed_at, "observed_at")
        validate.enum_value(self.sanitization, SanitizationState, "sanitization")
        validate.enum_value(self.completeness, Completeness, "completeness")
        if self.value is not None:
            validate.text(self.value, "value", limit=4096)
        if self.collection_error is not None:
            validate.text(self.collection_error, "collection_error")
        self._validate_completeness()
        if self.provenance is not None:
            if not isinstance(self.provenance, Provenance):
                raise ValueError("provenance must be a Provenance record")
            if self.provenance.collected_at < self.observed_at:
                raise ValueError("collection time must not precede observation time")

    def _validate_completeness(self) -> None:
        if self.completeness is Completeness.COMPLETE:
            if self.value is None or self.sanitization is SanitizationState.UNKNOWN:
                raise ValueError("complete evidence requires a value and sanitization")
            if self.collection_error is not None:
                raise ValueError("complete evidence cannot contain a collection error")
        if self.completeness is Completeness.FAILED and self.collection_error is None:
            raise ValueError("failed evidence requires a collection error")


@dataclass(frozen=True, slots=True, kw_only=True)
class Relationship:
    """The fixture adapter and normalization layer check inventory references."""

    id: str
    source_id: str
    destination_id: str
    kind: RelationshipType
    evidence_ids: tuple[str, ...] = ()
    conditions: tuple[str, ...] = field(default=(), repr=False)
    observation: ObservationState = ObservationState.UNKNOWN
    policy: Policy | None = None

    def __post_init__(self) -> None:
        validate.identifier(self.id, "id")
        validate.identifier(self.source_id, "source_id")
        validate.identifier(self.destination_id, "destination_id")
        validate.enum_value(self.kind, RelationshipType, "kind")
        validate.identifiers(self.evidence_ids, "evidence_ids")
        validate.text_tuple(self.conditions, "conditions")
        validate.enum_value(self.observation, ObservationState, "observation")
        if self.policy is not None and not isinstance(self.policy, Policy):
            raise ValueError("policy must be a Policy record")
        if self.observation is not ObservationState.UNKNOWN and not self.evidence_ids:
            raise ValueError(
                "observed or absent relationships require evidence references"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class AnalysisRun:
    id: str
    observed_at: datetime
    completeness: Completeness = Completeness.UNKNOWN
    issues: tuple[str, ...] = field(default=(), repr=False)

    def __post_init__(self) -> None:
        validate.identifier(self.id, "id")
        validate.timestamp(self.observed_at, "observed_at")
        validate.enum_value(self.completeness, Completeness, "completeness")
        validate.text_tuple(self.issues, "issues")
        if self.completeness is Completeness.COMPLETE and self.issues:
            raise ValueError("complete run cannot contain collection issues")
        if self.completeness is Completeness.FAILED and not self.issues:
            raise ValueError("failed run requires a collection issue")


@dataclass(frozen=True, slots=True, kw_only=True)
class Snapshot:
    scope: Scope
    entities: tuple[Entity, ...]
    evidence: tuple[Evidence, ...]
    relationships: tuple[Relationship, ...]
    input_sha256: str
    schema_version: str = SCHEMA_VERSION
    parser_version: str = PARSER_VERSION
