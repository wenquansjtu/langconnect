import json

from langchain_core.embeddings import Embeddings
from starlette.config import Config, undefined

env = Config()

IS_TESTING = env("IS_TESTING", cast=str, default="").lower() == "true"

if IS_TESTING:
    SUPABASE_URL = ""
    SUPABASE_KEY = ""
else:
    SUPABASE_URL = env("SUPABASE_URL", cast=str, default="https://blnamczglqvlmchqnicc.supabase.co")
    SUPABASE_KEY = env("SUPABASE_KEY", cast=str, default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJsbmFtY3pnbHF2bG1jaHFuaWNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk1MjExNjUsImV4cCI6MjA2NTA5NzE2NX0.AoUWXjvzKJUIgL4kQY7vMn4bzwQpTKOQLWyD2Ox2zYo")


def get_embeddings() -> Embeddings:
    """Get the embeddings instance based on the environment."""
    if IS_TESTING:
        from langchain_core.embeddings import DeterministicFakeEmbedding

        return DeterministicFakeEmbedding(size=512)
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(api_key="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")


DEFAULT_EMBEDDINGS = get_embeddings()
DEFAULT_COLLECTION_NAME = "default_collection"


# Database configuration
POSTGRES_HOST = env("POSTGRES_HOST", cast=str, default="postgres")
POSTGRES_PORT = env("POSTGRES_PORT", cast=int, default="5432")
POSTGRES_USER = env("POSTGRES_USER", cast=str, default="langchain")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD", cast=str, default="langchain")
POSTGRES_DB = env("POSTGRES_DB", cast=str, default="langchain_test")

# Read allowed origins from environment variable
ALLOW_ORIGINS_JSON = env("ALLOW_ORIGINS", cast=str, default="")

if ALLOW_ORIGINS_JSON:
    ALLOWED_ORIGINS = json.loads(ALLOW_ORIGINS_JSON.strip())
    print(f"ALLOW_ORIGINS environment variable set to: {ALLOW_ORIGINS_JSON}")
else:
    ALLOWED_ORIGINS = ["https://forgeai.matrix.io"]
    print("ALLOW_ORIGINS environment variable not set.")
