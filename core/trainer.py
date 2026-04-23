import torch
from torch.utils.data import DataLoader, TensorDataset
from core.model import BootModel
from core.dataset import load_dataset

def train():

    data = load_dataset()

    if len(data) < 10:
        print("Not enough data")
        return

    X = torch.tensor([d["x"] for d in data], dtype=torch.float32)
    y = torch.tensor([d["y"] for d in data], dtype=torch.float32).view(-1, 1)

    dataset = TensorDataset(X, y)
    loader = DataLoader(dataset, batch_size=8, shuffle=True)

    model = BootModel()

    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = torch.nn.BCELoss()

    for epoch in range(20):

        for xb, yb in loader:

            pred = model(xb)
            loss = loss_fn(pred, yb)

            opt.zero_grad()
            loss.backward()
            opt.step()

        print(f"epoch {epoch} loss {loss.item()}")

    torch.save(model.state_dict(), "models/latest.pth")
