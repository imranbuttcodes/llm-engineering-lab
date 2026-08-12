

# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np

# # Define two vectors
# vector_a = np.array([[1, 2, 3]])
# vector_b = np.array([[-4, 5, 1]])
# print(vector_a)
# print()
# print(vector_b)
# print()
# # Calculate cosine similarity
# similarity = cosine_similarity(vector_a, vector_b)
# print(similarity)
# print()
# print(f"Similarity: {similarity[0][0]:.4f}")









from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# documents = [
#     "Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.",
#     "MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
#     "Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",
#     "Rohit Sharma is known for his elegant batting and record-breaking double centuries.",
#     "Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers."
# ]
# query = "tell me about virat kohli"

# # Vectorize using TF-IDF (standard for text retrieval)
# vectorizer = TfidfVectorizer()
# all_texts = documents + [query]
# tfidf_matrix = vectorizer.fit_transform(all_texts)
# print(len(list(vectorizer.get_feature_names_out())))
# print()
# print(list(vectorizer.get_feature_names_out()))


# print()
# print()
# print(tfidf_matrix)
# # Separate documents and query
# doc_vectors = tfidf_matrix[:-1]
# query_vector = tfidf_matrix[-1]

# print()
# print(doc_vectors)
# print()
# print(query_vector)
# print()
# print()

# # Calculate scores
# scores = cosine_similarity(query_vector, doc_vectors).flatten()
# for i, score in enumerate(scores):
#     print(f"Doc {i+1}: {score:.4f}")





documents = [
    "Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.",
    "MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
    "Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",
    "Rohit Sharma is known for his elegant batting and record-breaking double centuries.",
    "Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers."
]

query = 'tell me about Virat Kohli'

emb_model = HuggingFaceEmbeddings(model = 'sentence-transformers/all-MiniLM-L6-v2')

doc_embedding = emb_model.embed_documents(documents)

query_embedding = emb_model.embed_query(query)

scores = cosine_similarity([query_embedding], doc_embedding).flatten()

print("Checking Similarity for", query,'.....')
for i, score in enumerate(scores):
    print(f'Doc {i + 1}: {score:.4f}')

index, score = sorted(list(enumerate(scores)), key = lambda x:x[1])[-1]


print("Document with high Similarity") 
print(f"Document: {documents[index]}")
print(f"index: {index} | Similarity Score: {score:.4f}")

#This is also use in sementic Search!