import glob
import time
import numpy as np
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

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
    charts = get_plots()
    st.plotly_chart(charts[1])
    st.plotly_chart(charts[2])
    st.plotly_chart(charts[3])
    st.dataframe(charts[0])


def tweets_for():
    st.title("Tweets for")
    load_tweets(FOLDER_FOR)


def tweets_against():
    st.title("Tweets against")
    load_tweets(FOLDER_AGAINST)


def tweets_neutral():
    st.title("Tweets neutral")
    load_tweets(FOLDER_NEUTRAL)


def get_plots():
    example_data = pd.read_csv('/home/mateusz/PycharmProjects/cleanhack/data/processed_tweets.csv')
    example_data.mentioned_locations[~ example_data.mentioned_locations.isnull()] = example_data.mentioned_locations[~ example_data.mentioned_locations.isnull()].apply(lambda x: x.split(', '))
    example_data.mentioned_organizations[~ example_data.mentioned_organizations.isnull()] = example_data.mentioned_organizations[~ example_data.mentioned_organizations.isnull()].apply(lambda x: x.split(', '))
    example_data.mentioned_organizations = example_data.mentioned_organizations.apply(lambda d: d if isinstance(d, list) else [])
    example_data.mentioned_locations = example_data.mentioned_locations.apply(lambda d: d if isinstance(d, list) else [])

    rename_dict = {
        'id': 'tweet_id', 'user_followers_count': 'user_followers', 'text': 'tweet_text',
        'created_at': 'timestamp', 'retweet_count': 'retweets_num', 'favorite_count': 'likes_num',
        'user_friends_count': 'user_friends_num',
        'user_favourites_count': 'user_favourites_num', 'user_statuses_count': 'user_statuses_num'
    }

    example_data = example_data.rename(columns=rename_dict)

    user_popularity = example_data.groupby(['user_name']).mean()[['user_followers']].reset_index()
    user_popularity = user_popularity.rename(
        columns={'user_name': 'User name', 'user_followers': 'Number of Followers'})

    user_topics = example_data.groupby(['user_name']).mean()[
        ['topic_energy', 'topic_clean_energy', 'topic_photovoltaics',
         'topic_gas', 'topic_nuclear', 'topic_coal', 'topic_other']].reset_index()

    user_topics = user_topics.rename(columns={'user_name': 'User name', 'topic_energy': 'energy',
                                              'topic_clean_energy': 'clean energy',
                                              'topic_photovoltaics': 'photovoltaics',
                                              'topic_gas': 'gas', 'topic_coal': 'coal',
                                              'topic_other': 'other'})

    user_emotions = example_data.groupby(['user_name', 'emotion']).sum()['tweet_id'].reset_index()
    user_emotions = user_emotions.rename(
        columns={"tweet_id": "Number of tweets", 'user_name': 'User name', 'emotion': 'Emotion'})

    user_mentions_org_loc = example_data.groupby(['user_name'])[
        'mentioned_organizations', 'mentioned_locations'].sum().reset_index()

    def to_flat_list(l):
        result = []
        for e in l:
            l = [w for w in e.split("'") if w not in ['[', ']', '', '[]']]
            result.extend(l)

        result = {e for e in result if not e.startswith('@')}
        return result

    user_mentions_org_loc.mentioned_organizations = user_mentions_org_loc.mentioned_organizations.apply(
        to_flat_list)
    user_mentions_org_loc.mentioned_locations = user_mentions_org_loc.mentioned_locations.apply(
        to_flat_list)

    # user_mentions_org_loc
    #
    # user_mentions_org_loc = example_data.groupby(['user_name'])[
    #     'mentioned_organizations', 'mentioned_locations'].sum().reset_index()

    user_sentiments = example_data.groupby(['user_name', 'sentiment']).count()[
        'tweet_id'].reset_index()
    user_sentiments = user_sentiments.rename(
        columns={"tweet_id": "Number of tweets", 'user_name': 'User name',
                 'sentiment': 'Sentiment'})

    fig0 = px.bar(user_sentiments, x="User name", y="Number of tweets",
                 color="Sentiment", title="Number of users' tweets and sentiments", height=700)

    fig1 = px.bar(user_popularity, x="User name", y=['Number of Followers'],
                 title="Users' connections", barmode='group')

    fig2 = px.bar(user_topics, x="User name",
                 y=['energy', 'clean energy', 'photovoltaics', 'gas', 'topic_nuclear', 'coal',
                    'other'],
                 title="Topics of tweets", height=800)

    return user_mentions_org_loc, fig0, fig1, fig2
