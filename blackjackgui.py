import tkinter as tk
from PIL import Image, ImageTk
import os
from cards import Card, Deck
from blackjack import BlackjackGame
from blackjack_ai import BlackjackAI
from blackjack_baseline import BaselineModel

CARD_WIDTH = 80
CARD_HEIGHT = 120

class BlackjackGUI:
    """
    GUI for the blackjack game with AI assistant.
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Blackjack with AI Assistant")
        self.window.geometry("1200x800")
        self.window.configure(bg="#054b25")

        # Initialize game
        self.deck = Deck()
        self.game = BlackjackGame(self.deck)
        
        # Load AI & Baseline models
        self.ai = BlackjackAI()
        self.baseline = BaselineModel()
        self.current_model = "ai"
        
        try:
            self.ai.load_model()
        except:
            print("No trained AI model found, using untrained version")

        self.card_images = {}
        self.load_images()

        button_style = {
            "font": ("Arial", 14, "bold"),
            "bg": "#333333",
            "activebackground": "#FFD700",
            "relief": "raised",
            "bd": 3,
            "padx": 15,
            "pady": 8,
            "highlightbackground": "black",
            "highlightthickness": 1
        }

        ai_panel_style = {
            "bg": "#1a1a1a",
            "bd": 2,
            "relief": "solid",
            "width": 280,
            "height": 400
        }

        bet_panel_style = {
            "bg": "#1a1a1a",
            "bd": 2,
            "relief": "solid",
            "width": 280,
            "height": 150
        }

        # ===== TOP AREA =====
        self.top_frame = tk.Frame(self.window, bg="#054b25")
        self.top_frame.pack(side="top", fill="x", pady=15, padx=15)

        # Chips
        self.chips_label = tk.Label(self.top_frame, text="Chips: 500", font=("Arial", 16, "bold"), bg="#054b25", fg="#FFD700")
        self.chips_label.pack(side="left", padx=20)

        # Model selection
        self.model_frame = tk.Frame(self.top_frame, bg="#054b25")
        self.model_frame.pack(side="left", padx=50)
        
        self.model_var = tk.StringVar(value="ai")
        tk.Radiobutton(self.model_frame, text="AI Model", variable=self.model_var, value="ai", command=self.switch_model, bg="#054b25", fg="white", selectcolor="#054b25", font=("Arial", 12)).pack(side="left")
        tk.Radiobutton(self.model_frame, text="Baseline", variable=self.model_var, value="baseline", command=self.switch_model, bg="#054b25", fg="white", selectcolor="#054b25", font=("Arial", 12)).pack(side="left", padx=20)

        self.bet_panel = tk.Frame(self.top_frame, **bet_panel_style)
        self.bet_panel.pack(side="right", padx=0, pady=10, fill="y")  
        self.bet_panel.pack_propagate(False)
        
        tk.Label(self.bet_panel, text="Place Your Bet", font=("Arial", 14, "bold"), fg="white", bg="#1a1a1a").pack(pady=5)

        self.bet_var = tk.IntVar(value=10)
        self.bet_entry = tk.Spinbox(self.bet_panel, from_=1, to=500, textvariable=self.bet_var, font=("Arial", 14), width=5, justify="center")
        self.bet_entry.pack(pady=5)

        self.bet_button = tk.Button(self.bet_panel, text="Bet", command=self.place_bet, **button_style)
        self.bet_button.pack(pady=5)

        # Main Game Area

        self.game_frame = tk.Frame(self.window, bg="#054b25")
        self.game_frame.pack(side="left", fill="both", expand=True)

        # Dealer area
        self.dealer_label = tk.Label(self.game_frame, text="DEALER", font=("Arial", 20, "bold"), bg="#054b25", fg="white")
        self.dealer_label.pack(pady=(30, 0))

        self.dealer_frame = tk.Frame(self.game_frame, bg="#054b25")
        self.dealer_frame.pack(pady=10)

        # Player area
        self.player_label = tk.Label(self.game_frame, text="PLAYER", font=("Arial", 20, "bold"), bg="#054b25", fg="white")
        self.player_label.pack(pady=(50, 0))

        self.player_frame = tk.Frame(self.game_frame, bg="#054b25")
        self.player_frame.pack(pady=10)

        # Buttons
        self.buttons_frame = tk.Frame(self.window, bg="#054b25")
        self.buttons_frame.pack(pady=20)

        self.hit_button = tk.Button(self.buttons_frame, text="Hit", command=self.hit, **button_style)
        self.hit_button.grid(row=0, column=0, padx=20)
        self.hit_button.config(state="disabled")

        self.stand_button = tk.Button(self.buttons_frame, text="Stand", command=self.stand, **button_style)
        self.stand_button.grid(row=0, column=1, padx=20)
        self.stand_button.config(state="disabled")

        # Result label
        self.result_label = tk.Label(self.game_frame, text="", font=("Arial", 20, "bold"), bg="#054b25", fg="white")
        self.result_label.pack(pady=10)

        # Restart button, only visible when chips are 0
        self.restart_button = tk.Button(self.game_frame, text="Restart Game", command=self.restart_game, **button_style)
        self.restart_button.pack(pady=10)
        self.restart_button.pack_forget()

        # AI & Baseline suggestion panel
        self.ai_panel = tk.Frame(self.window, **ai_panel_style)
        self.ai_panel.pack(side="right", fill="y", padx=10, pady=10)
        self.ai_panel.pack_propagate(False)

        self.panel_title_label = tk.Label(self.ai_panel, text="AI Assistant", font=("Arial", 16, "bold"), fg="white", bg="#1a1a1a")
        self.panel_title_label.pack(pady=10)

        # Bet suggestion
        self.bet_suggestion_label = tk.Label(self.ai_panel, text="Suggested Bet: -", font=("Arial", 12), fg="#FFD700", bg="#1a1a1a")
        self.bet_suggestion_label.pack(pady=5)

        # Action suggestion
        self.suggestion_label = tk.Label(self.ai_panel, text="Place a bet to begin", font=("Arial", 14), fg="#FFD700", bg="#1a1a1a", wraplength=250, justify="left")
        self.suggestion_label.pack(pady=10)

        # Reasoning
        self.reason_label = tk.Label(self.ai_panel, text="", font=("Arial", 10), fg="#AAAAAA", bg="#1a1a1a", wraplength=250, justify="left")
        self.reason_label.pack(pady=5)

        # Deck visualization
        self.deck_frame = tk.Frame(self.window, bg="#054b25")
        self.deck_frame.place(x=30, y=680)

        for i in range(5):
            card_label = tk.Label(self.deck_frame, image=self.card_images.get("card_back.gif"), bg="#054b25", bd=2, relief="solid", highlightbackground="white", highlightthickness=1)
            card_label.place(x=i*2, y=-i*3)

        self.start_game()
        self.update_suggestion()

  
    def switch_model(self):
        """
        Switch between AI and Baseline models
        """
        self.current_model = self.model_var.get()
        if self.current_model == "ai":
            self.panel_title_label.config(text="AI Assistant")
        else:
            self.panel_title_label.config(text="Baseline Model")
        self.update_suggestion()

    def load_images(self):
        """
        Load card images
        """
        image_dir = os.path.join(os.path.dirname(__file__), 'images')
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']:
                temp_card = Card(suit, rank)
                filename = temp_card.filename()
                path = os.path.join(image_dir, filename)
                image = Image.open(path).resize((CARD_WIDTH, CARD_HEIGHT))
                self.card_images[filename] = ImageTk.PhotoImage(image)

        back_path = os.path.join(image_dir, "card_back.gif")
        back_img = Image.open(back_path).resize((CARD_WIDTH, CARD_HEIGHT))
        self.card_images["card_back.gif"] = ImageTk.PhotoImage(back_img)

    def start_game(self):
        """
        Start a new game
        """
        self.clear_table()
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.update_suggestion()

    def clear_table(self):
        """
        Clear the table, i.e. remove all cards from the table
        """
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text="")

    def place_bet(self):
        """
        Place a bet
        """
        amount = self.bet_var.get()
        if self.game.place_bet(amount):
            self.bet_button.config(state="disabled")
            self.bet_entry.config(state="disabled")
            self.hit_button.config(state="normal")
            self.stand_button.config(state="normal")
            self.result_label.config(text="")
            self.game.deal_initial()
            self.update_table()
            self.update_chips()
            self.update_suggestion()
        else:
            self.result_label.config(text="Invalid bet.")

    
    def update_suggestion(self):
        """
        Update suggestion based on current deck probabilities
        """
        deck_probs = self.deck.get_remaining_probabilities()
        high_cards = sum(deck_probs[v] for v in range(10, 12))
        mid_cards = sum(deck_probs[v] for v in range(7, 10))
        low_cards = sum(deck_probs[v] for v in range(2, 7))
        
        if self.current_model == "ai":
            suggested_bet = self.ai.choose_bet(deck_probs)
            suggested_bet = min(suggested_bet, self.game.chips)
            self.bet_suggestion_label.config(text=f"Suggested Bet: {suggested_bet}")
        else:
            suggested_bet = self.baseline.get_bet()
            suggested_bet = min(suggested_bet, self.game.chips)
            self.bet_suggestion_label.config(text=f"Suggested Bet: {suggested_bet}")
        
        if not hasattr(self.game, 'player_hand') or len(self.game.player_hand) == 0:
            self.suggestion_label.config(text="Place your bet")
            self.reason_label.config(text=f"High cards: {high_cards*100:.1f}%\n"
                                        f"Mid cards: {mid_cards*100:.1f}%\n"
                                        f"Low cards: {low_cards*100:.1f}%")
        else:
            player_total = self.game.calculate_score(self.game.player_hand)
            dealer_card = self.game.dealer_hand[0].value
            
            if self.current_model == "ai":
                state = self.ai.get_state(player_total, dealer_card, deck_probs, self.game.bet)
                action = self.ai.choose_action(state)
                self.suggestion_label.config(text=f"Action: {action.upper()}")
            else:
                action = self.baseline.get_action(player_total, dealer_card)
                self.suggestion_label.config(text=f"Action: {action.upper()}")
            
            self.reason_label.config(text=f"High cards: {high_cards*100:.1f}%\n"
                                        f"Mid cards: {mid_cards*100:.1f}%\n"
                                        f"Low cards: {low_cards*100:.1f}%")

    def update_table(self, reveal_dealer=False):
        """
        Update the table
        """

        self.clear_table()
        
        for card in self.game.player_hand:
            img = self.card_images[card.filename()]
            label = tk.Label(self.player_frame, image=img, bg="green")
            label.image = img
            label.pack(side="left")

        for idx, card in enumerate(self.game.dealer_hand):
            if idx == 0 or reveal_dealer:
                img = self.card_images[card.filename()]
            else:
                img = self.card_images.get("card_back.gif")
            label = tk.Label(self.dealer_frame, image=img, bg="green")
            label.image = img
            label.pack(side="left")

        self.update_suggestion()

    def hit(self):
        """
        Deal a card to the player's hand
        """
        self.game.hit(self.game.player_hand)
        self.update_table()
        if self.game.calculate_score(self.game.player_hand) > 21:
            self.end_game()

    def stand(self):
        """
        End the player's turn
        """
        while self.game.calculate_score(self.game.dealer_hand) < 17:
            self.game.hit(self.game.dealer_hand)
        self.end_game()

    def end_game(self):
        """
        End the game
        """
        self.update_table(reveal_dealer=True)
        result = self.game.check_winner()
        self.result_label.config(text=result)
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.bet_button.config(state="normal")
        self.bet_entry.config(state="normal")
        self.update_chips()
        
        deck_probs = self.deck.get_remaining_probabilities()
        high_cards = sum(deck_probs[v] for v in range(10, 12))
        mid_cards = sum(deck_probs[v] for v in range(7, 10))
        low_cards = sum(deck_probs[v] for v in range(2, 7))
        
        if self.game.chips <= 0:
            self.suggestion_label.config(text="No more chips left!")
            self.reason_label.config(text="Game over - click Restart to play again")
            self.restart_button.pack()
        else:
            self.suggestion_label.config(text="Place your next bet")
            self.reason_label.config(text=f"High cards: {high_cards*100:.1f}%\n"
                                        f"Mid cards: {mid_cards*100:.1f}%\n"
                                        f"Low cards: {low_cards*100:.1f}%")

    def update_chips(self):
        """
        Update the chips label
        """
        self.chips_label.config(text=f"Chips: {self.game.chips}")

    def restart_game(self):
        """
        Restart the game
        """
        self.game = BlackjackGame(Deck(), chips=500)
        self.bet_button.config(state="normal")
        self.bet_entry.config(state="normal")
        self.restart_button.pack_forget()
        self.update_chips()
        self.clear_table()
        self.suggestion_label.config(text="Place bet to begin")
        self.reason_label.config(text="")
        self.update_suggestion()

    def run(self):
        """
        Run the game
        """
        self.window.mainloop()

if __name__ == "__main__":
    app = BlackjackGUI()
    app.run()