#!/usr/bin/env python3

import os
import sys
import re
import matplotlib.pyplot as plt

def parse_rtt(stats_path):
    """Extract the 95th‑percentile one‑way delay (RTT) from a stats log."""
    with open(stats_path) as f:
        for line in f:
            # match Pantheon’s wording for 95th‑pct delay
            m = re.search(r'95th[- ]percentile.*delay: ([\d\.]+) ms', line)
            if m:
                return float(m.group(1))
    return None

def main(exp_dir):
    schemes = ['cubic', 'bbr', 'vegas']
    rtts = []

    for cc in schemes:
        stats = os.path.join(exp_dir, f"{cc}_stats_run1.log")
        if not os.path.exists(stats):
            print(f"⚠️  Missing stats log for {cc}: {stats}")
            rtts.append(0)
            continue

        val = parse_rtt(stats)
        if val is None:
            print(f"⚠️  Couldn't parse RTT in {stats}")
            rtts.append(0)
        else:
            print(f"{cc}: 95th‑pct RTT = {val:.3f} ms")
            rtts.append(val)

    # plot
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(schemes, rtts, width=0.6)
    ax.set_ylabel("95th‑percentile RTT (ms)")
    ax.set_title(f"95th‑Percentile RTT — {os.path.basename(exp_dir)}")
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    out = os.path.join(exp_dir, "rtt_95pct_bar.png")
    fig.savefig(out, dpi=300)
    print(f"Wrote {out}")
    plt.show()

if __name__=="__main__":
    if len(sys.argv)!=2:
        print("Usage: plot_rtt_bar.py <experiment-dir>")
        sys.exit(1)
    main(sys.argv[1])
