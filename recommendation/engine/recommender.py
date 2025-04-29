import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import numpy as np
from app.recommendation.engine.utils import build_user_item_matrix

class Recommender:
    def __init__(self, interactions_df: pd.DataFrame):
        """
        interactions_df must have: user_id, product_id, rating
        """
        self.user_item_matrix = build_user_item_matrix(interactions_df)
        self.similarity_matrix = cosine_similarity(self.user_item_matrix.fillna(0))

    def recommend_products(self, user_index: int, top_n: int = 5) -> list:
        """
        Given a user index (row number, not user_id), return top-N product indices.
        """
        user_similarity_scores = self.similarity_matrix[user_index]
        most_similar_users = np.argsort(user_similarity_scores)[::-1][1:]  # Skip self

        recommended_products = set()
        for similar_user_idx in most_similar_users:
            # Get top items for similar user
            similar_user_ratings = self.user_item_matrix.iloc[similar_user_idx]
            top_items = similar_user_ratings[similar_user_ratings.notnull()].sort_values(ascending=False).index.tolist()

            recommended_products.update(top_items)

            if len(recommended_products) >= top_n:
                break

        return list(recommended_products)[:top_n]

