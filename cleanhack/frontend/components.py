import glob
import time
import numpy as np
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

from component_template.template.my_component import my_component

FOLDER_FOR = '/home/mateusz/PycharmProjects/cleanhack/cleanhack/frontend/images/for/'
FOLDER_AGAINST = '/home/mateusz/PycharmProjects/cleanhack/cleanhack/frontend/images/against/'
FOLDER_NEUTRAL = '/home/mateusz/PycharmProjects/cleanhack/cleanhack/frontend/images/neutral/'
FOLDER_ASSETS = '/home/mateusz/PycharmProjects/cleanhack/cleanhack/frontend/images/assets/'


def get_technologies_plot(data_path):
    images = glob.glob(f"{data_path}*.png")
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(30, 20), dpi=100)
    for index, img in enumerate(images):
        print(index // 4, index % 4)
        image = Image.open(img)
        axs[index // 4, index % 4].axis('off')
        axs[index // 4, index % 4].imshow(image)

    return fig


def load_tweets(folder):
    images = glob.glob(f"{folder}*.png")
    for index, image in enumerate(images):
        image = Image.open(image)
        st.image(image)


def home():
    st.title("Smart&Green.ai")
    st.text('A social media monitoring system.'
            ' that  about'
            ' environmental issues and ')
    st.text('Provides information on the emotional nature of tweets')
    st.text('Perform data analysis and divide users into thematic groups')
    fig = get_technologies_plot(FOLDER_ASSETS)
    st.pyplot(fig)


def analysis():
    st.title("Data analysis")


def tweets_for():
    st.title("Tweets for")
    load_tweets(FOLDER_FOR)


def tweets_against():
    st.title("Tweets against")
    load_tweets(FOLDER_AGAINST)


def tweets_neutral():
    st.title("Tweets neutral")
    load_tweets(FOLDER_NEUTRAL)
