import torch
from backend.core.model import BootModel
from backend.core.dataset import load_dataset

def train():

    data = load_dataset()

    # ------------------------
    # FIX: บังคับ x = 3 features
    # ------------------------
    X = []
    for d in data:
        x = list(d["x"])

        if len(x) < 3:
            x += [0] * (3 - len(x))
        else:
            x = x[:3]

        X.append(x)

    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor([d["y"] for d in data], dtype=torch.float32).view(-1, 1)

    print("X shape:", X.shape)  # ต้องเป็น (N, 3)

    # ------------------------
    # Model
    # ------------------------
    model = BootModel()

    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = torch.nn.BCELoss()

    # ------------------------
    # Train
    # ------------------------
    for epoch in range(20):

        pred = model(X)
        loss = loss_fn(pred, y)

        opt.zero_grad()
        loss.backward()
        opt.step()

        print("epoch", epoch, "loss", loss.item())

    torch.save(model.state_dict(), "models/latest.pth")


if __name__ == "__main__":
    train()
