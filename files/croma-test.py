import chromadb

client = chromadb.HttpClient(host="192.168.134.30", port=8000)
collection = client.get_or_create_collection("class_context")

print("✅ Connected to ChromaDB!")
