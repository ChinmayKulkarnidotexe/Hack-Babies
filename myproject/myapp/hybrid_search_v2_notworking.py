# from txtai import Embeddings
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# import json
# import torch

from txtai import Embeddings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from django.http import JsonResponse

# Initialize the BM25 index with txtai
keyword_index = Embeddings()

# Initialize the SentenceTransformer model for semantic search
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load your constitutional articles from the JSON file (one-time initialization)
with open('final_clean_constitution.json', 'r') as file:
    articles = json.load(file)

# Create list of articles for keyword indexing (BM25)
index_data = [{"article": article["article"], "title": article["title"]} for article in articles]
keyword_index.index(index_data)

# Generate semantic embeddings for all articles (one-time initialization)
article_texts = [article["description"] for article in articles]
article_embeddings = semantic_model.encode(article_texts, convert_to_tensor=True)
# def normalize_scores(bm25_scores, semantic_scores):
#     # Normalize BM25 scores (0-1 scaling)
#     if bm25_scores.max().item() > 0:  # Ensure max is a scalar
#         bm25_scores = bm25_scores / bm25_scores.max().item()

#     # Normalize semantic scores (0-1 scaling)
#     if semantic_scores.max().item() > 0:  # Ensure max is a scalar
#         semantic_scores = semantic_scores / semantic_scores.max().item()

#     return bm25_scores, semantic_scores

def normalize_scores(bm25_scores, semantic_scores):
    # Ensure bm25_scores is not empty before normalizing
    if bm25_scores.size > 0 and bm25_scores.max().item() > 0:
        bm25_scores = bm25_scores / bm25_scores.max().item()

    # Ensure semantic_scores is not empty before normalizing
    if semantic_scores.size > 0 and semantic_scores.max().item() > 0:
        semantic_scores = semantic_scores / semantic_scores.max().item()

    return bm25_scores, semantic_scores


def hybrid_search(query):
    """
    Hybrid search that combines keyword (BM25) and semantic search using dynamic weighting
    and normalized scores.
    """
    
    # Dynamically calculate weights
    query_length = len(query.split())
    if query_length > 5:
        keyword_weight = 0.3
        semantic_weight = 0.7
    elif query_length <= 3:
        keyword_weight = 0.7
        semantic_weight = 0.3
    else:
        keyword_weight = 0.5
        semantic_weight = 0.5

    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)

    # Normalize weights to ensure they sum to 1
    total_weight = keyword_weight + semantic_weight
    keyword_weight /= total_weight
    semantic_weight /= total_weight

    # Perform keyword search (BM25)
    keyword_results = keyword_index.search(query, 10)

    # Extract BM25 scores and normalize them (0-1 scaling)
    bm25_scores = np.array([result["score"] for result in keyword_results])
    bm25_scores, semantic_scores = normalize_scores(bm25_scores, np.zeros(len(bm25_scores)))  # Empty semantic scores for now

    # Perform semantic search (cosine similarity)
    query_embedding = semantic_model.encode([query], convert_to_tensor=True)
    all_semantic_scores = cosine_similarity(query_embedding, article_embeddings)

    semantic_scores = all_semantic_scores.argsort()[0][-10:][::-1]

    # Normalize semantic scores (0-1 scaling)
    semantic_scores, bm25_scores = normalize_scores(semantic_scores, bm25_scores)  # Normalize both

    # Combine results with normalized scores and dynamic weighting
    combined_scores = {}
    for i, article in enumerate(articles):
        # Compute the weighted combined score
        bm25_score = bm25_scores[i] if i < len(bm25_scores) else 0.0
        if i < len(semantic_scores):
            semantic_score = semantic_scores[i]
        combined_score = (keyword_weight * bm25_score) + (semantic_weight * semantic_score)

        combined_scores[article["article"]] = {
            "title": article["title"],
            "description": article["description"],
            "combined_score": combined_score,
            "bm25_score": bm25_score,
            "semantic_score": semantic_score,
        }

    # Sort results by combined score in descending order
    sorted_results = sorted(combined_scores.values(), key=lambda x: x["combined_score"], reverse=True)

    # Return the top 10 results as a JSON response
    # response = [
    #     {
    #         "article": article,
    #         "title": result["title"],
    #         "description": result["description"],
    #         "combined_score": result["combined_score"],
    #         "bm25_score": result["bm25_score"],
    #         "semantic_score": result["semantic_score"],
    #     }
    #     for article_number, result in sorted_results[:10]
    # ]

    # return JsonResponse({"results": response})
    return sorted_results

