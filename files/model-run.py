from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.ollama import Ollama
import chromadb

# Connect to ChromaDB
chroma_client = chromadb.HttpClient(host="192.168.134.30", port=8000)
chroma_collection = chroma_client.get_or_create_collection("class_context")

# Wrap the Chroma collection for LlamaIndex
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Set global settings (new API)
Settings.llm = Ollama(model="mistral")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

# Load the index
index = VectorStoreIndex.from_vector_store(vector_store)

# Query engine
query_engine = index.as_query_engine()

# Example usage
response = query_engine.query("What's happening in room 101?")
print(response)
