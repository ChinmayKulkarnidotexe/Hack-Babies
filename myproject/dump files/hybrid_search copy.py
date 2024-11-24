from txtai import Embeddings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re

# Initialize the BM25 index with txtai
keyword_index = Embeddings()

# Initialize the sentence transformer model for semantic search
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load your constitutional names from the JSON file

with open('final_database_v1.json', 'r') as file:
    names =  json.load(file)


def preprocess_query(query):
    # Extract specific article number from query
    match = re.search(r'\barticle (\d+)\b', query, re.IGNORECASE)
    if match:
        return f"Article {match.group(1)}"  # Normalize to "Article X" format
    return query  # Return original query if no match




def keyword_search(query, names):
    keyword_results = []
    # Extract specific article number if present
    match = re.search(r'\barticle (\d+)\b', query, re.IGNORECASE)
    article_number = match.group(1) if match else None

    for item in names:
        keyword_score = 0

        # Check for exact article match
        if article_number and f"Article {article_number}" == item["name"]:
            keyword_score += 5  # Assign higher score for exact matches

        # Check for regex match in name, title, and description
        if query.lower() in item['name'].lower():
            keyword_score += 1
        if query.lower() in item['title'].lower():
            keyword_score += 1
        if query.lower() in item['description'].lower():
            keyword_score += 1

        if keyword_score > 0:  # Only consider matches with a score
            keyword_results.append({
                "name": item["name"], 
                "title": item["title"],
                "description": item["description"], 
                "info": item["info"],
                "score": keyword_score
            })

    # Sort results by relevance (highest score first)
    keyword_results.sort(key=lambda x: x["score"], reverse=True)
    return keyword_results



# Create list of names for keyword indexing (BM25)
index_data = [{"name": name["name"], "title": name["title"], "description": name["description"]} for name in names]

# Generate sentence embeddings for the semantic index
name_texts = [name["description"] for name in names]
name_embeddings = semantic_model.encode(name_texts, convert_to_tensor=True)



def hybrid_search(query, weight_keyword, weight_semantic):
    # Preprocess query to normalize and extract specific article number
    processed_query = preprocess_query(query)
    match = re.search(r'\barticle (\d+)\b', processed_query, re.IGNORECASE)
    article_number = match.group(1) if match else None

    # Perform keyword-based search
    keyword_results = keyword_search(processed_query, names)

    # Perform semantic search
    query_embedding = semantic_model.encode([processed_query], convert_to_tensor=True)
    similarities = cosine_similarity(query_embedding, name_embeddings)
    semantic_results_indices = similarities.argsort()[0][-10:][::-1]  # Top 10 results

    results = {}

    # Process keyword-based results
    for name in keyword_results:
        results[name["name"]] = {
            "name": name["name"],
            "title": name["title"],
            "description": name["description"],
            "info": name["info"],
            "score": float(name["score"]) * weight_keyword  # Adjust score by weight
        }

    # Process semantic-based results
    for idx in semantic_results_indices:
        name = names[idx]
        semantic_score = similarities[0][idx] * weight_semantic  # Adjust score by weight

        # If the query contains an article number, filter semantic results
        if article_number and f"Article {article_number}" != name["name"]:
            continue  # Skip non-matching articles

        # Add or merge results
        if name["name"] not in results:
            results[name["name"]] = {
                "name": name["name"],
                "title": name["title"],
                "description": name["description"],
                "info": name["info"],
                "score": semantic_score
            }
        else:
            # Merge scores
            existing_score = results[name["name"]]["score"]
            results[name["name"]]["score"] = max(existing_score, semantic_score)

    # Sort combined results by score
    sorted_results = sorted(results.values(), key=lambda x: x['score'], reverse=True)

    return sorted_results

