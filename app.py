import streamlit as st
from model import run_pipeline, THRESHOLD, EVENT_WINDOW

st.set_page_config(page_title="Forecast Engine", layout="wide")
st.title("Modern Mercantilism Forecast Engine")

# Scenario presets
SCENARIOS = {
    "Competitive Coexistence": {'driver_1': -0.5, 'driver_2': 0.5, 'driver_3': 0.5, 'driver_4': 0.5},
    "Separate Silos": {'driver_1': -1.0, 'driver_2': 1.5, 'driver_3': 1.5, 'driver_4': 1.5},
    "Renaissance of Democracies": {'driver_1': -0.5, 'driver_2': -0.5, 'driver_3': -1.0, 'driver_4': -0.5},
}

# Sidebar controls
forecast_key = st.sidebar.selectbox("Select Forecast", list(THRESHOLD.keys()))
scenario = st.sidebar.selectbox("Choose Scenario", list(SCENARIOS.keys()) + ["Custom"])

if scenario == "Custom":
    targets = {f: st.sidebar.slider(f"{f} (z-shift)", -2.0, 2.0, 0.0, step=0.1) for f in SCENARIOS['Competitive Coexistence']}
else:
    targets = SCENARIOS[scenario]

if st.sidebar.button("Run Forecast"):
    prob, sims, effects = run_pipeline(forecast_key, targets)
    st.subheader(f"Probability Exceeds Threshold ({EVENT_WINDOW[forecast_key]}): {prob:.1%}")
    st.line_chart(effects[['baseline_level', 'adjusted_level']])
    st.dataframe(effects.loc[effects.index >= effects.index.max() - 10])
  
