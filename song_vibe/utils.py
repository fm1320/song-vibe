import pandas as pd
from faiss import read_index
from sentence_transformers import SentenceTransformer


def load_data(folder: str = "data/", file: str = "data.csv") -> pd.DataFrame:
    print("loading data...")
    data = pd.read_csv(f"{folder}/{file}")
    data.rename(columns={"Song_name": "category", "Response": "text"}, inplace=True)
    df = pd.DataFrame(data, columns=["text", "category"])
    return df


def load_model():
    print("loading model...")
    return SentenceTransformer("paraphrase-mpnet-base-v2")


def load_index(folder: str = "data/", file: str = "index.bin"):
    print("loading index...")
    return read_index(f"{folder}/{file}")
