class BaselineModel:
    """Simple baseline model that follows basic blackjack strategy"""
    
    @staticmethod
    def get_action(player_total, dealer_card_value):
        """
        Returns the optimal action based on basic blackjack strategy
        """
        # always stand on 17 or higher
        if player_total >= 17:
            return "stand"
        
        # stand on 13-16 if dealer has weak card (2-6)
        elif player_total >= 13:
            if dealer_card_value <= 6:
                return "stand"
            else:
                return "hit"
        
        # special case for 12
        elif player_total == 12:
            if 4 <= dealer_card_value <= 6:
                return "stand"
            else:
                return "hit"
        
        # always hit on 11 or lower
        else:
            return "hit"
    
    @staticmethod
    def get_bet():
        """
        Returns a fixed small bet amount for baseline strategy
        """
        return 10