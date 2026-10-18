
import streamlit as st
import pandas as pd
import plotly.express as px

from sample_sql_data import find_sql
from utils import compare_execution_plans

st.title("SQL ID Search")
st.caption(
    "Search simulated Oracle SQL data and compare execution plans. "
    "Live database connection is not enabled."
)

st.warning(
    "DEMO MODE: All SQL text, plan hashes, and performance metrics "
    "on this page are fictional sample data."
)

sql_id = st.text_input(
    "Enter SQL ID",
    placeholder="Example: 4abc123xyz789"
).strip().lower()

if st.button("Search SQL ID", type="primary"):
    st.session_state["searched_sql_id"] = sql_id

searched_id = st.session_state.get("searched_sql_id", "")

if searched_id:
    result = find_sql(searched_id)

    if result is None:
        st.error(
            "SQL ID not found in the sample dataset. "
            "Try 4abc123xyz789 or 7def456uvw123."
        )
    else:
        st.subheader("SQL Details")
        st.write(f"**SQL ID:** `{result['sql_id']}`")
        st.code(result["sql_text"], language="sql")

        plans = pd.DataFrame(result["plans"])

        st.subheader("Available Sample Plans")

        display_plans = plans.rename(columns={
            "plan_hash_value": "Plan Hash Value",
            "operation": "Example Operation",
            "elapsed_seconds": "Elapsed Seconds",
            "cpu_seconds": "CPU Seconds",
            "buffer_gets": "Buffer Gets",
            "disk_reads": "Disk Reads",
            "executions": "Executions",
        })

        st.dataframe(
            display_plans,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Elapsed Time by Plan")

        fig = px.bar(
            plans,
            x=plans["plan_hash_value"].astype(str),
            y="elapsed_seconds",
            labels={
                "x": "Plan Hash Value",
                "elapsed_seconds": "Elapsed Time (seconds)",
            },
            title="Simulated Plan Comparison",
        )

        st.plotly_chart(fig, use_container_width=True)

        
        comparison = compare_execution_plans(result["plans"])

        if comparison is not None and len(plans) >= 2:
            st.subheader("Comparison Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Faster Sample Plan",
                comparison["best_plan_hash"]
            )
            col2.metric(
                "Elapsed Time",
                f'{comparison["fastest_time"]:.2f} sec'
            )
            col3.metric(
                "Difference",
                f'{comparison["improvement_percent"]:.1f}%',
                help=(
                    "Percentage difference relative to the slower "
                    "sample plan's elapsed time."
                ),
            )

            st.info(
                "The faster sample plan has lower elapsed time. "
                "This does not prove it will perform better in a real database. "
                "Actual workload and execution statistics must be examined."
            )
        else:
            st.info(
                "Only one sample plan is available for this SQL ID, "
                "so there is no second plan to compare."
            )

