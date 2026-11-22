
import streamlit as st
import pandas as pd

from log_parser import parse_log_file
from ai_analyzer import analyze_errors


# Page configuration
st.set_page_config(
    page_title="AI Log Analyzer",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 AI-Powered Application Log Analyzer")
st.write("Analyze application logs using Python and local Ollama AI.")

# Read application log file
try:
    result = parse_log_file("logs/application.log")

    entries = result["entries"]
    counts = result["counts"]
    errors = result["error_messages"]
    invalid = result["invalid_lines"]

except Exception as e:
    st.error(f"Unable to read log file: {e}")
    st.stop()


# Summary metrics
st.subheader("Application Log Summary")

count_map = dict(zip(counts["level"], counts["count"]))

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Logs", len(entries))
col2.metric("Errors", int(count_map.get("ERROR", 0)))
col3.metric("Critical", int(count_map.get("CRITICAL", 0)))
col4.metric("Warnings", int(count_map.get("WARNING", 0)))


# Log distribution chart
st.subheader("Log Level Distribution")

st.bar_chart(counts.set_index("level")["count"])


# Application log table
st.subheader("All Application Logs")
st.dataframe(entries, use_container_width=True)


# Error messages
st.subheader("Errors and Critical Events")

if errors.empty:
    st.success("No errors found.")
else:
    st.dataframe(errors, use_container_width=True)


# Invalid logs
st.subheader("Invalid Log Entries")

if invalid.empty:
    st.success("No invalid log entries found.")
else:
    st.dataframe(invalid, use_container_width=True)


# AI analysis
st.subheader("🤖 AI Root Cause Analysis")

if st.button("Run AI Analysis", type="primary"):

    if errors.empty:
        st.info("No errors available for AI analysis.")

    else:
        with st.spinner("Ollama AI is analyzing your logs..."):

            analysis = analyze_errors(errors)

        st.session_state["analysis"] = analysis

if "analysis" in st.session_state:
    st.markdown(st.session_state["analysis"])


st.caption("Powered by Python, Pandas, Streamlit and Ollama")