# # Initialize the BM25 index with txtai
# keyword_index = Embeddings()

# # Initialize the sentence transformer model for semantic search
# semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# # Load your constitutional articles from the JSON file
# with open('final_clean_constitution.json', 'r') as file:
#     articles = json.load(file)

# # Create list of articles for keyword indexing (BM25)
# index_data = [{"article": article["article"], "title": article["title"]} for article in articles]
# keyword_index.index(index_data)

# # Generate sentence embeddings for the semantic index
# article_texts = [article["description"] for article in articles]
# article_embeddings = semantic_model.encode(article_texts, convert_to_tensor=True)

# def normalize_scores(scores):
#     """
#     Normalize a list of scores to the range [0, 1].

#     Parameters:
#         scores (list of float): The scores to normalize.

#     Returns:
#         list of float: Normalized scores.
#     """
#     if not scores:  # Check if the scores list is empty
#         return []  # Return an empty list if no scores are available

#     min_score = min(scores)
#     max_score = max(scores)

#     # Avoid division by zero if all scores are the same
#     if max_score - min_score == 0:
#         return [0.5] * len(scores)  # Assign a neutral value if scores can't be differentiated

#     return [(score - min_score) / (max_score - min_score) for score in scores]



# def normalize_scores(scores):
#     """
#     Normalize a list of scores to the range [0, 1].

#     Parameters:
#         scores (list of float): The scores to normalize.

#     Returns:
#         list of float: Normalized scores.
#     """
#     min_score = min(scores)
#     max_score = max(scores)

#     # Avoid division by zero if all scores are the same
#     if max_score - min_score == 0:
#         return [0.5] * len(scores)  # Assign a neutral value if scores can't be differentiated

#     return [(score - min_score) / (max_score - min_score) for score in scores]


# def hybrid_search_dynamic_normalized(query):
#     results = {}

#     # Perform keyword-based search
#     keyword_results = keyword_index.search(query, len(articles))
#     if not keyword_results:
#         print("No keyword results found.")  # Debugging log

#     bm25_scores = [result[1] for result in keyword_results] if keyword_results else []
#     bm25_scores_normalized = normalize_scores(bm25_scores)

#     # Perform semantic search
#     query_embedding = semantic_model.encode([query], convert_to_tensor=True)

#     if article_embeddings.numel() > 0:  # Check if tensor is non-empty
#         similarities = cosine_similarity(query_embedding,article_embeddings)
#         semantic_results_indices = similarities.argsort()[0][-10:][::-1]

#         # Check if similarities array is non-empty
#         if semantic_results_indices.size > 0:
#             semantic_scores_normalized = normalize_scores(semantic_results_indices)
#         else:
#             semantic_scores_normalized = []
#     else:
#         semantic_results_indices = []
#         semantic_scores_normalized = []



#     # if not similarities:
#     #     print("No semantic results found.")  # Debugging log

#     # semantic_scores_normalized = normalize_scores(similarities)

#     # Dynamically calculate weights
#     query_length = len(query.split())
#     if query_length > 5:
#         keyword_weight = 0.3
#         semantic_weight = 0.7
#     elif query_length <= 3:
#         keyword_weight = 0.7
#         semantic_weight = 0.3
#     else:
#         keyword_weight = 0.5
#         semantic_weight = 0.5

