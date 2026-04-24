import torch
from torch.utils.data import DataLoader, TensorDataset
from backend.core.model import BootModel
from backend.core.dataset import load_dataset

def train():

    data = load_dataset()

    if len(data) < 10:
        print("Not enough data")
        return

    # ----------------------------
    # DEBUG: ดูข้อมูลก่อน
    # ----------------------------
    print("Sample data:", data[0])

    # ----------------------------
    # สร้าง X / y แบบกันพัง
    # ----------------------------
    try:
        X = torch.tensor([list(d["x"]) for d in data], dtype=torch.float32)
    except Exception as e:
        raise ValueError(
            "❌ X format error: d['x'] must be list/array, not empty or scalar"
        ) from e

    y = torch.tensor([d["y"] for d in data], dtype=torch.float32).view(-1, 1)

    print("X shape:", X.shape)
    print("y shape:", y.shape)

    # ----------------------------
    # กันเคส feature ว่าง (ปัญหาที่คุณเจอ)
    # ----------------------------
    if X.shape[1] == 0:
        raise ValueError("❌ X has 0 features. Check load_dataset() preprocessing")

    dataset = TensorDataset(X, y)
    loader = DataLoader(dataset, batch_size=8, shuffle=True)

    model = BootModel(input_dim=X.shape[1])  # 🔥 แก้ให้ dynamic

    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = torch.nn.BCELoss()

    for epoch in range(20):
        total_loss = 0

        for xb, yb in loader:

            pred = model(xb)

            # กัน shape error
            pred = pred.view_as(yb)

            loss = loss_fn(pred, yb)

            opt.zero_grad()
            loss.backward()
            opt.step()

            total_loss += loss.item()

        print(f"epoch {epoch} loss {total_loss/len(loader):.4f}")

    torch.save(model.state_dict(), "models/latest.pth")
