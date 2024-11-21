from txtai import Embeddings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import torch

# Initialize the BM25 index with txtai
keyword_index = Embeddings()

# Initialize the sentence transformer model for semantic search
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load your constitutional articles from the JSON file
with open('final_clean_constitution.json', 'r') as file:
    articles = json.load(file)

# Create list of articles for keyword indexing (BM25)
index_data = [{"article": article["article"], "title": article["title"]} for article in articles]
keyword_index.index(index_data)

# Generate sentence embeddings for the semantic index
article_texts = [article["description"] for article in articles]
article_embeddings = semantic_model.encode(article_texts, convert_to_tensor=True)

def normalize_scores(scores):
    """
    Normalize a list of scores to the range [0, 1].

    Parameters:
        scores (list of float): The scores to normalize.

    Returns:
        list of float: Normalized scores.
    """
    if not scores:  # Check if the scores list is empty
        return []  # Return an empty list if no scores are available

    min_score = min(scores)
    max_score = max(scores)

    # Avoid division by zero if all scores are the same
    if max_score - min_score == 0:
        return [0.5] * len(scores)  # Assign a neutral value if scores can't be differentiated

    return [(score - min_score) / (max_score - min_score) for score in scores]



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


def hybrid_search_dynamic_normalized(query):
    results = {}

    # Perform keyword-based search
    keyword_results = keyword_index.search(query, len(articles))
    if not keyword_results:
        print("No keyword results found.")  # Debugging log

    bm25_scores = [result[1] for result in keyword_results] if keyword_results else []
    bm25_scores_normalized = normalize_scores(bm25_scores)

    # Perform semantic search
    query_embedding = semantic_model.encode([query], convert_to_tensor=True)

    if article_embeddings.numel() > 0:  # Check if tensor is non-empty
        similarities = cosine_similarity(
            query_embedding.cpu().detach().numpy(),
            article_embeddings.cpu().detach().numpy()
        )[0]

        # Check if similarities array is non-empty
        if similarities.size > 0:
            semantic_scores_normalized = normalize_scores(similarities)
        else:
            semantic_scores_normalized = []
    else:
        similarities = []
        semantic_scores_normalized = []



    # if not similarities:
    #     print("No semantic results found.")  # Debugging log

    # semantic_scores_normalized = normalize_scores(similarities)

    # Dynamically calculate weights
    query_length = len(query.split())
    if query_length > 5:
        weight_keyword = 0.3
        weight_semantic = 0.7
    elif query_length <= 3:
        weight_keyword = 0.7
        weight_semantic = 0.3
    else:
        weight_keyword = 0.5
        weight_semantic = 0.5

    # Normalize weights
    weight_sum = weight_keyword + weight_semantic
    weight_keyword /= weight_sum
    weight_semantic /= weight_sum

    # Combine results if any scores exist
    for i, result in enumerate(keyword_results):
        article_id = result[0]
        if article_id not in results:
            results[article_id] = {
                "article": articles[article_id]["article"],
                "title": articles[article_id]["title"],
                "description": articles[article_id]["description"],
                "bm25_score": bm25_scores_normalized[i] if bm25_scores_normalized else 0,
                "semantic_score": 0,
                "combined_score": (bm25_scores_normalized[i] * weight_keyword) if bm25_scores_normalized else 0,
            }

    for i, semantic_score in enumerate(semantic_scores_normalized):
        article_id = i
        if article_id not in results:
            results[article_id] = {
                "article": articles[article_id]["article"],
                "title": articles[article_id]["title"],
                "description": articles[article_id]["description"],
                "bm25_score": 0,
                "semantic_score": semantic_score,
                "combined_score": semantic_score * weight_semantic,
            }
        else:
            results[article_id]["semantic_score"] = semantic_score
            results[article_id]["combined_score"] += semantic_score * weight_semantic

    # Sort results by combined score (highest first)
    sorted_results = sorted(results.values(), key=lambda x: x["combined_score"], reverse=True)
    return sorted_results



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
#         weight_keyword = 0.3
#         weight_semantic = 0.7
#     elif query_length <= 3:  # Short query favors keyword search
#         weight_keyword = 0.7
#         weight_semantic = 0.3
#     else:  # Medium-length query balances both
#         weight_keyword = 0.5
#         weight_semantic = 0.5

#     # Normalize weights (ensure they sum to 1)
#     weight_sum = weight_keyword + weight_semantic
#     weight_keyword /= weight_sum
#     weight_semantic /= weight_sum

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
#                 "combined_score": bm25_scores_normalized[i] * weight_keyword,
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
#                 "combined_score": semantic_score * weight_semantic,
#             }
#         else:
#             # Combine scores dynamically with normalized weights
#             results[article_id]["semantic_score"] = semantic_score
#             results[article_id]["combined_score"] += semantic_score * weight_semantic

#     # Sort results by combined score (highest first)
#     sorted_results = sorted(results.values(), key=lambda x: x["combined_score"], reverse=True)
#     return sorted_results
