import json
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Load configuration from environment variables
QDRANT_URL = os.getenv('QDRANT_URL', 'https://33c22064-4170-49ed-8a6c-e94ced19111b.us-east4-0.gcp.cloud.qdrant.io:6333')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ETikYAkkQSUn0AWte1oG1rX97amGVIAh0vSdxnc0d1o')

def initialize_client():
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

def main():
    # Initialize client
    client = initialize_client()
    collection_name = "product_comments3"
    
    # Set the model before adding documents
    client.set_model('BAAI/bge-small-en-v1.5')
    
    # Optional: Add this before create_collection
    # if collection_name in client.get_collections().collections:
    #     print(f"Collection {collection_name} already exists")
    # else:
    #     client.create_collection(
    #         collection_name=collection_name,
    #         vectors_config=models.VectorParams(
    #             size=384,  # BGE-small model produces 384-dimensional vectors
    #             distance=models.Distance.COSINE
    #         ),
    #         on_disk_payload=True
    #     )
    
    # Read comments from JSON file
    with open('comments.json', 'r') as f:
        data = json.load(f)
    
    comments = data['comments']
    print(f"Found {len(comments)} comments in {data['video_title']} by {data['channel']}")
    
    # Add comments to Qdrant
    client.add(
        collection_name=collection_name,
        documents=[comment["text"] for comment in comments],
        metadata=comments,
        ids=list(range(len(comments)))
    )
    
    print(f"Successfully added {len(comments)} comments to Qdrant")
    
    # Test search
    search_result = client.query(
        collection_name=collection_name,
        query_text="What do people think about competition?",
        limit=3
    )
    
    print("\nSample search results:")
    for result in search_result:
        print(f"Score: {result.score}")
        print(f"Text: {result.document}")
        print(f"Metadata: {result.metadata}")
        print("---")

if __name__ == "__main__":
    main()