#     # Normalize weights
#     weight_sum = keyword_weight + semantic_weight
#     keyword_weight /= weight_sum
#     semantic_weight /= weight_sum

#     # Combine results if any scores exist
#     for i, result in enumerate(keyword_results):
#         article_id = result[0]
#         if article_id not in results:
#             results[article_id] = {
#                 "article": articles[article_id]["article"],
#                 "title": articles[article_id]["title"],
#                 "description": articles[article_id]["description"],
#                 "bm25_score": bm25_scores_normalized[i] if bm25_scores_normalized else 0,
#                 "semantic_score": 0,
#                 "combined_score": (bm25_scores_normalized[i] * keyword_weight) if bm25_scores_normalized else 0,
#             }

#     for i, semantic_score in enumerate(semantic_scores_normalized):
#         article_id = i
#         if article_id not in results:
#             results[article_id] = {
#                 "article": articles[article_id]["article"],
#                 "title": articles[article_id]["title"],
#                 "description": articles[article_id]["description"],
#                 "bm25_score": 0,
#                 "semantic_score": semantic_score,
#                 "combined_score": semantic_score * semantic_weight,
#             }
#         else:
#             results[article_id]["semantic_score"] = semantic_score
#             results[article_id]["combined_score"] += semantic_score * semantic_weight

#     # Sort results by combined score (highest first)
#     sorted_results = sorted(results.values(), key=lambda x: x["combined_score"], reverse=True)
#     return sorted_results



# def hybrid_search_dynamic_normalized(query):
#     results = {}

#     # Perform keyword-based search
#     keyword_results = keyword_index.search(query, len(articles))
#     bm25_scores = [result[1] for result in keyword_results]
#     bm25_scores_normalized = normalize_scores(bm25_scores)

#     # Perform semantic search
#     query_embedding = semantic_model.encode([query], convert_to_tensor=True)
#     similarities = cosine_similarity(query_embedding.cpu().detach().numpy(), article_embeddings.cpu().detach().numpy())[0]
#     semantic_scores_normalized = normalize_scores(similarities)

#     # Dynamically calculate weights based on query characteristics
#     query_length = len(query.split())

#     # Example logic for dynamic weight calculation
#     if query_length > 5:  # Long query favors semantic search
#         keyword_weight = 0.3
#         semantic_weight = 0.7
#     elif query_length <= 3:  # Short query favors keyword search
#         keyword_weight = 0.7
#         semantic_weight = 0.3
#     else:  # Medium-length query balances both
#         keyword_weight = 0.5
#         semantic_weight = 0.5

#     # Normalize weights (ensure they sum to 1)
#     weight_sum = keyword_weight + semantic_weight
#     keyword_weight /= weight_sum
#     semantic_weight /= weight_sum

#     # Combine results with normalized weights
#     for i, result in enumerate(keyword_results):
#         article_id = result[0]
#         if article_id not in results:
#             results[article_id] = {
#                 "article": articles[article_id]["article"],
#                 "title": articles[article_id]["title"],
#                 "description": articles[article_id]["description"],
#                 "bm25_score": bm25_scores_normalized[i],
#                 "semantic_score": 0,
#                 "combined_score": bm25_scores_normalized[i] * keyword_weight,
#             }

#     for i, semantic_score in enumerate(semantic_scores_normalized):
#         article_id = i
#         if article_id not in results:
#             results[article_id] = {
#                 "article": articles[article_id]["article"],
#                 "title": articles[article_id]["title"],
#                 "description": articles[article_id]["description"],
#                 "bm25_score": 0,
#                 "semantic_score": semantic_score,
#                 "combined_score": semantic_score * semantic_weight,
#             }
#         else:
#             # Combine scores dynamically with normalized weights
#             results[article_id]["semantic_score"] = semantic_score
#             results[article_id]["combined_score"] += semantic_score * semantic_weight

#     # Sort results by combined score (highest first)
#     sorted_results = sorted(results.values(), key=lambda x: x["combined_score"], reverse=True)
#     return sorted_results
