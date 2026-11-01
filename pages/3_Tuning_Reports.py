
import streamlit as st
from utils import apply_theme, detective_guide
import pandas as pd
from datetime import date
from report_store import load_reports, save_report

st.title("📄 SQL Tuning Reports")
apply_theme()
st.caption("Document and export your Oracle SQL tuning investigations.")
detective_guide("A few clear notes make this report useful to your future self.", "Include the test conditions and how you checked the result.", "🦉")

st.info("Enter your own measurements. The report does not connect to Oracle.")

with st.form("tuning_report_form"):
    query_name = st.text_input(
        "Query name",
        placeholder="Example: Orders by customer"
    )

    sql_id = st.text_input(
        "Oracle SQL ID (optional)",
        placeholder="Example: 4abc123xyz"
    )

    investigation_date = st.date_input(
        "Investigation date",
        value=date.today()
    )

    st.subheader("Before Tuning")
    before_elapsed = st.number_input(
        "Elapsed time (seconds)",
        min_value=0.0, value=8.4, step=0.1
    )
    before_gets = st.number_input(
        "Buffer gets",
        min_value=0, value=125000, step=1000
    )
    before_reads = st.number_input(
        "Disk reads",
        min_value=0, value=18000, step=100
    )

    st.subheader("After Tuning")
    after_elapsed = st.number_input(
        "Elapsed time (seconds)",
        min_value=0.0, value=1.6, step=0.1
    )
    after_gets = st.number_input(
        "Buffer gets",
        min_value=0, value=21000, step=1000
    )
    after_reads = st.number_input(
        "Disk reads",
        min_value=0, value=3200, step=100
    )

    notes = st.text_area(
        "DBA investigation notes",
        placeholder=(
            "What did you investigate? What changed? "
            "How did you validate the results?"
        )
    )

    submitted = st.form_submit_button("Generate Report")

if submitted:
    def improvement(before, after):
        if before == 0:
            return None
        return round((before - after) / before * 100, 2)

    report = pd.DataFrame([
        {
            "Query Name": query_name or "Unnamed query",
            "SQL ID": sql_id,
            "Investigation Date": investigation_date.isoformat(),
            "Metric": "Elapsed Time (seconds)",
            "Before": before_elapsed,
            "After": after_elapsed,
            "Change (%)": improvement(before_elapsed, after_elapsed),
            "DBA Notes": notes
        },
        {
            "Query Name": query_name or "Unnamed query",
            "SQL ID": sql_id,
            "Investigation Date": investigation_date.isoformat(),
            "Metric": "Buffer Gets",
            "Before": before_gets,
            "After": after_gets,
            "Change (%)": improvement(before_gets, after_gets),
            "DBA Notes": notes
        },
        {
            "Query Name": query_name or "Unnamed query",
            "SQL ID": sql_id,
            "Investigation Date": investigation_date.isoformat(),
            "Metric": "Disk Reads",
            "Before": before_reads,
            "After": after_reads,
            "Change (%)": improvement(before_reads, after_reads),
            "DBA Notes": notes
        }
    ])

    saved_report_id = save_report(report.to_dict(orient="records"))
    st.session_state["latest_tuning_report"] = report.to_dict(orient="records")
    st.session_state["latest_tuning_report_id"] = saved_report_id

if "latest_tuning_report" in st.session_state:
    report = pd.DataFrame(st.session_state["latest_tuning_report"])

    st.subheader("Report Preview")
    st.dataframe(report, use_container_width=True, hide_index=True)

    st.download_button(
        "Download Tuning Report (CSV)",
        data=report.to_csv(index=False).encode("utf-8-sig"),
        file_name="sql_tuning_report.csv",
        mime="text/csv"
    )

    st.success(
        f"Report #{st.session_state['latest_tuning_report_id']} saved on this device and ready to download."
    )

    st.caption(
        "A negative change means the after value increased. "
        "Validate comparisons using equivalent workloads and test conditions."
    )

st.divider()
st.subheader("Saved Report History")
saved_reports = pd.DataFrame(load_reports())
if saved_reports.empty:
    st.caption("Generated reports will appear here and remain available after you restart the app.")
else:
    st.caption(f"{saved_reports['Report #'].nunique()} saved investigation(s) on this device.")
    st.dataframe(saved_reports, use_container_width=True, hide_index=True)
    st.download_button(
        "Download Saved History (CSV)",
        data=saved_reports.to_csv(index=False).encode("utf-8-sig"),
        file_name="sql_tuning_report_history.csv",
        mime="text/csv",
        key="download_report_history",
    )
