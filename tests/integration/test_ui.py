"""Exercise the browser app without starting a network server."""

import io
import json
import socket
from pathlib import Path

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from cyber_security_systems.ingestion.fixtures import (
    MAX_BYTES,
    FixtureError,
    load_fixture,
    load_fixture_bytes,
)
from cyber_security_systems.reporting.reports import render_reports, write_reports

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/industrial/vendor_access.json"


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("UI analysis attempted a network connection")

    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)


def app():
    return AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=15).run()


def test_demo_analysis_downloads_and_input_change(tmp_path):
    page = app()
    page.button[0].click().run()
    assert not page.exception
    assert page.metric[0].value == "1"
    result = page.session_state["result"]
    reports = render_reports(result)
    write_reports(result, tmp_path / "reports")
    assert len(page.get("download_button")) == 3
    for name, content in reports.items():
        assert (tmp_path / "reports" / name).read_text() == content
    page.radio[0].set_value("Upload JSON").run()
    assert not page.exception
    assert not page.metric
    assert page.button[0].disabled


def test_demo_comparison():
    page = app()
    page.radio[1].set_value("Compare before and after").run()
    page.button[0].click().run()
    assert not page.exception
    assert page.metric[0].value == "0"
    assert page.session_state["result"]["comparison_summary"]["resolved"] == 1


@pytest.mark.parametrize("incomplete", [False, True])
def test_uploaded_snapshot(monkeypatch, incomplete):
    raw = json.loads(FIXTURE.read_bytes())
    if incomplete:
        raw["evidence"].clear()
    payload = json.dumps(raw).encode()
    monkeypatch.setattr(st, "file_uploader", lambda *a, **kw: io.BytesIO(payload))
    page = app()
    page.radio[0].set_value("Upload JSON").run()
    page.button[0].click().run()
    assert not page.exception
    assert bool(page.warning) == incomplete
    assert page.metric[0].value == ("0" if incomplete else "1")


def test_invalid_upload_clears_previous_result(monkeypatch):
    payload = b'{"private-marker":'
    monkeypatch.setattr(st, "file_uploader", lambda *a, **kw: io.BytesIO(payload))
    page = app()
    page.button[0].click().run()
    page.radio[0].set_value("Upload JSON").run()
    page.button[0].click().run()
    assert not page.exception
    assert page.error
    assert "private-marker" not in page.error[0].value
    assert not page.metric
    assert not page.get("download_button")


def test_uploaded_comparison_requires_both_files(monkeypatch):
    payloads = {"before": FIXTURE.read_bytes()}

    def upload(*args, **kwargs):
        payload = payloads.get(kwargs["key"])
        return io.BytesIO(payload) if payload is not None else None

    monkeypatch.setattr(st, "file_uploader", upload)
    page = app()
    page.radio[0].set_value("Upload JSON").run()
    page.radio[1].set_value("Compare before and after").run()
    assert page.button[0].disabled
    payloads["after"] = (FIXTURE.parent / "vendor_access_remediated.json").read_bytes()
    page.run()
    page.button[0].click().run()
    assert not page.exception
    assert page.session_state["result"]["comparison_summary"]["resolved"] == 1


@pytest.mark.parametrize(
    "payload",
    [
        b"x" * (MAX_BYTES + 1),
        b'{"a":1,"a":2}',
        b'{"a":NaN}',
        b"\xff",
    ],
)
def test_upload_validation_rejects_invalid_bytes(payload):
    with pytest.raises(FixtureError):
        load_fixture_bytes(payload)


def test_upload_and_file_share_exact_input_hash():
    assert load_fixture_bytes(FIXTURE.read_bytes()) == load_fixture(FIXTURE)
