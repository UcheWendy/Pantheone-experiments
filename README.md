Note: This top‑level README describes my experiment setup. Pantheon’s original documentation (including its own README.md) remains in src/README.md and should be kept intact
# Pantheon Congestion Control Experiments

This repository contains a set of experiments comparing three congestion-control algorithms (Cubic, BBR, and Vegas) using the Pantheon test harness and Mahimahi network emulation.

## Repository Structure
```
pantheon/
├── data/                 # Experiment outputs
│   ├── experiment-1      # 60 Mb/s, 10 ms RTT results
│   ├── experiment-2      # 2 Mb/s, 200 ms RTT results
│   └── setup-test        # Initial setup test data
├── tests/                # Mahimahi trace files & test utilities
│   ├── *.trace           # Bandwidth–delay profiles for Mahimahi
│   ├── context.py        # Test runner context definitions
│   ├── local_test.py     # Local test harness script
│   ├── remote_test.py    # Remote test harness script
│   ├── test_analyze.py   # Script to parse logs and summarize data
│   └── test_schemes.py   # Scheme selection helper
├── combine_throughput.py # Plot throughput over time for all schemes
├── combine_loss.py       # Plot loss over time for all schemes
├── plot_rtt_bar.py       # Generate 95th‑pct RTT bar charts
├── README.md             # This file
└── src/                  # Pantheon source code and wrappers
    ├── experiments/      # Pantheon’s experiment runner scripts
    ├── analysis/         # Custom analysis modules and scripts
    └── helpers/          # Utility modules used by wrappers and analysis
```

## Prerequisites


- Ubuntu 18.04 LTS (in a VM or bare metal)
- Python 2.7 for Pantheon wrappers
- Python 3.8+ for analysis scripts
- Mahimahi v2.7 (built and installed from source)
- Git
- `matplotlib`, `numpy` (install via `python3 -m pip install matplotlib numpy`)

## Setup

1. **Clone Pantheon** and this repo:
   ```bash
   git clone https://github.com/StanfordSNR/pantheon.git
   git clone https://github.com/UcheWendy/Pantheone-experiments.git
   cd Pantheone-experiments/pantheon
   ```
2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install -y build-essential python2.7 python2-pip python3 python3-pip libcap2-bin libsqlite3-dev
   # Mahimahi dependencies
   sudo apt install -y git autoconf automake libtool libsqlite3-dev
   # Install Python3 libraries
   python3 -m pip install matplotlib numpy
   ```
3. **Build Mahimahi** (from source if needed) and ensure `mm-link` is available.

## Generating Traces

Create the Mahimahi trace files under `tests/`:

```bash
# 60 Mb/s, 10 ms RTT
for i in $(seq 1 60); do echo 60; done > tests/60mbps.trace
# 2 Mb/s, 200 ms RTT
for i in $(seq 1 200); do echo 2; done > tests/2mbps.trace
```

## Running Experiments

Launch each 60 s experiment with all three schemes:

```bash
# Experiment 1: 60 Mb/s, 10 ms RTT
src/experiments/test.py local \
  --schemes "cubic bbr vegas" \
  --runtime 60 \
  --uplink-trace tests/60mbps.trace \
  --downlink-trace tests/60mbps.trace \
  --data-dir data/experiment-1

# Experiment 2: 2 Mb/s, 200 ms RTT
src/experiments/test.py local \
  --schemes "cubic bbr vegas" \
  --runtime 60 \
  --uplink-trace tests/2mbps.trace \
  --downlink-trace tests/2mbps.trace \
  --data-dir data/experiment-2
```

## Generating Plots

Run the custom analysis scripts:

```bash
# Throughput over time
python3 src/analysis/combine_throughput.py data/experiment-1
python3 src/analysis/combine_throughput.py data/experiment-2

# Loss over time
python3 src/analysis/combine_loss.py data/experiment-1
python3 src/analysis/combine_loss.py data/experiment-2

# 95th‑percentile RTT bar chart
python3 src/analysis/plot_rtt_bar.py data/experiment-1
python3 src/analysis/plot_rtt_bar.py data/experiment-2

# RTT vs Throughput scatter
cp data/experiment-1/pantheon_summary_mean.svg data/experiment-1/exp1_rtt_vs_throughput.svg
cp data/experiment-2/pantheon_summary_mean.svg data/experiment-2/exp2_rtt_vs_throughput.svg
```

## Results

Each `data/experiment-*` directory contains:

- `combined_throughput_time.png`
- `combined_loss_time.png`
- `rtt_95pct_bar.png`
- `exp?_rtt_vs_throughput.svg`

Embed these graphs in your report to compare protocol performance under each network profile.

## License

This work is released under the MIT License. Feel free to reuse or adapt these scripts for your own research.