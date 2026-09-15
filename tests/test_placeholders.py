from cyber_security_systems.infrastructure.pipeline import pipeline_placeholder
from cyber_security_systems.lambdas.handler import lambda_placeholder


def test_lambda_placeholder_returns_none():
    assert lambda_placeholder({}, None) is None


def test_pipeline_placeholder_returns_none():
    assert pipeline_placeholder("development") is None
