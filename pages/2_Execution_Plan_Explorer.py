
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Execution Plan Explorer")
st.caption("Inspect sample Oracle execution plans.")

plan = pd.DataFrame([
    {"Id": 0, "Parent Id": None, "Operation": "SELECT STATEMENT",
     "Object": "-", "Cost": 25},
    {"Id": 1, "Parent Id": 0, "Operation": "NESTED LOOPS",
     "Object": "-", "Cost": 25},
    {"Id": 2, "Parent Id": 1, "Operation": "TABLE ACCESS BY INDEX ROWID",
     "Object": "EMPLOYEES", "Cost": 15},
    {"Id": 3, "Parent Id": 2, "Operation": "INDEX RANGE SCAN",
     "Object": "EMP_DEPT_IX", "Cost": 5},
    {"Id": 4, "Parent Id": 1, "Operation": "TABLE ACCESS FULL",
     "Object": "DEPARTMENTS", "Cost": 10},
])

st.info("Illustrative data only — not a live Oracle execution plan.")

st.subheader("Plan Operations")
st.dataframe(plan, use_container_width=True, hide_index=True)


st.subheader("Automated Plan Insights")

# Identify full table scans
full_scans = plan[
    plan["Operation"].str.contains("TABLE ACCESS FULL", case=False, na=False)
]

# Identify index-related operations
index_ops = plan[
    plan["Operation"].str.contains("INDEX", case=False, na=False)
]

# Find the operation with the highest displayed optimizer cost
highest_cost = plan.loc[plan["Cost"].idxmax()]

col1, col2, col3 = st.columns(3)

col1.metric("Full Table Scans", len(full_scans))
col2.metric("Index Operations", len(index_ops))
col3.metric("Highest Displayed Cost", int(highest_cost["Cost"]))

if not full_scans.empty:
    st.warning(
        "Review full table scans: " +
        ", ".join(full_scans["Object"].astype(str).tolist()) +
        ". Check table size, filters, statistics, and the actual workload "
        "before deciding whether an index would help."
    )
else:
    st.success("No full table scans found in this sample plan.")

if not index_ops.empty:
    st.info(
        "Index-related operations found: " +
        ", ".join(index_ops["Operation"].astype(str).tolist()) +
        ". Confirm whether these operations efficiently support the query."
    )

st.write(
    f"**Highest-cost operation:** {highest_cost['Operation']} "
    f"(Id {int(highest_cost['Id'])}, cost {highest_cost['Cost']})."
)

st.caption(
    "These are preliminary observations based on illustrative data. "
    "Optimizer cost is an estimate, not elapsed time. A full table scan "
    "or a high-cost operation is not necessarily a performance problem."
)


st.subheader("Optimizer Cost by Operation")
fig = px.bar(
    plan,
    x="Operation",
    y="Cost",
    hover_data=["Id", "Object"],
    title="Sample Execution Plan"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Plan Hierarchy")


def show_tree(data, parent=None, depth=0):
    if parent is None:
        children = data[data["Parent Id"].isna()]
    else:
        children = data[data["Parent Id"] == parent]

    for _, row in children.iterrows():
        cols = st.columns([depth + 1, 10])

        with cols[1]:
            st.markdown(
                f"**|-- Id {int(row['Id'])}: {row['Operation']}**  \n"
                f"Object: `{row['Object']}` | Cost: {row['Cost']}"
            )

        show_tree(data, int(row["Id"]), depth + 1)


show_tree(plan)

