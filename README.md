# Reinforcement Learning–Based Blackjack AI

This repository contains a complete implementation of a Blackjack AI using tabular Q-learning, dynamic bet-sizing based on card-count probabilities, and a Tkinter GUI for interactive play and real-time AI suggestions.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🗂 Repository Structure](#-repository-structure)
- [🔧 Requirements](#-requirements)
- [🚀 Installation](#-installation)
- [🏃 Usage](#-usage)
  - [Training & Testing the AI](#training--testing-the-ai)
  - [Running the GUI](#running-the-gui)
- [🧠 Algorithms](#-algorithms)
  - [MDP Formulation](#mdp-formulation)
  - [Q-Learning Agent](#q-learning-agent)
  - [Bet-Sizing Heuristic](#bet-sizing-heuristic)
  - [Baseline Agent](#baseline-agent)
- [📊 Results](#-results)

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
└── README.md             # Project overview and usage
```

---

## 🔧 Requirements

- Python 3.8+
- Packages:
  - `numpy`
  - `pillow`
  - `reportlab`

Install via:
```bash
pip install numpy pillow reportlab
```

---

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/tulsyanlakshya009/BlackjackAI.git
cd BlackjackAI
```

---

## 🏃 Usage

### Training & Testing the AI

AI is trained over 500,000 hands and tested on 100,000 hands:
```bash
python train_blackjack_ai.py
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
  `Q(s, a) ← Q(s, a) + α [r + γ * maxₐ′ Q(s′, a′) – Q(s, a)]`
- α = 0.05, γ = 0.95
- ε-greedy exploration: ε decays from 1.0 -> 0.05

### Bet-Sizing Heuristic

Choose a bet based on the remaining card probabilities:

1. Bet 100 if high > 0.37
2. Bet 80 if high > 0.3
3. Bet 60 if mid > 0.4
4. Bet 40 if low > 0.4
5. Else, pick random: 10–70


### Baseline Agent

- Fixed bet = 10
- Hit if `player_total <= 16`, stand if >= 17

---

## 📊 Results

| Metric           | AI Model     | Baseline    |
|------------------|--------------|-------------|
| Total Profit     | 1,265,025    | 159,870     |
| Avg Profit/Hand  | 12.65        | 1.60        |
| Win Rate         | 42.13%       | 42.74%      |
| Draw Rate        | 8.59%        | 9.14%       |
| Loss Rate        | 49.28%       | 48.12%      |



