from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymilvus import Collection, connections
from sentence_transformers import SentenceTransformer
import os

# Initialize FastAPI app
app = FastAPI()

# Milvus and model configuration
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = "19530"           # Default gRPC port
connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
model = SentenceTransformer("WhereIsAI/UAE-Large-V1")

# Define request and response models
class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 3

class QueryResponse(BaseModel):
    id: int
    text_chunk: str
    score: float

@app.post("/query/product", response_model=list[QueryResponse])
def query_milvus_api(request: QueryRequest):
    """
    Query the Milvus index and return the top K matches.

    Parameters:
    - query_text (str): The query string to search for.
    - top_k (int): The number of top matches to return (default is 3).

    Returns:
    - List of top matches as JSON.
    """
    COLLECTION_NAME = "product_details"

    collection_name = COLLECTION_NAME
    collection = Collection(name=collection_name)

    # Ensure collection is loaded into memory
    collection.load()

    # Vectorize the query text
    query_embedding = model.encode([request.query_text])[0]

    # Define search parameters
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    
    # Perform search
    try:
        results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=request.top_k,
            output_fields=["text_chunk"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

    # Process results
    top_matches = [
        QueryResponse(id=result.id, text_chunk=result.entity.get("text_chunk"), score=result.distance)
        for result in results[0]  # results[0] because search returns a list of lists
    ]
    return top_matches


@app.post("/query/hr", response_model=list[QueryResponse])
def query_milvus_api(request: QueryRequest):
    """
    Query the Milvus index and return the top K matches.

    Parameters:
    - query_text (str): The query string to search for.
    - top_k (int): The number of top matches to return (default is 3).

    Returns:
    - List of top matches as JSON.
    """
    COLLECTION_NAME = "HR_policies"

    collection_name = COLLECTION_NAME
    collection = Collection(name=collection_name)

    # Ensure collection is loaded into memory
    collection.load()

    # Vectorize the query text
    query_embedding = model.encode([request.query_text])[0]

    # Define search parameters
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    
    # Perform search
    try:
        results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=request.top_k,
            output_fields=["text_chunk"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

    # Process results
    top_matches = [
        QueryResponse(id=result.id, text_chunk=result.entity.get("text_chunk"), score=result.distance)
        for result in results[0]  # results[0] because search returns a list of lists
    ]
    return top_matches

@app.post("/query/accounts", response_model=list[QueryResponse])
def query_milvus_api(request: QueryRequest):
    """
    Query the Milvus index and return the top K matches.

    Parameters:
    - query_text (str): The query string to search for.
    - top_k (int): The number of top matches to return (default is 3).

    Returns:
    - List of top matches as JSON.
    """
    COLLECTION_NAME = "customer_accounts"

    collection_name = COLLECTION_NAME
    collection = Collection(name=collection_name)

    # Ensure collection is loaded into memory
    collection.load()

    # Vectorize the query text
    query_embedding = model.encode([request.query_text])[0]

    # Define search parameters
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    
    # Perform search
    try:
        results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=request.top_k,
            output_fields=["text_chunk"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

    # Process results
    top_matches = [
        QueryResponse(id=result.id, text_chunk=result.entity.get("text_chunk"), score=result.distance)
        for result in results[0]  # results[0] because search returns a list of lists
    ]
    return top_matches

