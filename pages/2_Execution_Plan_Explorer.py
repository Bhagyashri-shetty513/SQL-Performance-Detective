
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
                f"**↳ Id {int(row['Id'])}: {row['Operation']}**  \n"
                f"Object: `{row['Object']}` · Cost: {row['Cost']}"
            )

        show_tree(data, int(row["Id"]), depth + 1)


show_tree(plan)

