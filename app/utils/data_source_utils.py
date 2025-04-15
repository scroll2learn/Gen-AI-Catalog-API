import httpx
from fastapi import HTTPException
from typing import Optional
import numpy as np

async def get_text_embedding(string1: Optional[str] = None, string2: Optional[str] = None, string3: Optional[str] = None):
    texts = [text for text in [string1, string2, string3] if text]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://agent-ai-app:8090/api/embedding/get_text_embedding",
                json={"texts": texts}
            )
            response.raise_for_status()
            embeddings = response.json()["embeddings"]
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to get embeddings: {str(e)}")

    # Combine embeddings to store it in one database field
    if len(embeddings) == 2:
        combined_embedding = embeddings[0] + embeddings[1] 
    elif len(embeddings) == 3:
        combined_embedding = (embeddings[0], embeddings[1], embeddings[2])
    else:
        combined_embedding = embeddings[0] 
    return combined_embedding


async def get_query_embedding(user_query: str):
    """Gets the embedding for the query and extends it to match 1536 dimensions."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://agent-ai-app:8090/api/embedding/get_text_embedding",
                json={"texts": [user_query]}
            )
            response.raise_for_status()
            embedding = response.json()["embeddings"][0]  # Original 768 dimensions
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to get embeddings: {str(e)}")

    # Normalize embedding for consistent comparison
    norm = np.linalg.norm(embedding)
    normalized_embedding = embedding / norm if norm > 0 else embedding

    # Duplicate embedding to match 1536 dimensions
    extended_embedding = np.tile(normalized_embedding, 2).tolist()
    return extended_embedding, embedding
