#!/usr/bin/env python3

# Monkey‑patch Python2's xrange for TunnelGraph.parse_tunnel_log:
import builtins
builtins.xrange = range

import os
import sys

# Ensure Python can find Pantheon modules
root = os.getcwd()
sys.path.insert(0, os.path.join(root, 'src'))
sys.path.insert(0, os.path.join(root, 'src', 'helpers'))
sys.path.insert(0, os.path.join(root, 'src', 'analysis'))

import context
context.base_dir = root

import matplotlib.pyplot as plt
from analysis.tunnel_graph import TunnelGraph

def main(exp_dir):
    # Draw schemes in this order so cubic plots on top
    schemes = ['bbr', 'vegas', 'cubic']
    styles = {
        'cubic': ('blue',   '-',  'o'),
        'bbr':   ('orange', '--', 's'),
        'vegas': ('green',  ':',  '^'),
    }

    plt.figure(figsize=(8,4))

    for cc in schemes:
        # Try "mm_" log first, then fallback to plain log
        log_mm  = os.path.join(exp_dir, f"{cc}_mm_datalink_run1.log")
        log_std = os.path.join(exp_dir, f"{cc}_datalink_run1.log")

        if os.path.exists(log_mm):
            log = log_mm
        elif os.path.exists(log_std):
            log = log_std
        else:
            print(f"⚠️  No datalink log for {cc} in {exp_dir}")
            continue

        print(f"Loading {cc} from {log}")
        tg = TunnelGraph(
            tunnel_log=log,
            throughput_graph=None,
            delay_graph=None
        )
        tg.parse_tunnel_log()

        # Arrivals (ingress) and departures (egress)
        in_t, in_p = tg.ingress_t[0],  tg.ingress_tput[0]
        eg_t, eg_p = tg.egress_t[0],   tg.egress_tput[0]

        # Compute instantaneous loss % per time bin
        loss = [((i-d)/i*100) if i>0 else 0 for i,d in zip(in_p, eg_p)]
        t_loss = eg_t[:len(loss)]
        print(f"{cc}: len(eg_t)={len(eg_t)}, len(loss)={len(loss)}")

        # Plot with distinct style
        color, ls, marker = styles[cc]
        plt.plot(
            t_loss,
            loss,
            label=cc,
            color=color,
            linestyle=ls,
            marker=marker,
            markevery=max(1, len(loss)//10),
            linewidth=2,
            alpha=0.8
        )

    plt.xlabel("Time (s)")
    plt.ylabel("Loss rate (%)")
    plt.title(f"Loss Over Time — {os.path.basename(exp_dir)}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    out = os.path.join(exp_dir, "combined_loss_time.png")
    plt.savefig(out, dpi=300)
    print(f"Wrote {out}")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: combine_loss.py <experiment-dir>")
        sys.exit(1)
    main(sys.argv[1])
