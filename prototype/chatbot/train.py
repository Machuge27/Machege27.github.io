import numpy as np
import random
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nltk_utils import bag_of_words, tokenize, stem
from model import NeuralNet

with open("intents.json", "r") as name:
    intents = json.load(name)

our_words = []
mytags = []
mine = []
# looping through each sentence in our intents patterns
for intent in intents["intents"]:
    mytag = intent["mytag"]
    # adding to mytag list
    mytags.append(mytag)
    for pattern in intent["patterns"]:
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # adding to our words list
        our_words.extend(w)
        # adding to mine pair
        mine.append((w, mytag))

# stem and lower each word
our_ignored_words = ["?", ".", "!"]
our_words = [stem(w) for w in our_words if w not in our_ignored_words]
# remove duplicates and sort
our_words = sorted(set(our_words))
mytags = sorted(set(mytags))

print(len(mine), "patterns")
print(len(mytags), "mytags:", mytags)
print(len(our_words), "unique stemmed words:", our_words)

# creating our training data
value_train = []
othervalue_train = []
for pattern_sentence, mytag in mine:
    # X: bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, our_words)
    value_train.append(bag)
    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = mytags.index(mytag)
    othervalue_train.append(label)

value_train = np.array(value_train)
othervalue_train = np.array(othervalue_train)

# Hyper-parameters
our_epochs = 1000
batch_size = 8
learning_rate = 0.001
our_input_size = len(value_train[0])
hidden_size = 8
our_output_size = len(mytags)
print(our_input_size, our_output_size)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(value_train)
        self.x_data = value_train
        self.y_data = othervalue_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples


dataset = ChatDataset()
our_our_train_loader = DataLoader(
    dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = NeuralNet(our_input_size, hidden_size, our_output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(our_epochs):
    for words, labels in our_our_train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f"Epoch [{epoch+1}/{our_epochs}], Loss: {loss.item():.4f}")


print(f"Last loss: {loss.item():.4f}")

data = {
    "model_state": model.state_dict(),
    "our_input_size": our_input_size,
    "hidden_size": hidden_size,
    "our_output_size": our_output_size,
    "our_words": our_words,
    "mytags": mytags,
}

FILE = "data.pth"
torch.save(data, FILE)
# we complete our training
print(f"training complete. file saved to {FILE}")
