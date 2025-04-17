#!/usr/bin/env python3

# Monkey‑patch Python2's xrange for TunnelGraph.parse_tunnel_log:
import builtins
builtins.xrange = range

import os
import sys

# Ensure Python can find the Pantheon modules
root = os.getcwd()
sys.path.insert(0, os.path.join(root, 'src'))
sys.path.insert(0, os.path.join(root, 'src', 'helpers'))
sys.path.insert(0, os.path.join(root, 'src', 'analysis'))

import context
context.base_dir = root

import matplotlib.pyplot as plt
from analysis.tunnel_graph import TunnelGraph

def main(exp_dir):
    # define the three schemes in the order you want them drawn
    schemes = ['bbr', 'vegas', 'cubic']
    # styling: color, linestyle, marker
    styles = {
        'cubic': ('blue',   '-',  'o'),
        'bbr':   ('orange', '--', 's'),
        'vegas': ('red',  ':',  '^'),
    }

    plt.figure(figsize=(8,4))

    for cc in schemes:
        # try the "mm_" log first, then fallback
        log_mm  = os.path.join(exp_dir, f"{cc}_mm_datalink_run1.log")
        log_std = os.path.join(exp_dir, f"{cc}_datalink_run1.log")
        if os.path.exists(log_mm):
            log = log_mm
        elif os.path.exists(log_std):
            log = log_std
        else:
            print(f"⚠️  No datalink log for {cc}")
            continue

        # parse
        tg = TunnelGraph(tunnel_log=log, throughput_graph=None, delay_graph=None)
        tg.parse_tunnel_log()
        t = tg.egress_t[0]
        y = tg.egress_tput[0]

        # debug print to verify values
        if cc == 'cubic':
            print("First 5 cubic throughputs:", [f"{v:.2f}" for v in y[:5]])
        if cc == 'vegas':
            print("First 5 vegas throughputs:", [f"{v:.2f}" for v in y[:5]])

        # plot with distinct style
        color, ls, marker = styles[cc]
        plt.plot(
            t, y,
            label=cc,
            color=color,
            linestyle=ls,
            marker=marker,
            markevery=max(1, len(t)//10),
            linewidth=2,
            alpha=0.8
        )

    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (Mbit/s)")
    plt.title(f"Throughput Over Time — {os.path.basename(exp_dir)}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    out = os.path.join(exp_dir, "combined_throughput_time.png")
    plt.savefig(out, dpi=300)
    print(f"Wrote {out}")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: combine_throughput.py <experiment-dir>")
        sys.exit(1)
    main(sys.argv[1])
