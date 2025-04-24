import random
import numpy as np
import pickle

class BlackjackAI:
    """
    Class representing the blackjack AI.
    """
    def __init__(self, epsilon=1.0, alpha=0.05, gamma=0.95, epsilon_min=0.05, epsilon_decay=0.999995):
        self.actions = ['hit', 'stand']
        self.bet_sizes = [i for i in range(10, 101, 10)]  
        self.q_table = {} 
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

    def decay_epsilon(self):
        """
        decreases the epsilon value over time.
        """
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_state(self, player_total, dealer_card, deck_probs, bet):
        """
        Returns a tuple representing the current state of the game. 
        """
        low = round(sum(deck_probs[v] for v in range(2, 7)), 1)
        mid = round(sum(deck_probs[v] for v in range(7, 10)), 1)
        high = round(sum(deck_probs[v] for v in range(10, 12)), 1)
        return (player_total, dealer_card, low, mid, high, bet)

    def choose_action(self, state):
        """
        Selects an action based on the current state and epsilon-greedy policy.
        """
        if state not in self.q_table:
            player_total, dealer_card, _, _, _, _ = state
            
            # bias based on player's total
            hit_bias = min(1.0, (21 - player_total)/21 * 2)  # favor hitting when far from 21
            stand_bias = 1 - (abs(player_total - 17)/17)      # favor standing near 17-21
            
            # adjust based on dealer's visibile card
            dealer_modifier = 1.0
            if dealer_card in [7, 8, 9, 10, 11]:  # dealer strong cards
                hit_bias *= 1.2
            elif dealer_card in [2, 3, 4, 5, 6]:  # dealer weak cards
                stand_bias *= 1.2
            
            # normalize and initialize
            total = hit_bias + stand_bias
            self.q_table[state] = [hit_bias/total, stand_bias/total]

        # epsilon-greedy policy
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return self.actions[np.argmax(self.q_table[state])]

    def choose_bet(self, deck_probs):
        """
        Determines a confident bet based on high/mid/low card probabilities.
        """
        low = sum(deck_probs[v] for v in range(2, 7))
        mid = sum(deck_probs[v] for v in range(7, 10))
        high = sum(deck_probs[v] for v in range(10, 12))

        if high > 0.37:
            return 100
        elif high > 0.3:
            return 80
        elif mid > 0.4:
            return 60
        elif low > 0.4:
            return 40
        else:
            return random.choice([10, 20, 30, 50, 70]) 

    def update(self, state, action, reward, next_state=None):
        """ 
        updates the q-table based on the current state, action, reward, and next state.
        """
        if state not in self.q_table:
            self.q_table[state] = [0.5, 0.5]
        if next_state and next_state not in self.q_table:
            self.q_table[next_state] = [0.5, 0.5]

        action_idx = self.actions.index(action)
        max_q_next = max(self.q_table[next_state]) if next_state else 0
        self.q_table[state][action_idx] += self.alpha * (reward + self.gamma * max_q_next - self.q_table[state][action_idx])

    def save_model(self, path="blackjack_q_table.pkl"):
        """
        saves the model
        """
        with open(path, "wb") as f:
            pickle.dump({
                "q_table": self.q_table,
                "epsilon": self.epsilon
            }, f)

    def load_model(self, path="blackjack_q_table.pkl"):
        """
        loads the model
        """
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.q_table = data["q_table"]
            self.epsilon = data.get("epsilon", 0.1)
