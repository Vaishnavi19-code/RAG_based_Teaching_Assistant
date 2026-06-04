import requests
import os
import json
import pandas as pd
import joblib
# def create_embedding(text):
#     r = requests.post("http://localhost:11434/api/embed", json={                 #ollama local instance port
#         "model": "bge-m3",
#         "prompt": text
#     })

#     embedding = r.json()['embedding']
#     return embedding
import requests

def create_embedding(text):

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text
        }
    )

    response = r.json()
    print(response)
    return response["embeddings"]

jsons = os.listdir("jsons")  # List all the jsons 
my_dicts = []
chunk_id = 0

for json_file in jsons:
    with open(f"jsons/{json_file}") as f:
        content = json.load(f)
    print(f"Creating Embeddings for {json_file}")
    embeddings = create_embedding([c['text'] for c in content['chunks']])
       
    for i, chunk in enumerate(content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk_id += 1
        my_dicts.append(chunk) 
# print(my_dicts)

df = pd.DataFrame.from_records(my_dicts)
# print(df_embeddings)
# Save this dataframe
joblib.dump(df, 'embeddings.joblib')
# # a = create_embedding(["Cat sat on the mat", "Harry dances on a mat"])
# # print(a)


# import requests
# import os
# import json
# import pandas as pd

# def create_embedding(texts):

#     r = requests.post(
#         "http://localhost:11434/api/embeddings",
#         json={
#             "model": "bge-m3",
#             "prompt": texts
#         }
#     )

#     response = r.json()
#     print(response)

#     # if multiple embeddings returned
#     if "embeddings" in response:
#         return response["embeddings"]

#     # if single embedding returned
#     elif "embedding" in response:
#         return [response["embedding"]]

#     else:
#         raise Exception(response)

# jsons = os.listdir("jsons")

# my_dicts = []
# chunk_id = 0

# for json_file in jsons:

#     with open(f"jsons/{json_file}") as f:
#         content = json.load(f)

#     print(f"Creating Embeddings for {json_file}")

#     texts = [c['text'] for c in content['chunks']]

#     embeddings = create_embedding(texts)

#     for i, chunk in enumerate(content['chunks']):

#         chunk['chunk_id'] = chunk_id
#         chunk['embedding'] = embeddings[i]

#         chunk_id += 1

#         my_dicts.append(chunk)

# df = pd.DataFrame.from_records(my_dicts)
# print(df)