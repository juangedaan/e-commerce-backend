import pandas as pd

def build_user_item_matrix(interactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a pivot table: rows are users, columns are products, values are ratings.
    """
    return interactions_df.pivot_table(index='user_id', columns='product_id', values='rating')


def normalize_interactions(interactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the ratings between 0 and 1 (optional pre-processing).
    """
    df = interactions_df.copy()
    df['rating'] = df['rating'] / df['rating'].max()
    return df

