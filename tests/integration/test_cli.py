import json
import os
import socket
from pathlib import Path

import pytest

from cyber_security_systems.cli import main
from cyber_security_systems.ingestion.fixtures import (
    MAX_BYTES,
    FixtureError,
    load_fixture,
)

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures" / "industrial"


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("offline prototype attempted a network connection")

    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)


def test_validate_analyze_compare_commands(tmp_path, capsys):
    before = str(FIXTURES / "vendor_access.json")
    after = str(FIXTURES / "vendor_access_remediated.json")
    assert main(["validate", before]) == 0
    assert main(["analyze", before, "--output", str(tmp_path / "analysis")]) == 0
    assert (
        main(["compare", before, after, "--output", str(tmp_path / "comparison")]) == 0
    )
    result = json.loads((tmp_path / "comparison/finding.json").read_text())
    assert result["comparison"][0]["status"] == "resolved"
    report = (tmp_path / "comparison/report.md").read_text()
    assert "resolved" in report
    assert "membership" in report
    assert "not prove compromise" in report
    graph = json.loads((tmp_path / "comparison/graph.json").read_text())
    assert graph["relationships"] == result["relationships"]
    assert set(p.name for p in (tmp_path / "comparison").iterdir()) == {
        "finding.json",
        "report.md",
        "graph.json",
    }
    assert "Invalid" not in capsys.readouterr().err


def test_commands_without_unix_open_flags(tmp_path, monkeypatch, capsys):
    monkeypatch.delattr(os, "O_NONBLOCK", raising=False)
    monkeypatch.delattr(os, "O_NOFOLLOW", raising=False)
    test_validate_analyze_compare_commands(tmp_path, capsys)


def test_symlink_rejected_without_unix_open_flags(tmp_path, monkeypatch):
    link = tmp_path / "input.json"
    link.symlink_to(FIXTURES / "vendor_access.json")
    monkeypatch.delattr(os, "O_NONBLOCK", raising=False)
    monkeypatch.delattr(os, "O_NOFOLLOW", raising=False)
    with pytest.raises(FixtureError):
        load_fixture(link)


def test_input_replaced_during_open_is_rejected(tmp_path, monkeypatch):
    path = tmp_path / "input.json"
    replacement = tmp_path / "replacement.json"
    path.write_bytes((FIXTURES / "vendor_access.json").read_bytes())
    replacement.write_bytes(path.read_bytes())
    original_open = os.open

    def replace_then_open(candidate, flags):
        replacement.replace(path)
        return original_open(candidate, flags)

    monkeypatch.delattr(os, "O_NOFOLLOW", raising=False)
    monkeypatch.setattr(os, "open", replace_then_open)
    with pytest.raises(FixtureError, match="changed while opening"):
        load_fixture(path)


@pytest.mark.parametrize("command", ["analyze", "compare"])
def test_missing_output_parents_are_created(tmp_path, command):
    output = tmp_path / "new" / "nested" / "reports"
    args = [command, str(FIXTURES / "vendor_access.json")]
    if command == "compare":
        args.append(str(FIXTURES / "vendor_access_remediated.json"))
    assert main([*args, "--output", str(output)]) == 0
    assert {path.name for path in output.iterdir()} == {
        "finding.json",
        "graph.json",
        "report.md",
    }
    if os.name != "nt":
        assert output.stat().st_mode & 0o777 == 0o700


def test_output_parent_file_is_preserved(tmp_path, capsys):
    parent = tmp_path / "existing-file"
    parent.write_text("keep existing work")
    assert (
        main(
            [
                "analyze",
                str(FIXTURES / "vendor_access.json"),
                "--output",
                str(parent / "reports"),
            ]
        )
        == 2
    )
    assert parent.read_text() == "keep existing work"
    assert "Cannot write reports" in capsys.readouterr().err


def test_existing_output_is_not_overwritten(tmp_path):
    sentinel = tmp_path / "report.md"
    sentinel.write_text("keep existing work")
    assert (
        main(
            ["analyze", str(FIXTURES / "vendor_access.json"), "--output", str(tmp_path)]
        )
        == 2
    )
    assert sentinel.read_text() == "keep existing work"


@pytest.mark.parametrize(
    "content",
    [
        '{"secret-marker":',
        '{"schema_version":"1.0","schema_version":"1.0"}',
        '{"field":NaN}',
        "[" * 2000,
    ],
)
def test_malformed_input_fails_without_echoing_content(tmp_path, capsys, content):
    path = tmp_path / "input.json"
    path.write_text(content)
    assert main(["validate", str(path)]) == 2
    assert "secret-marker" not in capsys.readouterr().err


def test_large_and_symlink_inputs_rejected(tmp_path):
    large = tmp_path / "large.json"
    with large.open("wb") as stream:
        stream.truncate(MAX_BYTES + 1)
    with pytest.raises(FixtureError):
        load_fixture(large)
    link = tmp_path / "link.json"
    link.symlink_to(FIXTURES / "vendor_access.json")
    with pytest.raises(FixtureError):
        load_fixture(link)


def test_incomplete_input_emits_report_and_nonzero_exit(tmp_path):
    raw = json.loads((FIXTURES / "vendor_access.json").read_text())
    raw["evidence"].clear()
    path = tmp_path / "incomplete.json"
    path.write_text(json.dumps(raw))
    assert main(["validate", str(path)]) == 3
    output = tmp_path / "output"
    assert main(["analyze", str(path), "--output", str(output)]) == 3
    result = json.loads((output / "finding.json").read_text())
    assert result["status"] == "incomplete_analysis"
    assert result["findings"] == []


def test_imported_markup_is_escaped_not_executed(tmp_path):
    import hashlib

    raw = json.loads((FIXTURES / "vendor_access.json").read_text())
    value = '<script>alert("synthetic")</script> [link](https://invalid.example)'
    raw["evidence"][0]["value"] = value
    raw["evidence"][0]["provenance"]["integrity_reference"] = (
        "sha256:" + hashlib.sha256(value.encode()).hexdigest()
    )
    path = tmp_path / "markup.json"
    path.write_text(json.dumps(raw))
    output = tmp_path / "report"
    assert main(["analyze", str(path), "--output", str(output)]) == 0
    rendered = (output / "report.md").read_text()
    assert "<script>" not in rendered
    assert "[link](https://invalid.example)" not in rendered


def test_output_symlink_is_rejected(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "output"
    link.symlink_to(target, target_is_directory=True)
    assert (
        main(["analyze", str(FIXTURES / "vendor_access.json"), "--output", str(link)])
        == 2
    )
    assert list(target.iterdir()) == []
