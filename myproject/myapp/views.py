from django.shortcuts import render
from django.conf import settings
#from .models import Laws
import json
from .hybrid_search import hybrid_search_dynamic_normalized
from django.http import JsonResponse

# def search(request):
#     # Initialize the BM25 index with txtai
#     keyword_index = Embeddings()

#     # Initialize the sentence transformer model for semantic search
#     semantic_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#     # Load your constitutional articles from the JSON file
#     with open('constitution_of_india.json', 'r') as file:
#         articles = json.load(file)

#     # Create list of articles for keyword indexing (BM25)
#     index_data = [{"article": article["article"], "description": article["description"]} for article in articles]  
#     # Index the articles for keyword search
#     keyword_index.index(index_data)

#     # Generate sentence embeddings for the semantic index
#     article_texts = [article["description"] for article in articles]
#     article_embeddings = semantic_model.encode(article_texts, convert_to_tensor=True)

#     # Now you can use keyword_index and article_embeddings for hybrid search functionality  
#     # Add your search logic here (e.g., handle user query)
#     query = request.POST.get("query")
#     # Keyword search example (using BM25)
#     keyword_results = keyword_index.search(query, 5)  # Adjust the number of results
    
#     # Semantic search example (using cosine similarity with sentence embeddings)
#     query_embedding = semantic_model.encode([query], convert_to_tensor=True)
#     semantic_results = cosine_similarity(query_embedding, article_embeddings)
    
#     # You can combine the results from both searches to perform hybrid search here

#     # For example, if you return the results:
#     return render(request, 'search.html',{
#         "keyword_results": keyword_results,
#         "semantic_results": semantic_results.tolist(),  # Convert tensor to list for JSON serialization
#     })



def search(request):
    query = request.POST['searched']
    search_results = [] 
    
    # def dynamic_weighting(query):
    # # Simple rule: if the query is short and specific, prioritize keyword search
    #     if len(query.split()) < 3:
    #         return 0.8, 0.2  # More weight to BM25 (keyword)
    #     else:
    #         return 0.2, 0.8  # More weight to semantic search
        
    if query:
        # weight_keyword, weight_semantic = dynamic_weighting(query)
        search_results = hybrid_search_dynamic_normalized(query)
        # search_results = hybrid_search(query,weight_keyword,weight_semantic)
    return render(request, 'search.html', {'query': query, 'results': search_results})



# Load the model and articles
# model = SentenceTransformer("nli-mpnet-base-v2")
# with open('constitution_of_india.json', 'r') as f:
#     articles = json.load(f)
# article_embeddings = [model.encode(article['description']) for article in articles]

# def search(request):
#     query = request.POST['searched']
#     if query:
#         query_embedding = model.encode(query)
#         similarities = cosine_similarity([query_embedding], article_embeddings)
#         top_indices = similarities[0].argsort()[-10:][::-1]
#         results = [{"article":articles[i]["article"],"title": articles[i]["title"], "description": articles[i]["description"]} for i in top_indices]
#     else:
#         results = []

#     return render(request, 'search.html', {'query': query, 'results': results})

# Create your views here.
def index(request):
    return render(request, 'index.html')



# def search(request):
#     laws=None
#     if request.method == "POST":
#         raw_searched = request.POST['searched']
#         searched_values = raw_searched.split()
#         for searched in searched_values:
#             laws = Laws.objects.filter(desc__contains=searched) | Laws.objects.filter(title__contains=searched) | Laws.objects.filter(law_name__contains=searched)
#         return render(request, 'search.html', {'laws':laws,'raw_searched': raw_searched})
#     else:
#         return render(request, 'search.html')


