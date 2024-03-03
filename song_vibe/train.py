import pandas as pd
import sys
import faiss
from sentence_transformers import SentenceTransformer
from utils import load_data

encoder = SentenceTransformer("paraphrase-mpnet-base-v2")


def train(data_folder: str = "data"):
    load_data(data_folder)
    text = df["text"]
    vectors = encoder.encode(text, show_progress_bar=True)

    vector_dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(vector_dimension)
    faiss.normalize_L2(vectors)
    index.add(vectors)
    faiss.write_index(index, f"{data_folder}/index.bin")
    sys.exit(0)


if __name__ == "__main__":
    data_folder = sys.argv[1]
    train(data_folder=data_folder)
