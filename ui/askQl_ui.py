# askql_ui.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from ui.connections2 import connect_to_db_and_list, connect_to_selected_db
from cli.agents.sql_agent import create_sql_agent_executor

# Initialize session state
if 'db_type' not in st.session_state:
    st.session_state.db_type = None
if 'db_list' not in st.session_state:
    st.session_state.db_list = []
if 'selected_db' not in st.session_state:
    st.session_state.selected_db = None
if 'db' not in st.session_state:
    st.session_state.db = None
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="AskQL - SQL Insight Agent", layout="wide")
st.title("🧠 AskQL: Natural Language to SQL Interface")

# Sidebar: DB type selection
st.sidebar.header("🔌 Database Selector")
st.session_state.db_type = st.sidebar.selectbox("Choose Database Type", ["mysql", "sqlite"])

# Fetch database list
if st.sidebar.button("List Databases"):
    try:
        st.session_state.db_list = connect_to_db_and_list(st.session_state.db_type)
        st.sidebar.success("Databases loaded!")
    except Exception as e:
        st.sidebar.error(f"Error fetching databases: {e}")

# Show DB list dropdown
if st.session_state.db_list:
    st.session_state.selected_db = st.sidebar.selectbox("Select a Database", st.session_state.db_list)

# Connect to selected DB and create agent
if st.sidebar.button("Connect to Selected DB") and st.session_state.selected_db:
    try:
        st.session_state.db = connect_to_selected_db(st.session_state.db_type, st.session_state.selected_db)
        st.session_state.agent = create_sql_agent_executor(st.session_state.db)
        st.sidebar.success(f"Connected to {st.session_state.selected_db} and agent ready!")
    except Exception as e:
        st.sidebar.error(f"Connection failed: {e}")

# Input area for querying
if st.session_state.agent:
    question = st.text_area("Ask a question about your data:", "What are the top 5 customers by revenue?")
    if st.button("Ask"):
        try:
            question = question + " with no limit."
            result = st.session_state.agent.run(question)
            st.session_state.history.append((question, result))
            st.success("✅ Query executed successfully!")
            st.markdown("### 🤖 Agent's Response")
            st.markdown(f"**Question:** {question}")
            st.markdown("**Answer:**")
            st.write(result)
        except Exception as e:
            st.error(f"❌ Failed to run query: {e}")

# History panel
with st.expander("📜 Query History", expanded=False):
    for idx, (q, r) in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"**{idx}.** *{q}*\n\n{r}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + LangChain + OpenAI")
