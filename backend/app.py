import pickle
import logging
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the saved model and vectorizer
with open("classifier.py", "rb") as f:
    vectorizer, model = pickle.load(f)
app = Flask(__name__)

# Dummy emails
emails = [
    {"id": 1, "subject": "You've won!", "body": "Click here to claim your prize", "sender": "scam@example.com"},
    {"id": 2, "subject": "Meeting tomorrow", "body": "Don't forget our meeting at 10am", "sender": "boss@example.com"}
]

# Route: /inbox
@app.route("/inbox", methods=["GET"])
def inbox():
    return jsonify(emails)

# Route: /classify
@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    email_text = data.get("body", "")
    
    X = vectorizer.transform([email_text])
    prediction = model.predict(X)[0]
    
    return jsonify({"prediction": prediction})
    
# Route: /send
@app.route("/send", methods=["POST"])
def send_email():
    data = request.get_json()
    new_email = {
        "id": len(emails) + 1,
        "subject": data.get("subject", ""),
        "body": data.get("body", ""),
        "sender": data.get("sender", "me@example.com")
    }
    emails.append(new_email)
    return jsonify({"status": "Email sent", "email": new_email})

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/test", methods=["GET"])
def test_classify():
    mock_email = {
        "subject": "Claim your free iPhone!",
        "body": "Click the link to get your prize",
        "sender": "scammer@example.com"
    }
    X = vectorizer.transform([mock_email["body"]])
    prediction = model.predict(X)[0]
    return jsonify({"mock_email_prediction": prediction})
    logging.info(f"Email body: {email_text}")
    logging.info(f"Prediction: {prediction}")



