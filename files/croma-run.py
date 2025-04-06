import chromadb
import json

# Connect to ChromaDB
client = chromadb.HttpClient(host="192.168.134.30", port=8000)
collection = client.get_or_create_collection("class_context")

print("✅ Connected to ChromaDB!")

# Load schedule from a JSON file
with open("context/timetable.json", "r") as f:
    schedule = json.load(f)

# Insert each item
for item in schedule:
    doc_text = (
        f"{item['subject']} class on {item['day']} from {item['start_time']} to {item['end_time']} "
        f"in {item['location']}. {item['description']} "
        f"Syllabus: {item['syllabus_url']}, Notes: {item['notes_url']}"
    )

    collection.add(
        documents=[doc_text],
        ids=[item["id"]],
        metadatas=[{
            "day": item["day"],
            "start_time": item["start_time"],
            "end_time": item["end_time"],
            "location": item["location"],
            "subject": item["subject"]
        }]
    )
    print(f"➕ Inserted: {item['id']}")

print("✅ All entries inserted into ChromaDB.")
