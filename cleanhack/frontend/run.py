import streamlit as st
import numpy as np

from components import home, analysis, tweets_for, tweets_against, tweets_neutral
from data_loading import load_data

# Settings

COMPONENTS = {
    'Home': home,
    'Analysis': analysis,
    'Users For': tweets_for,
    'Users Against': tweets_against,
    'Users Neutral': tweets_neutral
}

# Data loading

df = load_data()

# Layout start

# Menu start

mode = st.sidebar.selectbox("Home", list(COMPONENTS.keys()))

# Menu end

# Render components
COMPONENTS[mode]()

# Layout end
