from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel
from fastembed import TextEmbedding
from typing import Annotated
#from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models, grpc 
from qdrant_client.http.models import PointStruct
import logging
import os
import uvicorn
import json 

logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG) 
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


_model = None
app = FastAPI()

def llm(query, context):
    prompt_template = f"""
    Give a concise answer to the QUESTION" with simple english as financial consultant.
    Use 'CONTEXT'. In case 'CONTEXT' is empty, give concise answer without 'CONTEXT'.
    QUESTION: {query}
    CONTEXT: {context}
    """.strip()
    # CONTEXT: {context}
    # Provide example from context.

    return prompt_template

def get_model():
    global _model
    if _model is None:
        _reload_model()
    return _model

# Load fastembed model
#model = TextEmbedding("nomic-ai/nomic-embed-text-v1")
# Connect to Qdrant
qdrant_host = os.getenv("QDRANT_HOST", "localhost") 
client = QdrantClient(url=f"http://{qdrant_host}:6333")
COLLECTION_NAME_CONTEXT = "ContextCollection"
COLLECTION_NAME_VIDEO = "VideoCollection"
# Input/Output Models (same as before)
class TextInput(BaseModel):
    text: str
class TextOutput(BaseModel):
    answer: str
    video_url: str 


# Upsert Collection (on startup)
@app.on_event("startup")
async def upsert_collection():
    collection_name_context = COLLECTION_NAME_CONTEXT
    collection_name_video = COLLECTION_NAME_VIDEO

    try:
        collection_exists_context = client.collection_exists(collection_name_context)
    except grpc.RpcError as e:
        print(f"Error checking collection existence: {e}")

    # Check if collection exists, create if not
    if not collection_exists_context:
        try:
            client.create_collection(
                collection_name_context,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)  # Adjust vector config
            )
            print(f"Collection '{collection_name_context}' created.")
        except grpc.RpcError as e:
            print(f"Error creating collection: {e}")
    else:
        print(f"Collection '{collection_name_context}' already exists.")
    # Load data from JSON
    with open("my_collection.json", "r") as f:
        data = json.load(f)
        points = []
        for item in data:
            points.append(PointStruct(id=item['id'], vector=item['vector'], payload=item.get("payload", {})))
        client.upsert(collection_name=collection_name_context, wait=True, points=points)
        
    try:
        collection_exists_video = client.collection_exists(collection_name_video)
    except grpc.RpcError as e:
        print(f"Error checking collection existence: {e}")
        collection_exists_video = False

    # Check if collection exists, create if not
    if not collection_exists_video:
        try:
            client.create_collection(
                collection_name_video,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)  # Adjust vector config
            )
            print(f"Collection '{collection_name_video}' created.")
        except grpc.RpcError as e:
            print(f"Error creating collection: {e}")
    else:
        print(f"Collection '{collection_name_video}' already exists.")
    # Load data from JSON
    with open("my_collection_video_new.json", "r") as f:
        data = json.load(f)
        points = []
        for item in data:
            points.append(PointStruct(id=item['id'], vector=item['vector'], payload=item.get("payload", {})))
        client.upsert(collection_name=collection_name_video, wait=True, points=points)

@app.get("/health")
def health():
    return "OK"

def _reload_model():
    global _model
    _model = TextEmbedding(model_name="nomic-ai/nomic-embed-text-v1")


@app.get("/check_collection_context")
def health_context():
    return client.collection_exists(collection_name=COLLECTION_NAME_CONTEXT)

@app.get("/check_collection_video")
def health_video():
    return client.collection_exists(collection_name=COLLECTION_NAME_VIDEO)

# Search Endpoint (same as before)
@app.post("/search")
def search(text_input: Annotated[TextInput, Body()], model=Depends(get_model)) -> TextOutput:
    query = text_input.text
    query_vector = next(model.embed(query))
    search_result = client.search(
        collection_name=COLLECTION_NAME_CONTEXT,
        query_vector=query_vector.tolist(), limit=1
        )
    
    search_result_video = client.search(
        collection_name=COLLECTION_NAME_VIDEO,
        query_vector=query_vector.tolist(), limit=1
        )
    
    context = "\n".join(search_result[0].payload["context"]) if search_result[0].score >= 0.7 else ""
    print("context search result score", search_result[0].score)
    response = llm(query, context)
    
    
    video_url = search_result_video[0].payload["url"] if search_result_video[0].score >= 0.5 else ""
    print("context search result score", search_result_video[0].score)
    
    return TextOutput(answer=response, video_url=video_url)
    
def main():
    uvicorn.run(app, host="0.0.0.0", port=8991)


if __name__ == "__main__":
    main()
    
    
