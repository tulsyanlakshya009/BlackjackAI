from blackjack import BlackjackGame
from cards import Deck
from blackjack_ai import BlackjackAI
from blackjack_baseline import BaselineModel

deck=Deck()

def simulate_hand(ai: BlackjackAI, train=True):
    """
    Simulate a single hand of blackjack using the AI
    """
    global deck
    game = BlackjackGame(deck, chips=500)

    # choosing bet
    deck_probs = deck.get_remaining_probabilities()
    bet = ai.choose_bet(deck_probs)
    bet = min(bet, game.chips)
    game.place_bet(bet)

    # initial deal after bet
    game.deal_initial()
    player_total = game.calculate_score(game.player_hand)
    dealer_card_val = game.dealer_hand[0].value

    state = ai.get_state(player_total, dealer_card_val, deck.get_remaining_probabilities(), bet)

    # player's turn
    while True:
        action = ai.choose_action(state)
        if action == 'hit':
            game.hit(game.player_hand)
            new_total = game.calculate_score(game.player_hand)
            if new_total > 21:
                reward = -bet
                if train:
                    ai.update(state, action, reward)
                return reward
            next_state = ai.get_state(new_total, dealer_card_val, deck.get_remaining_probabilities(), bet)
            if train:
                ai.update(state, action, 0, next_state)
            state = next_state
        else:
            break

    # dealer's turn
    while game.calculate_score(game.dealer_hand) < 17:
        game.hit(game.dealer_hand)

    result = game.check_winner()
    if result == "Player wins":
        reward = int(bet * 1.5)  
    elif result == "Draw":
        reward = 0
    else:
        reward = -bet

    if train:
        ai.update(state, action, reward)

    return reward

def simulate_baseline_hand(baseline: BaselineModel):
    """
    Simulate a single hand of blackjack using the baseline strategy
    """
    deck = Deck()
    game = BlackjackGame(deck, chips=500)

    # fixed bet
    bet = baseline.get_bet()
    game.place_bet(bet)

    # initial deal after bet
    game.deal_initial()
    player_total = game.calculate_score(game.player_hand)
    dealer_card_val = game.dealer_hand[0].value

    # player's turn
    while True:
        action = baseline.get_action(player_total, dealer_card_val)
        if action == 'hit':
            game.hit(game.player_hand)
            new_total = game.calculate_score(game.player_hand)
            if new_total > 21:
                return -bet
            player_total = new_total
        else:
            break

    # dealer's turn
    while game.calculate_score(game.dealer_hand) < 17:
        game.hit(game.dealer_hand)

    result = game.check_winner()
    if result == "Player wins":
        return int(bet * 1.5)
    elif result == "Draw":
        return 0
    else:
        return -bet

def print_results(label, results):
    """
    print the results of the simulation
    """
    total_profit = sum(results)
    wins = sum(1 for r in results if r > 0)
    draws = sum(1 for r in results if r == 0)
    losses = sum(1 for r in results if r < 0)
    
    print(f"\n{label} Results:")
    print("--------------------")
    print(f"Total Profit:         {total_profit}")
    print(f"Average Profit per Hand: {total_profit / len(results):.2f}")
    print(f"Win Rate:              {wins / len(results) * 100:.2f}%")
    print(f"Draw Rate:            {draws / len(results) * 100:.2f}%")
    print(f"Loss Rate:            {losses / len(results) * 100:.2f}%")

def main():
    """
    main function
    """
    # initialize models
    ai = BlackjackAI()
    baseline = BaselineModel()
    
    # training ai
    total_training_hands = 500000
    print("Training AI model...")
    
    for i in range(total_training_hands):
        simulate_hand(ai, train=True)
        ai.decay_epsilon()
        if (i + 1) % 50000 == 0:
            print(f"Completed {i + 1} hands")

    ai.save_model()
    
    # testing phase
    test_hands = 100000
    print(f"\nTesting both models on {test_hands} hands each...")
    
    # test AI model
    ai.epsilon = 0.0  # Disable exploration
    ai_results = [simulate_hand(ai, train=False) for _ in range(test_hands)]
    
    # test Baseline model
    baseline_results = [simulate_baseline_hand(baseline) for _ in range(test_hands)]
    
    # print results
    print("\n=== Final Test Results ===")
    print("-"*75)
    print(f"| {'Metric':<25} | {'AI Model':<20} | {'Baseline':<20} | ")
    print("-"*75)

    ai_profit = sum(ai_results)
    baseline_profit = sum(baseline_results)
    print(f"| {'Total Profit':<25} | {ai_profit:20,} | {baseline_profit:20,} | ")

    ai_avg = ai_profit / test_hands
    baseline_avg = baseline_profit / test_hands
    print(f"| {'Avg Profit/Hand':<25} | {ai_avg:20.2f} | {baseline_avg:20.2f} | ")

    ai_wins = sum(1 for r in ai_results if r > 0)
    baseline_wins = sum(1 for r in baseline_results if r > 0)
    print(f"| {'Win Rate':<25} | {ai_wins/test_hands*100:19.2f}% | {baseline_wins/test_hands*100:19.2f}% | ")

    ai_draws = sum(1 for r in ai_results if r == 0)
    baseline_draws = sum(1 for r in baseline_results if r == 0)
    print(f"| {'Draw Rate':<25} | {ai_draws/test_hands*100:19.2f}% | {baseline_draws/test_hands*100:19.2f}% | ")

    ai_losses = sum(1 for r in ai_results if r < 0)
    baseline_losses = sum(1 for r in baseline_results if r < 0)
    print(f"| {'Loss Rate':<25} | {ai_losses/test_hands*100:19.2f}% | {baseline_losses/test_hands*100:19.2f}% | ")
    print("-"*75)

if __name__ == "__main__":
    main()