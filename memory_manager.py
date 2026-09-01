"""
Wraps Mem0 configured to use Qdrant Cloud as its vector store,
and Google Gemini as the LLM + embedder.
"""

import os

from dotenv import load_dotenv
from mem0 import Memory


load_dotenv()


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "recipe_user_memory",
            "url": QDRANT_URL,
            "api_key": QDRANT_API_KEY,
            "embedding_model_dims": 768,
        },
    },

    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-3.6-flash",
            "api_key": GOOGLE_API_KEY,
        },
    },

    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "models/gemini-embedding-001",
            "api_key": GOOGLE_API_KEY,
        },
    },
}


memory = Memory.from_config(config)


def store_message(user_id: str, message: str):
    memory.add(
        message,
        user_id=user_id
    )


def get_relevant_memories(
    user_id: str,
    query: str,
    limit: int = 5
) -> list[str]:

    results = memory.search(
        query=query,
        filters={"user_id": user_id},
        limit=limit
    )

    return [
        item["memory"]
        for item in results.get("results", [])
    ]


def get_all_memories(user_id: str) -> list[str]:

    results = memory.get_all(
        filters={"user_id": user_id}
    )

    return [
        item["memory"]
        for item in results.get("results", [])
    ]