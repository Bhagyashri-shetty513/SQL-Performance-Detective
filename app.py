
import streamlit as st

st.set_page_config(
    page_title="SQL Performance Detective",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("🔍 SQL Performance Detective")
st.caption("Oracle DBA Toolkit | Investigate. Compare. Optimize.")

st.markdown("""
Welcome to your SQL performance investigation workspace.

Use the sidebar to navigate between the modules.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tools", "3")
    st.caption("Performance, execution plans, and reports")

with col2:
    st.metric("Database Mode", "Demo")
    st.caption("No live Oracle connection required")

with col3:
    st.metric("Purpose", "SQL Analysis")
    st.caption("Compare metrics and document findings")

st.subheader("Your Workspace")

st.markdown("""
- **Performance Comparison:** Compare elapsed time, CPU time,
  buffer gets, and disk reads.
- **Execution Plan Explorer:** Inspect plan operations and their hierarchy.
- **Tuning Reports:** Record investigation details and export CSV reports.
""")

st.info(
    "Start with sample values, then use measurements from controlled "
    "tests. Always validate tuning changes before applying them to production."
)

st.divider()

st.caption(
    "SQL Performance Detective | Personal Oracle DBA learning project"
)
