# -*- coding: utf-8 -*-
"""dl676.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/136NaUAXHxywuXm_E0f7gk5vtoC4p2bQQ
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader, random_split

# Define the FNN model
class FNN(nn.Module):
    def __init__(self):
        super(FNN, self).__init__()
        self.hidden1 = nn.Linear(784, 256)
        self.hidden2 = nn.Linear(256, 256)
        self.hidden3 = nn.Linear(256, 256)
        self.output = nn.Linear(256, 10)

    def forward(self, x):
        x = torch.relu(self.hidden1(x))
        x = torch.relu(self.hidden2(x))
        x = torch.relu(self.hidden3(x))
        x = self.output(x)
        return torch.softmax(x, dim=1)

# Load the MNIST dataset
dataset = MNIST(root='data/', train=True, transform=ToTensor(), download=True)
train_dataset, val_dataset = random_split(dataset, [50000, 10000])

# Create data loaders for training and validation
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=64)

# Initialize the FNN model
model = FNN()

# Define the optimizer and loss function
optimizer = optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.CrossEntropyLoss()

# Train the model
epochs = 10
for epoch in range(epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        # Flatten the input data
        data = data.view(-1, 784)

        # Zero the gradients
        optimizer.zero_grad()

        # Forward pass
        output = model(data)

        # Compute the loss
        loss = loss_fn(output, target)

        # Backward pass
        loss.backward()

        # Update the parameters
        optimizer.step()

        # Print the loss and accuracy for the current batch
        if batch_idx % 100 == 0:
            with torch.no_grad():
                # Compute the accuracy on the validation set
                val_loss = 0
                val_acc = 0
                for val_data, val_target in val_loader:
                    # Flatten the input data
                    val_data = val_data.view(-1, 784)

                    # Forward pass
                    val_output = model(val_data)

                    # Compute the loss
                    val_loss += loss_fn(val_output, val_target).item()

                    # Compute the accuracy
                    _, pred = torch.max(val_output, dim=1)
                    val_acc += torch.sum(pred == val_target).item()

                val_loss /= len(val_loader)
                val_acc /= len(val_dataset)

                print(f'Epoch {epoch}, Batch {batch_idx}: Loss={loss.item():.4f}, Val_Loss={val_loss:.4f}, Val_Accuracy={val_acc:.4f}')
                
                //reference: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
                        
