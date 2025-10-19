import pickle
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the saved model and vectorizer
with open("model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)

app = Flask(__name__)
CORS(app)  # allow frontend connections

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
    try:
        data = request.get_json()
        email_text = data.get("body", "")
        if not email_text:
            return jsonify({"error": "No email body provided"}), 400

        X = vectorizer.transform([email_text])
        prediction = model.predict(X)[0]

        logging.info(f"Email classified — Prediction: {prediction}, Body: {email_text}")
        return jsonify({"prediction": prediction})

    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": "Classification failed"}), 500

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
    logging.info(f"New email added: {new_email}")
    return jsonify({"status": "Email sent", "email": new_email})

# Route: /test
@app.route("/test", methods=["GET"])
def test_classify():
    mock_email = {
        "subject": "Claim your free iPhone!",
        "body": "Click the link to get your prize",
        "sender": "scammer@example.com"
    }
    X = vectorizer.transform([mock_email["body"]])
    prediction = model.predict(X)[0]
    logging.info(f"Mock email classified — Prediction: {prediction}")
    return jsonify({"mock_email_prediction": prediction})

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)
