# -*- coding: utf-8 -*-

import json
import random
import pickle
import gradio as gr

# Load saved model
with open("model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
vectorizer = data["vectorizer"]
le = data["label_encoder"]
intents = data["intents"]

def chatbot_response(message, history):
    X = vectorizer.transform([message])
    predicted = model.predict(X)[0]
    tag = le.inverse_transform([predicted])[0]

    # find correct response
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Sorry, I didn't understand that."

# Create Gradio Chat Interface
chatbot = gr.ChatInterface(
    fn=chatbot_response,
    title="Simple NLP Chatbot",
    description="A TF-IDF + Logistic Regression chatbot deployed using Gradio."
)

# Launch for HF Spaces
if __name__ == "__main__":
    chatbot.launch()

