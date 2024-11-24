from txtai import Embeddings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Initialize the BM25 index with txtai
keyword_index = Embeddings()

# Initialize the sentence transformer model for semantic search
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load your constitutional names from the JSON file

with open('final_database_v1.json', 'r') as file:
    names =  json.load(file)

def keyword_search(query, names):
    keyword_results = []
    
    for item in names:
        # Check for keyword match
        keyword_score = 0
        if query.lower() in item['name'].lower():
            keyword_score += 1
        if query.lower() in item['title'].lower():
            keyword_score += 1
        if query.lower() in item['description'].lower():
            keyword_score += 1
        
        if keyword_score > 0:  # Only consider matches
            keyword_results.append({"name": item["name"], 
                        "title": item["title"],
                        "description": item["description"], 
                        "info": item["info"],
                        "score": keyword_score})  # Higher count = higher relevance

    # Sort results by relevance (highest score first)
    keyword_results.sort(key=lambda x: x["score"], reverse=True)
    return keyword_results

# Create list of names for keyword indexing (BM25)
index_data = [{"name": name["name"], "title": name["title"], "description": name["description"]} for name in names]

# Generate sentence embeddings for the semantic index
name_texts = [name["description"] for name in names]
name_embeddings = semantic_model.encode(name_texts, convert_to_tensor=True)



def hybrid_search(query, weight_keyword, weight_semantic):
    # Perform keyword-based search using BM25
    keyword_results = keyword_search(query, names)  # Top 5 results based on keyword matching
    print(keyword_results)
    # Perform semantic search using LLM embeddings
    query_embedding = semantic_model.encode([query], convert_to_tensor=True)
    similarities = cosine_similarity(query_embedding, name_embeddings)
    semantic_results_indices = similarities.argsort()[0][-10:][::-1]  # Top 5 results based on semantic similarity
    # Combine results
    results = {}
    
    # Process BM25 keyword-based results
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
        
        # Check if the name is already in the results and if the semantic score is better
        if name["name"] not in results:
            results[name["name"]] = {
                "name": name["name"],
                "title": name["title"],
                "description": name["description"],
                "info": name["info"],
                "score": semantic_score
            }
        else:
            # If name is in both, you can merge or compare scores
            existing_score = results[name["name"]]["score"]
            new_score = semantic_score
            results[name["name"]]["score"] = max(existing_score, new_score)  # Take the best score

    # Sort the combined results by score (highest to lowest)
    sorted_results = sorted(results.values(), key=lambda x: x['score'], reverse=True)
    
    return sorted_results
