from txtai import Embeddings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Initialize the BM25 index with txtai
keyword_index = Embeddings()

# Initialize the sentence transformer model for semantic search
semantic_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load your constitutional articles from the JSON file
with open('constitution_of_india.json', 'r') as file:
    articles = json.load(file)

# Create list of articles for keyword indexing (BM25)
index_data = [{"article": article["article"], "title": article["title"]} for article in articles]
keyword_index.index(index_data)

# Generate sentence embeddings for the semantic index
article_texts = [article["description"] for article in articles]
article_embeddings = semantic_model.encode(article_texts, convert_to_tensor=True)
