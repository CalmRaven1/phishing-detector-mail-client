from flask import Flask, request, jsonify

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
    
    # Dummy classifier logic
    if "click" in email_text.lower() or "won" in email_text.lower():
        prediction = "Phishing"
    else:
        prediction = "Safe"
    
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
