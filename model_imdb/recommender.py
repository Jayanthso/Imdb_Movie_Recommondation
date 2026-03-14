import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from model_imdb.preprocess import clean_text


class MovieRecommender:

    def __init__(self, path="data/imdb_2024_all.csv"):
        self.df = pd.read_csv(path)
        self.prepare()

    def prepare(self):
        self.df["clean"] = self.df["Storyline"].fillna("").apply(clean_text)

        self.vectorizer = TfidfVectorizer(max_features=50000)
        self.matrix = self.vectorizer.fit_transform(self.df["clean"])

    def recommend(self, user_input, top_k=5):
        user_clean = clean_text(user_input)
        user_vec = self.vectorizer.transform([user_clean])

        similarity = cosine_similarity(user_vec, self.matrix)[0]

        top_idx = similarity.argsort()[-top_k:][::-1]

        results = self.df.iloc[top_idx][["Movie_Name", "Storyline"]]
        return results