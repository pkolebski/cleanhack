import streamlit as st
import numpy as np

from components import home, analysis, user_stance
from data_loading import load_data

# Settings

COMPONENTS = {
    '-': home,
    'Home': home,
    'Analysis': analysis,
    'User stance': user_stance
}

# Data loading

df = load_data()

# Layout start

st.title("Clean energy")

# Menu start

mode = st.sidebar.selectbox("", list(COMPONENTS.keys()))

# Menu end

# components_to_pass = {
#     '-': {'last_rows': last_rows, 'progress_bar': progress_bar, 'chart': chart},
#     'Home': {'last_rows': last_rows, 'progress_bar': progress_bar, 'chart': chart},
#     'Analysis': {},
#     'User stance': {}
# }

# Render components
COMPONENTS[mode]()

st.button("Refresh")

# Layout end
