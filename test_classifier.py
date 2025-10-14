import pickle

with open("model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)

emails = [
    "You won a free iPhone, click here!",
    "Project meeting at 3pm"
]

for e in emails:
    X = vectorizer.transform([e])
    print(e, "→", model.predict(X)[0])
