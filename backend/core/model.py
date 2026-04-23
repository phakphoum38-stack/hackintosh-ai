# backend/core/model.py

import torch
import torch.nn as nn

class BootModel(nn.Module):

    def __init__(self):
        super(BootModel, self).__init__()

        self.net = nn.Sequential(
            nn.Linear(3, 16),   # ACPI / GPU / USB
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()        # output 0-1 (boot success probability)
        )

    def forward(self, x):
        return self.net(x)
