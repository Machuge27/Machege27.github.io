import random
import json
import time
import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 10)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open("intents.json", "r") as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["our_input_size"]
hidden_size = data["hidden_size"]
output_size = data["our_output_size"]
our_words = data["our_words"]
mytags = data["mytags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"


def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, our_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = mytags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["mytag"]:
                return random.choice(intent["responses"])

    return "I do not understand..."


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break
        

        resp = get_response(sentence)
        print(resp)
        words = resp.split()
        for word in words:
            print(word, end=' ', flush=True)
            time.sleep(0.3)
            break
        
        engine.say(resp)
        engine.runAndWait()
