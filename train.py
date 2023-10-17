import pandas as pd
import sys
import faiss

data = pd.read_csv('data.csv')
data.rename(columns={'Song_name': 'category', 'Response': 'text'}, inplace=True)
df = pd.DataFrame(data, columns = ['text', 'category'])

from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer("paraphrase-mpnet-base-v2")

def train():
    text = df['text']
    vectors = encoder.encode(text, show_progress_bar=True)

    vector_dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(vector_dimension)
    faiss.normalize_L2(vectors)
    index.add(vectors)
    faiss.write_index(index, 'index.bin')
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        train()
