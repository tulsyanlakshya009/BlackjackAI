class BlackjackGame:
    """
    Represents a blackjack game.
    """
    def __init__(self, deck, chips=500):
        """
        Initializes a new blackjack game.
        """
        self.deck = deck
        self.player_hand = []
        self.dealer_hand = []
        self.chips = chips
        self.bet = 0
        self.game_over = False

    def place_bet(self, amount):
        """
        Places a bet for the current hand.
        """
        if 0 < amount <= min(100, self.chips):
            self.bet = amount
            self.chips -= amount
            return True
        return False

    def deal_initial(self):
        """
        Deals the initial cards to the player and dealer.
        """
        self.player_hand = [self.deck.deal(), self.deck.deal()]
        self.dealer_hand = [self.deck.deal(), self.deck.deal()]

    def hit(self, hand):
        """
        Deals a card to a player's hand.
        """
        hand.append(self.deck.deal())

    def calculate_score(self, hand):
        """
        Calculates the score of a player's hand.
        """
        score = sum(card.value for card in hand)
        aces = sum(1 for card in hand if card.rank == 'ace')
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def check_winner(self):
        """
        Checks the winner of the current hand.
        """
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        if player_score > 21:
            return "Dealer wins"
        elif dealer_score > 21 or player_score > dealer_score:
            self.chips += self.bet * 2
            return "Player wins"
        elif dealer_score == player_score:
            self.chips += self.bet  # Push
            return "Draw"
        else:
            return "Dealer wins"
