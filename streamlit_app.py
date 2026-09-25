"""Local synthetic demo UI; analysis and report generation stay in the package."""

from pathlib import Path

import streamlit as st

from cyber_security_systems.analysis.engine import analyze, compare
from cyber_security_systems.ingestion.fixtures import (
    MAX_BYTES,
    FixtureError,
    load_fixture,
    load_fixture_bytes,
)
from cyber_security_systems.reporting.reports import render_reports

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "industrial"


def clear_result() -> None:
    st.session_state.pop("result", None)


def show_result(result: dict) -> None:
    status = result.get("comparison_status", result["status"])
    if status == "complete":
        st.success("Analysis complete within the supported synthetic scope.")
    else:
        st.warning("Analysis incomplete. Missing evidence does not establish safety.")
    findings, entities, relationships = st.columns(3)
    findings.metric("Current findings", len(result["findings"]), border=True)
    entities.metric("Entities reviewed", len(result["entities"]), border=True)
    relationships.metric(
        "Relationships reviewed", len(result["relationships"]), border=True
    )
    if "comparison_summary" in result:
        st.subheader("What changed")
        summary = result["comparison_summary"]
        for column, (key, value) in zip(
            st.columns(len(summary)), summary.items(), strict=True
        ):
            column.metric(key.replace("_", " ").capitalize(), value, border=True)
    reports = render_reports(result)
    st.subheader("Download reports")
    for column, (name, content) in zip(st.columns(3), reports.items(), strict=True):
        column.download_button(
            f"Download {name}",
            content,
            file_name=name,
            mime="application/json" if name.endswith(".json") else "text/markdown",
            on_click="ignore",
        )
    report_tab, evidence_tab = st.tabs(
        ["Readable report", "Evidence and findings JSON"]
    )
    with report_tab:
        st.markdown(reports["report.md"])
    with evidence_tab:
        st.json(result)


def main() -> None:
    st.set_page_config(page_title="Industrial access paths", layout="wide")
    st.title("Industrial access paths")
    st.caption("Explore access paths and compare remediation evidence locally.")
    st.info(
        "Synthetic prototype only. Upload supported synthetic inventory JSON, "
        "not customer exports. No live scanning or AWS access is performed."
    )
    with st.container(border=True):
        st.subheader("Set up your analysis")
        input_column, task_column = st.columns(2)
        source = input_column.radio(
            "Input",
            ["Bundled demo", "Upload JSON"],
            on_change=clear_result,
            horizontal=True,
        )
        mode = task_column.radio(
            "Task",
            ["Analyze one snapshot", "Compare before and after"],
            on_change=clear_result,
            horizontal=True,
        )
    comparing = mode == "Compare before and after"
    before = after = None
    if source == "Upload JSON":
        st.caption(
            "Maximum 4 MiB per file. Both comparison files must use matching scope."
        )
        before = st.file_uploader(
            "Before snapshot" if comparing else "Snapshot",
            type=["json"],
            key="before",
            max_upload_size=4,
            on_change=clear_result,
        )
        if comparing:
            after = st.file_uploader(
                "After snapshot",
                type=["json"],
                key="after",
                max_upload_size=4,
                on_change=clear_result,
            )
    else:
        st.caption(
            "The demo starts with a vendor access path. The after snapshot "
            "contains evidence that VPN group membership was removed."
        )
    ready = source == "Bundled demo" or (
        before is not None and (not comparing or after is not None)
    )
    if st.button("Run analysis", type="primary", disabled=not ready):
        clear_result()
        try:
            with st.spinner("Checking evidence and access paths…"):
                if source == "Bundled demo":
                    baseline = load_fixture(FIXTURES / "vendor_access.json")
                    current = (
                        load_fixture(FIXTURES / "vendor_access_remediated.json")
                        if comparing
                        else None
                    )
                else:
                    baseline = load_fixture_bytes(
                        before.getbuffer()[: MAX_BYTES + 1].tobytes()
                    )
                    current = (
                        load_fixture_bytes(after.getbuffer()[: MAX_BYTES + 1].tobytes())
                        if comparing
                        else None
                    )
                st.session_state["result"] = (
                    compare(baseline, current) if comparing else analyze(baseline)
                )
        except FixtureError as error:
            st.error("Invalid fixture: " + str(error))
    if "result" in st.session_state:
        st.divider()
        st.subheader("Analysis results")
        show_result(st.session_state["result"])


if __name__ == "__main__":
    main()
