import pandas as pd
import sys
import faiss

data = pd.read_csv('data.csv', sep=';')
data.rename(columns={'Song_name': 'category', 'Response': 'text'}, inplace=True)
# data = data.head(10)
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
def predict():
    import numpy as np
    index = faiss.read_index('index.bin')
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    from fastapi.responses import PlainTextResponse
    import uvicorn

    app = FastAPI()

    @app.get("/robots.txt")
    async def robots():
        return PlainTextResponse("""User-agent: *\nDisallow: /""")

    @app.get("/")
    async def root():
        return HTMLResponse("""<!DOCTYPE html>
 <html>
        <head>
                              <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
            <title>Demo</title>
        </head>
        <body>
            <div class="max-w-2xl mx-auto p-2">
                <h2 class="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl">Get a song suggestion</h2>
                             <p class="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-300">Enter your mood and we will use ML to give you songs you might like</p>
                           <form class="mt-10 max-w-md" id="forma">
      <div class="flex gap-x-4">
        <label for="songv" class="sr-only">Email address</label>
        <input id="songv" name="songv" type="text" class="min-w-0 flex-auto rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" placeholder="Enter song vibes, description...">
        <button type="submit" class="flex-none rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Get songs</button>
      </div>
      <p class="mt-4 text-sm leading-6 text-gray-900 hidden">We care about your data. Read our <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">privacy&nbsp;policy</a>.</p>
    </form>
                            <div id='results'></div>
                        <script>
                            forma.addEventListener('submit', (e) => {
                                e.preventDefault();
                                fetch("/suggest?" + new URLSearchParams({ song_desc: songv.value })).then(response => response.json()).then(data => {
                                    let full = document.createElement('div');
                                    data.results.map(x => {
                                        let m = document.createElement('div');
                                        m.innerText = x;
                                        full.appendChild(m);
                                    })
                                    results.innerHTML = full.innerHTML;
                                });
                            });
                            </script>
       
    
            </div>
        </body>
    </html>
                            """)
    
    @app.get("/suggest")
    async def suggest(song_desc: str = ""):
            search_text = song_desc
            search_vector = encoder.encode(search_text)
            _vector = np.array([search_vector])
            faiss.normalize_L2(_vector)

            k = index.ntotal
            distances, ann = index.search(_vector, k=k)

            results = pd.DataFrame({'distances': distances[0], 'ann': ann[0]})
            results = results.head(10)
            # print(results)
            merge = pd.merge(results, df, left_on='ann', right_index=True)
            return {"results": list(merge.to_dict()['category'].values())}
    uvicorn.run(app, host='0.0.0.0', port=9898)
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        train()
    else:
        predict()