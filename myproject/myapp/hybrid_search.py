from txtai import Embeddings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Initialize the BM25 index with txtai
keyword_index = Embeddings()

# Initialize the sentence transformer model for semantic search
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load your constitutional articles from the JSON file
with open('final_clean_constitution.json', 'r') as file:
    articles = json.load(file)

def keyword_search(query, articles):
    
    results = []
    
    for article in articles:
        # Count how many times the query appears in the text
        count = article["description"].lower().count(query.lower())
        
        if count > 0:  # Only consider matches
            results.append({"article": article["article"], 
                            "title": article["title"],
                            "description": article["description"], 
                            "info": article["info"],
                            "score": count})  # Higher count = higher relevance

    # Sort results by relevance (highest score first)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

# Create list of articles for keyword indexing (BM25)
index_data = [{"article": article["article"], "title": article["title"], "description": article["description"]} for article in articles]

# Generate sentence embeddings for the semantic index
article_texts = [article["description"] for article in articles]
article_embeddings = semantic_model.encode(article_texts, convert_to_tensor=True)



def hybrid_search(query, weight_keyword, weight_semantic):
    # Perform keyword-based search using BM25
    keyword_results = keyword_search(query, articles)  # Top 5 results based on keyword matching
    print(keyword_results)
    # Perform semantic search using LLM embeddings
    query_embedding = semantic_model.encode([query], convert_to_tensor=True)
    similarities = cosine_similarity(query_embedding, article_embeddings)
    semantic_results_indices = similarities.argsort()[0][-10:][::-1]  # Top 5 results based on semantic similarity
    # Combine results
    results = {}
    
    # Process BM25 keyword-based results
    for article in keyword_results:
        results[article["article"]] = {
            "article": article["article"],
            "title": article["title"],
            "description": article["description"],
            "info": article["info"],
            "score": float(article["score"]) * weight_keyword *100  # Adjust score by weight
        }

    # Process semantic-based results
    for idx in semantic_results_indices:
        article = articles[idx]
        semantic_score = similarities[0][idx] * weight_semantic * 100  # Adjust score by weight
        
        # Check if the article is already in the results and if the semantic score is better
        if article["article"] not in results:
            results[article["article"]] = {
                "article": article["article"],
                "title": article["title"],
                "description": article["description"],
                "info": article["info"],
                "score": semantic_score
            }
        else:
            # If article is in both, you can merge or compare scores
            existing_score = results[article["article"]]["score"]
            new_score = semantic_score
            results[article["article"]]["score"] = max(existing_score, new_score)  # Take the best score

    # Sort the combined results by score (highest to lowest)
    sorted_results = sorted(results.values(), key=lambda x: x['score'], reverse=True)
    
    return sorted_results
