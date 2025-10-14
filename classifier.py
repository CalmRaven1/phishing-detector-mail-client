import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample training data
emails = [
    ("Congratulations! You won a prize", "Phishing"),
    ("Click here to claim your reward", "Phishing"),
    ("Meeting tomorrow at 10am", "Safe"),
    ("Don't forget the project deadline", "Safe")
]

# Separate texts and labels
texts, labels = zip(*emails)

# Convert text to numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train a simple Naive Bayes classifier
model = MultinomialNB()
model.fit(X, labels)

# Save the model and vectorizer for later use
with open("model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("Classifier trained and saved!")
