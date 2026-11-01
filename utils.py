
import streamlit as st


def apply_theme():
    """Apply the shared colorful visual system to every Streamlit page."""
    st.markdown("""
    <style>
      :root { --ink:#18233f; --muted:#62708c; --violet:#6c4cf1; --cyan:#12b8c7;
              --coral:#ff7168; --gold:#ffbd4a; --surface:#ffffff; }
      .stApp { background: linear-gradient(135deg,#f4f3ff 0%,#f5fbff 48%,#fff8f1 100%); color:var(--ink); }
      [data-testid="stHeader"] { background:rgba(244,243,255,.78); }
      .block-container { padding-top:2.2rem; padding-bottom:2.5rem; max-width:1440px; }
      h1 { color:#25224a; letter-spacing:-.045em; font-weight:800 !important; }
      h2,h3 { color:#302d59; letter-spacing:-.025em; }
      [data-testid="stCaptionContainer"] { color:var(--muted); }
      [data-testid="stMetric"] { background:linear-gradient(145deg,#fff,#f7f5ff); border:1px solid #e7e2ff;
        border-radius:18px; padding:18px 20px; box-shadow:0 8px 24px rgba(55,48,120,.07); }
      [data-testid="stMetricLabel"] p { color:#66708b; font-weight:650; }
      [data-testid="stMetricValue"] { color:#302d59; font-weight:800; }
      [data-testid="stVerticalBlockBorderWrapper"] { border-radius:18px; }
      [data-testid="stAlert"] { border-radius:14px; }
      .stButton button, .stDownloadButton button, [data-testid="stFormSubmitButton"] button {
        border:0; border-radius:11px; color:white; font-weight:700;
        background:linear-gradient(100deg,#6c4cf1,#9b56dc); box-shadow:0 6px 16px #6c4cf133; }
      .stButton button:hover, .stDownloadButton button:hover { color:white; border:0; filter:brightness(1.07); }
      [data-baseweb="input"]>div, [data-baseweb="select"]>div, [data-testid="stTextArea"] textarea {
        border-radius:10px; background:#fff; }
      [data-testid="stSidebar"] { background:linear-gradient(180deg,#26234f,#38306f 58%,#42408a); }
      [data-testid="stSidebar"] * { color:#f5f3ff; }
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#d9d5ff; }
      [data-testid="stDataFrame"] { border:1px solid #e4e5f5; border-radius:14px; overflow:hidden; }
      hr { border-color:#dddaf4; }
    </style>
    """, unsafe_allow_html=True)


def detective_guide(message, tip, avatar="🕵️"):
    """Show a friendly, illustrated guide with a practical page-specific tip."""
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;margin:8px 0 22px;padding:16px 20px;
      background:linear-gradient(105deg,#fff 0%,#f2f0ff 55%,#e9fbfc 100%);
      border:1px solid #e4e0ff;border-radius:18px;box-shadow:0 7px 22px #39337612">
      <div style="min-width:54px;height:54px;border-radius:18px;display:grid;place-items:center;
        background:linear-gradient(145deg,#7457f5,#27bfd0);font-size:30px;box-shadow:0 6px 14px #6c4cf133">{avatar}</div>
      <div><div style="font-size:15px;font-weight:800;color:#302d59">Detective's note</div>
        <div style="color:#465273;margin-top:3px">{message}</div>
        <div style="font-size:13px;color:#74809a;margin-top:5px">💡 {tip}</div></div>
    </div>
    """, unsafe_allow_html=True)


def calculate_change(before, after):
    if before == 0:
        return None
    return ((before - after) / before) * 100



def compare_execution_plans(plans):
    """Compare execution plans using elapsed time and workload metrics."""
    if not plans:
        return None

    best_plan = min(
        plans,
        key=lambda plan: plan["elapsed_seconds"]
    )

    worst_plan = max(
        plans,
        key=lambda plan: plan["elapsed_seconds"]
    )

    fastest_time = best_plan["elapsed_seconds"]
    slowest_time = worst_plan["elapsed_seconds"]

    if slowest_time <= 0:
        improvement_percent = 0.0
    else:
        improvement_percent = (
            (slowest_time - fastest_time) / slowest_time
        ) * 100

    return {
        "best_plan_hash": best_plan["plan_hash_value"],
        "worst_plan_hash": worst_plan["plan_hash_value"],
        "fastest_time": fastest_time,
        "slowest_time": slowest_time,
        "improvement_percent": improvement_percent,
        "best_cpu_seconds": best_plan.get("cpu_seconds"),
        "best_buffer_gets": best_plan.get("buffer_gets"),
        "best_disk_reads": best_plan.get("disk_reads"),
        "best_executions": best_plan.get("executions"),
    }
