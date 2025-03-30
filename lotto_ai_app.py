
import streamlit as st
import pandas as pd
import io
from combo_generators import generate_basic_combos, generate_smart_combos
from backtest_engine import backtest_combos
from combo_scorer import score_combo

# --- Sidebar ---
st.sidebar.title("🎰 Universal Lotto AI Engine")

# Game Profile Selection
game = st.sidebar.selectbox("Select Game Profile", [
    "Lotto Texas", "Powerball", "Mega Millions", "EuroMillions", "Custom Fantasy League"])

# Upload CSV
data_file = st.sidebar.file_uploader("Upload Draw History (CSV)", type="csv")

# Game Parameters
st.sidebar.markdown("---")
st.sidebar.subheader("Game Parameters")
numbers_per_draw = st.sidebar.number_input("Numbers Per Draw", min_value=1, max_value=10, value=6)
number_range_max = st.sidebar.number_input("Max Number (Range)", min_value=10, max_value=100, value=54)
use_bonus = st.sidebar.checkbox("Include Bonus Ball")
bonus_range_max = st.sidebar.number_input("Max Bonus Number", min_value=1, max_value=50, value=0) if use_bonus else 0

# Module Toggles
st.sidebar.markdown("---")
st.sidebar.subheader("Modules")
modules = {
    "Mood Engine": st.sidebar.checkbox("Mood Engine", value=True),
    "Genetic Evolution": st.sidebar.checkbox("Genetic Evolution", value=True),
    "Entropy + Gap Filter": st.sidebar.checkbox("Entropy + Gap Filter", value=True),
    "Repeat Avoidance": st.sidebar.checkbox("Repeat Avoidance", value=True),
    "AI Voting System": st.sidebar.checkbox("AI Voting System", value=True),
    "Smart Coverage": st.sidebar.checkbox("Smart Coverage", value=True),
    "Permutation Scrambler": st.sidebar.checkbox("Permutation Scrambler", value=True),
    "Backtesting": st.sidebar.checkbox("Backtesting", value=True)
}

# --- Main App Tabs ---
st.title("🔍 Universal Lotto Strategy Engine")
tabs = st.tabs(["Data Overview", "Strategy Engine", "Backtesting", "Export + Save"])

# Tab 1: Data Overview
with tabs[0]:
    st.subheader("📊 Draw Data Overview")
    if data_file:
        try:
            stringio = io.StringIO(data_file.getvalue().decode("utf-8"))
            df = pd.read_csv(stringio)
            if df.empty:
                st.error("The uploaded CSV is empty. Please upload a valid file.")
            else:
                st.dataframe(df.head(10))
                if st.button("Analyze Draw Data"):
                    st.success("Analyzing... 🧠")
                    try:
                        draw_cols = df.select_dtypes(include=['number']).iloc[:, :6]
                        st.write("Number of draws:", len(draw_cols))
                        st.write("Number range:", draw_cols.min().min(), "to", draw_cols.max().max())
                        st.write("Draw sum range:", draw_cols.sum(axis=1).min(), "to", draw_cols.sum(axis=1).max())
                        st.write("Average entropy (approx.):", round(draw_cols.std(axis=1).mean(), 3))
                    except:
                        st.error("Unable to process number columns. Make sure the first 6 columns are numbers.")
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
    else:
        st.warning("Upload a CSV file to begin.")

# Tab 2: Strategy Engine
with tabs[1]:
    st.subheader("🎯 Combo Generator")
    if data_file:
        stringio = io.StringIO(data_file.getvalue().decode("utf-8"))
        df = pd.read_csv(stringio)

        if st.button("🎲 Generate Basic Combos"):
            st.success("Generating basic combos...")
            basic_combos = generate_basic_combos(list(range(1, number_range_max + 1)), numbers_per_draw, total=10)
            for c in basic_combos:
                st.write("🎰", c)
            st.session_state['last_generated_combos'] = basic_combos

        if st.button("🔥 Generate Smart Combos"):
            st.success("Generating hot + entropy combos...")
            smart_df = generate_smart_combos(df, n_picks=numbers_per_draw, total=10)
            st.dataframe(smart_df)
            st.session_state['last_generated_combos'] = smart_df['Combo'].tolist()

            if st.button("📈 Score These Smart Combos"):
                score_results = [score_combo(c, df.iloc[:, 4:10]) for c in smart_df['Combo']]
                score_df = pd.DataFrame(score_results).sort_values(by='Total Score', ascending=False)
                st.dataframe(score_df)
                st.session_state['last_scored_combos'] = score_df
    else:
        st.warning("Upload a CSV file first.")

# Tab 3: Backtesting
with tabs[2]:
    st.subheader("🧪 Historical Combo Tester")
    if data_file and 'last_generated_combos' in st.session_state:
        stringio = io.StringIO(data_file.getvalue().decode("utf-8"))
        df = pd.read_csv(stringio)
        st.info("Using previously generated combos for backtesting.")
        if st.button("📊 Run Backtest"):
            result_df = backtest_combos(st.session_state['last_generated_combos'], df.iloc[:, 4:10])
            st.dataframe(result_df)
    else:
        st.warning("Generate combos and upload draw history to enable backtesting.")

# Tab 4: Export + Save
with tabs[3]:
    st.subheader("💾 Export + Session Save")
    st.markdown("Download combos as CSV. Add session notes. Save your strategy memory.")

# Footer
st.markdown("---")
st.caption("Powered by the Universal Lotto AI Engine ✨")
