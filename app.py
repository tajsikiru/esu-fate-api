from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import uuid

app = Flask(__name__)

# Replace with your MongoDB Atlas connection URI
client = MongoClient("mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority")
db = client["esu_fate_ai"]
collection = db["symbolic_history"]

@app.route('/log_session', methods=['POST'])
def log_session():
    data = request.json
    user_id = data['user_id']
    input_text = data['input_text']
    odù = data['odu']
    tags = data['symbol_tags']
    entropy = data['entropy']
    recursion = data['recursion']
    ebo_status = data['ebo_status']
    delay = data['delay']
    resolved = data['resolved']

    session_data = {
        "session_id": f"sess_{uuid.uuid4().hex[:6]}",
        "timestamp": datetime.utcnow(),
        "input_text": input_text,
        "symbol_tags": tags,
        "odù_returned": odù,
        "entropy_score": entropy,
        "recursion_depth": recursion,
        "ebo_status": ebo_status,
        "delay_score": delay,
        "resolved": resolved
    }

    collection.update_one(
        {"_id": user_id},
        {"$push": {"sessions": session_data}},
        upsert=True
    )

    user = collection.find_one({"_id": user_id})
    odu_history = [s["odù_returned"] for s in user["sessions"]]
    recursions = odu_history.count(odù)

    return jsonify({
        "message": "Session logged",
        "recursion_alert": recursions >= 2,
        "repeats": recursions
    })

if __name__ == '__main__':
    app.run(debug=True)
