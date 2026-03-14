import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
print("CWD:", os.getcwd())

import streamlit as st
from model_imdb.recommender import MovieRecommender

st.set_page_config(page_title="IMDB Movie Recommender", layout="wide")

st.title("🎬 IMDB Movie Recommendation System")

st.write("Enter a movie storyline and get similar movie suggestions.")

recommender = MovieRecommender()

user_input = st.text_area("Enter Storyline")

if st.button("Recommend"):
    if user_input.strip() == "":
        st.warning("Please enter a storyline.")
    else:
        results = recommender.recommend(user_input)

        st.subheader("Top Recommendations")

        for i, row in results.iterrows():
            st.markdown(f"### {row['Movie_Name']}")
            st.write(row["Storyline"])
            st.markdown("---")
