from flask import Flask, jsonify
from pymongo import MongoClient, ReturnDocument
import os

app = Flask(__name__)

# Connect to MongoDB using your environment variable
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.analytics
counters = db.counters

# Ensure the counter exists
def init_counter():
    if counters.find_one({"_id": "total"}) is None:
        counters.insert_one({"_id": "total", "count": 0})

init_counter()

@app.route("/api/visit")
def visit():
    result = counters.find_one_and_update(
        {"_id": "total"},
        {"$inc": {"count": 1}},
        return_document=ReturnDocument.AFTER
    )
    return jsonify({"visits": result["count"]})

@app.route("/")
def home():
    return "MongoDB visitor counter API running."
