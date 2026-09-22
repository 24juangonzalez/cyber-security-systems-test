"""Shared domain vocabulary. Values are part of the serialized input contract."""

from enum import StrEnum


class EntityType(StrEnum):
    IDENTITY = "identity"
    CREDENTIAL = "credential"
    ACCESS_GROUP = "access_group"
    REMOTE_ACCESS_SERVICE = "remote_access_service"
    HOST = "host"
    NETWORK_ZONE = "network_zone"
    APPLICATION = "application"
    DATA_STORE = "data_store"
    OPERATIONAL_ASSET = "operational_asset"


class RelationshipType(StrEnum):
    MEMBER_OF = "MEMBER_OF"
    CAN_AUTHENTICATE_TO = "CAN_AUTHENTICATE_TO"
    CAN_CONNECT_TO = "CAN_CONNECT_TO"
    CAN_ROUTE_TO = "CAN_ROUTE_TO"
    CAN_ASSUME = "CAN_ASSUME"
    CAN_READ = "CAN_READ"
    CAN_WRITE = "CAN_WRITE"
    MANAGES = "MANAGES"
    HOSTS = "HOSTS"
    TRUSTS = "TRUSTS"
    DEPENDS_ON = "DEPENDS_ON"
    CONTAINS = "CONTAINS"
    PROTECTS = "PROTECTS"
    REFERENCES = "REFERENCES"


class SourceType(StrEnum):
    SYNTHETIC_FIXTURE = "synthetic_fixture"
    AUTHORIZED_EXPORT = "authorized_export"
    CONFIGURATION_FILE = "configuration_file"
    READ_ONLY_API = "read_only_api"
    MANUAL_RECORD = "manual_record"


class Criticality(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Sensitivity(StrEnum):
    UNKNOWN = "unknown"
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class Effect(StrEnum):
    ALLOW = "allow"
    DENY = "deny"


class Completeness(StrEnum):
    UNKNOWN = "unknown"
    COMPLETE = "complete"
    PARTIAL = "partial"
    FAILED = "failed"


class ObservationState(StrEnum):
    UNKNOWN = "unknown"
    OBSERVED = "observed"
    ABSENT = "absent"


class SanitizationState(StrEnum):
    UNKNOWN = "unknown"
    SYNTHETIC = "synthetic"
    SANITIZED = "sanitized"
