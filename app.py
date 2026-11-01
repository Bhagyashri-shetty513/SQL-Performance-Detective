
import streamlit as st
from utils import apply_theme, detective_guide

st.set_page_config(
    page_title="SQL Performance Detective",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

st.title("🔍 SQL Performance Detective")
st.caption("Oracle DBA Toolkit | Investigate. Compare. Optimize.")

st.markdown("### Pick your investigation partner")
partner = st.radio(
    "Choose a guide",
    ["🕵️ Nova · Performance", "🤖 Byte · Execution plans", "🦉 Sage · Tuning notes"],
    horizontal=True,
    label_visibility="collapsed",
    key="detective_partner",
)
partner_notes = {
    "🕵️ Nova · Performance": ("Let’s compare the before and after numbers and look for a clear signal.", "Use equivalent workloads for both measurements.", "🕵️"),
    "🤖 Byte · Execution plans": ("I can help you trace how Oracle reaches the rows it needs.", "Optimizer cost is an estimate; check actual execution statistics too.", "🤖"),
    "🦉 Sage · Tuning notes": ("I’ll help you turn an investigation into a useful record.", "Capture what changed and how you validated the result.", "🦉"),
}
message, tip, avatar = partner_notes[partner]
detective_guide(message, tip, avatar)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Investigation tools", "4")
    st.caption("Compare, explore, report, and search")

with col2:
    st.metric("Database Mode", "Demo")
    st.caption("No live Oracle connection required")

with col3:
    st.metric("Purpose", "SQL Analysis")
    st.caption("Compare metrics and document findings")

st.subheader("Choose a mission")
mission = st.selectbox("What would you like to investigate?", [
    "Compare before and after metrics", "Explore an execution plan",
    "Search a sample SQL ID", "Create a tuning report"
], label_visibility="collapsed")
mission_tips = {
    "Compare before and after metrics": "Open Performance Comparison to adjust measurements and see the chart update.",
    "Explore an execution plan": "Open Execution Plan Explorer to inspect sample operations, cost, and hierarchy.",
    "Search a sample SQL ID": "Open SQL ID Search and try 4abc123xyz789 or 7def456uvw123.",
    "Create a tuning report": "Open Tuning Reports to add your notes and download a CSV.",
}
st.markdown(f"<div style='padding:16px 18px;border-radius:14px;background:#fff;border-left:5px solid #12b8c7;color:#394562'>{mission_tips[mission]}</div>", unsafe_allow_html=True)

with st.expander("What can I do in this workspace?"):
    st.markdown("**Performance Comparison** — compare elapsed time, CPU, buffer gets, and disk reads.\n\n**Execution Plan Explorer** — inspect sample plan operations and hierarchy.\n\n**SQL ID Search** — explore fictional sample SQL and compare plans.\n\n**Tuning Reports** — document an investigation and export it to CSV.")

st.info(
    "Start with sample values, then use measurements from controlled "
    "tests. Always validate tuning changes before applying them to production."
)

st.divider()

st.caption(
    "SQL Performance Detective | Personal Oracle DBA learning project"
)
