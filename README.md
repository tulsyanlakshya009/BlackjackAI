# Reinforcement Learning–Based Blackjack AI

This repository contains a complete implementation of a Blackjack AI using tabular Q-learning, dynamic bet-sizing based on card-count probabilities, and a Tkinter GUI for interactive play and real-time AI suggestions.

---

## 📋 Table of Contents

- [Features](#features)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Training the AI](#training-the-ai)
  - [Testing the AI](#testing-the-ai)
  - [Running the GUI](#running-the-gui)
- [Algorithms](#algorithms)
  - [MDP Formulation](#mdp-formulation)
  - [Q-Learning Agent](#q-learning-agent)
  - [Bet-Sizing Heuristic](#bet-sizing-heuristic)
  - [Baseline Agent](#baseline-agent)
- [Results](#results)
- [Future Work](#future-work)
- [License](#license)

---

## ✨ Features

- **Blackjack Simulator**: Implements standard rules, persistent multi-deck shoe with automatic reshuffle.
- **Q-Learning Agent**: Learns hit/stand policy using ε-greedy exploration and dynamic ε-decay.
- **Dynamic Bet-Sizing**: Maps card-count probabilities (low/mid/high) to bets (10–100) via a damped linear ramp.
- **Baseline Rule-Based Agent**: Simple strategy for benchmarking.
- **Tkinter GUI**: Play interactively, see AI's suggested action and bet in real time.

---

## 🗂 Repository Structure

```
├── cards.py              # Card & Deck classes for shoe management
├── blackjack.py          # Game logic (deal, hit, score, check_winner)
├── blackjack_ai.py       # Q-learning agent & bet-sizing strategy
├── blackjack_baseline.py # Rule-based baseline agent
├── train_blackjack_ai.py # Training & testing harness (persistent deck)
├── blackjackgui.py       # Tkinter GUI with AI integration
├── requirements.txt      # Python dependencies
└── README.md             # Project overview and usage
```

---

## 🔧 Requirements

- Python 3.8+
- Packages listed in `requirements.txt`:
  - `numpy`
  - `pillow`
  - `reportlab` (for PDF generation, optional)

Install via:
```bash
pip install -r requirements.txt
```

---

## 🚀 Installation

1. Clone this repository:
   ```bash
git clone https://github.com/your-username/blackjack-ai.git
cd blackjack-ai
```
2. Install dependencies:
   ```bash
pip install -r requirements.txt
```

---

## 🏃 Usage

### Training the AI

Run the training script to train over 500,000 hands:
```bash
python train_blackjack_ai.py --train --episodes 500000 --save_model
```
- **Options**:
  - `--train`: enable training mode
  - `--episodes N`: number of simulated hands
  - `--save_model`: saves Q-table to `blackjack_q_table.pkl`

### Testing the AI

After training (or loading a saved model), evaluate over 100,000 hands:
```bash
python train_blackjack_ai.py --test --episodes 100000 --load_model blackjack_q_table.pkl
```

### Running the GUI

Launch the interactive GUI:
```bash
python blackjackgui.py
```
- Use the radio buttons to switch between **AI** and **Baseline**.
- Enter a bet and click **Bet** to start.
- The AI panel displays suggested bet, action, and deck composition percentages.

---

## 🧠 Algorithms

### MDP Formulation

- **State**: `(player_total, dealer_up, low_prob, mid_prob, high_prob, bet)`
- **Actions**: `hit` or `stand`
- **Reward**: +1.5×bet on win, 0 on draw, –1×bet on loss

### Q-Learning Agent

- Tabular Q-learning with update:
  \(Q(s,a) ← Q(s,a) + α [r + γ max_{a'} Q(s',a') – Q(s,a)]\)
- α = 0.05, γ = 0.95
- ε-greedy exploration: ε decays from 1.0 → 0.05

### Bet-Sizing Heuristic

1. Compute `low`, `mid`, `high` probabilities from deck
2. Raw advantage: `adv_raw = high – low`
3. Damped: `adv_adj = adv_raw × (1 – mid)` to account for neutral 7–9’s
4. Normalize to [0,1], then linearly scale to [10,100]
5. Round to nearest multiple of 10

### Baseline Agent

- Fixed bet = 10
- Hit if `player_total ≤ 16`, stand if ≥ 17

---

## 📊 Results


