import torch
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# -------------------------
# 1. Grab the boston housing CSV from kaggle
# -------------------------

import pandas as pd

# Load from GitHub
url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
df = pd.read_csv(url)

X = df.drop("medv", axis=1).values   # features
y = df["medv"].values.reshape(-1, 1) # target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Standardize
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert to tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)
# -------------------------
# 2. Define the net
# -------------------------
import torch.nn as nn

class HousingNet(nn.Module):
    def __init__(self):
        super().__init__()
        #Defining a feedforward nn.
        #13 -> 128 -> 64 -> 1
        self.net = nn.Sequential(
            nn.Linear(13, 128),
            nn.Tanh(), #Activation Function
            nn.Dropout(0.3), #Dropout to help with overfitting
            nn.Linear(128, 64),
            nn.ReLU(), #Activation Function
            nn.Dropout(0.3),  # Dropout to help with overfitting
            nn.Linear(64, 1)
            )

    def forward(self, x):
        return self.net(x)

model = HousingNet()

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01) #loss rate of 0.01

epochs = 200
for epoch in range(epochs):
    model.train() #Put model in training mode
    optimizer.zero_grad() #clear previous gradients, using optimizer here too
    y_pred = model(X_train) #Forward pass
    loss = criterion(y_pred, y_train) #calculate loss
    loss.backward() #compute gradients and back propagate
    optimizer.step() #update weights

    #Check performance every 20 epochs on test set
    if epoch % 20 == 0:
        model.eval()
        with torch.no_grad():
            test_pred = model(X_test)
            test_loss = criterion(test_pred, y_test)
        print(f"Epoch {epoch:03d}: train_loss={loss.item():.4f}, test_loss={test_loss.item():.4f}")

# -------------------------
# 5. Evaluate loss
# -------------------------


model.eval()
with torch.no_grad():
    preds = model(X_test).numpy()

r2 = r2_score(y_test.numpy(), preds)
print(f"R² Score: {r2:.3f}")
