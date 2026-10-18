
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 SQL Performance Comparison")
st.caption("Compare Oracle SQL metrics before and after tuning.")

st.info("Demo mode: default values are illustrative sample data.")

before_col, after_col = st.columns(2)

with before_col:
    st.subheader("Before Tuning")
    before_elapsed = st.number_input(
        "Elapsed time (seconds)", min_value=0.0,
        value=8.4, step=0.1, key="before_elapsed"
    )
    before_cpu = st.number_input(
        "CPU time (seconds)", min_value=0.0,
        value=6.2, step=0.1, key="before_cpu"
    )
    before_gets = st.number_input(
        "Buffer gets", min_value=0,
        value=125000, step=1000, key="before_gets"
    )
    before_reads = st.number_input(
        "Disk reads", min_value=0,
        value=18000, step=100, key="before_reads"
    )

with after_col:
    st.subheader("After Tuning")
    after_elapsed = st.number_input(
        "Elapsed time (seconds)", min_value=0.0,
        value=1.6, step=0.1, key="after_elapsed"
    )
    after_cpu = st.number_input(
        "CPU time (seconds)", min_value=0.0,
        value=1.1, step=0.1, key="after_cpu"
    )
    after_gets = st.number_input(
        "Buffer gets", min_value=0,
        value=21000, step=1000, key="after_gets"
    )
    after_reads = st.number_input(
        "Disk reads", min_value=0,
        value=3200, step=100, key="after_reads"
    )

st.divider()
st.subheader("Performance Results")


def calculate_change(before, after):
    if before == 0:
        return None
    return ((before - after) / before) * 100


metrics = [
    ("Elapsed Time (seconds)", before_elapsed, after_elapsed),
    ("CPU Time (seconds)", before_cpu, after_cpu),
    ("Buffer Gets", before_gets, after_gets),
    ("Disk Reads", before_reads, after_reads),
]

cols = st.columns(4)

for col, (name, before, after) in zip(cols, metrics):
    change = calculate_change(before, after)
    delta = f"{change:.1f}%" if change is not None else None

    with col:
        st.metric(
            label=name,
            value=f"{after:,.1f}" if isinstance(after, float)
            else f"{after:,}",
            delta=delta,
            delta_color="normal" if change is not None else "off"
        )

comparison = pd.DataFrame([
    {"Metric": name, "Before": before, "After": after}
    for name, before, after in metrics
])

st.divider()
st.subheader("Metric Comparison")

selected_metric = st.selectbox(
    "Choose a metric to visualize",
    comparison["Metric"]
)

row = comparison[comparison["Metric"] == selected_metric].iloc[0]

chart_data = pd.DataFrame({
    "Stage": ["Before Tuning", "After Tuning"],
    "Value": [row["Before"], row["After"]]
})

fig = px.bar(
    chart_data,
    x="Stage",
    y="Value",
    text="Value",
    color="Stage",
    title=selected_metric
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "A percentage decrease is not proof of successful tuning. "
    "Compare equivalent workloads and validate execution statistics."
)
