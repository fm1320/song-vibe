import pandas as pd
import faiss
import numpy as np
from song_vibe.ui.utils import load_data, load_model, load_index


def suggest(song_desc: str = ""):
    df = load_data()
    encoder = load_model()
    index = load_index()
    search_vector = encoder.encode(song_desc)
    _vector = np.array([search_vector])
    faiss.normalize_L2(_vector)

    k = index.ntotal
    distances, ann = index.search(_vector, k=k)

    results = pd.DataFrame({"distances": distances[0], "ann": ann[0]})
    results = results.head(10)
    merge = pd.merge(results, df, left_on="ann", right_index=True)
    res_dict = {"results": list(merge.to_dict()["category"].values())}
    return res_dict
