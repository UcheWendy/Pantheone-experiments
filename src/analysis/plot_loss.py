#!/usr/bin/env python3
import json
import os
import matplotlib.pyplot as plt

# 1) Tell me where your perf JSON lives:
#    adjust this path to point at YOUR experiment folder
perf_path = 'data/experiment-1/pantheon_perf.json'
if not os.path.exists(perf_path):
    raise FileNotFoundError(f"{perf_path} not found")

# 2) Load the JSON
with open(perf_path) as f:
    perf = json.load(f)

# 3) Extract schemes and their loss rates
schemes    = list(perf.keys())
loss_rates = [perf[s]['all']['loss'] * 100 for s in schemes]

# 4) Make a bar chart
plt.figure(figsize=(6,4))
plt.bar(schemes, loss_rates)
plt.ylabel('Loss rate (%)')
plt.title('Loss Rate by Congestion Control Scheme')
plt.ylim(0, max(loss_rates)*1.2)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# 5) Save & show
plt.savefig('loss_rate_comparison.png', dpi=300)
plt.show()
