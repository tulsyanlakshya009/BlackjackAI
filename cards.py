import random

SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

class Card:
    """
    Represents a playing card.
    """
    def __init__(self, suit, rank):
        """
        Initializes a card with a suit and rank.
        """
        self.suit = suit
        self.rank = rank
        self.value = self._get_value()

    def _get_value(self):
        """
        Returns the value of the card based on its rank.
        """
        if self.rank in ['jack', 'queen', 'king']:
            return 10
        elif self.rank == 'ace':
            return 11
        return int(self.rank)

    def filename(self):
        """
        Returns the filename of the card image.
        """
        suit_map = {'clubs': '1', 'spades': '2', 'diamonds': '3', 'hearts': '4'}
        rank_map = {
            'ace': '1', '2': '2', '3': '3', '4': '4', '5': '5', 
            '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
            'jack': '11', 'queen': '12', 'king': '13'
        }
        suit_num = suit_map[self.suit]
        rank_num = rank_map[self.rank]
        return f"card_{suit_num}{rank_num}.gif"

class Deck:
    """
    Represents a deck of cards.
    """
    def __init__(self):
        """
        Initializes the deck.
        """
        self.full_deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.cards = self.full_deck.copy()
        self.used_cards = []
        random.shuffle(self.cards)

    def deal(self):
        """
        Deals a card from the deck.
        """
        if len(self.cards) < 15:
            self.cards += self.used_cards
            self.used_cards = []
            random.shuffle(self.cards)
        card = self.cards.pop()
        self.used_cards.append(card)
        return card

    def shuffle(self):
        """
        Shuffles the deck.
        """
        self.cards = self.full_deck.copy()
        self.used_cards = []
        random.shuffle(self.cards)

    def get_remaining_probabilities(self):
        """
        Returns the probabilities of each card value remaining in the deck.
        """
        total = len(self.cards)
        value_counts = {v: 0 for v in range(2, 12)}
        for card in self.cards:
            value_counts[card.value] += 1
        return {k: v / total for k, v in value_counts.items()}
