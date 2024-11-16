from card import Card, Deck
import os, time


class Hand():
    
    
    def __init__(self, is_player=False, coins=0):
        self.is_player = is_player
        self.cards = []
        self.coins = coins
        self.split_cards = []
        
    def discard(self):
        self.cards = []
        self.split_cards = []
        
    def acquire_bet(self):
        while True:
            try:
                ans = int(input(f"How much would you like to bet? You have {self.coins} coins: "))
                while ans > self.coins or ans < 0:
                    ans = int(input(f"Please give a valid number. You have {self.coins} coins: "))
                self.current_bet = ans
                return
            except:
                print("Invalid input.")
    

    def double_bet(self):
        self.current_bet *= 2
        
    def update_coins(self, win):
        if win == 1:
            self.coins += self.current_bet
        elif win == -1:
            self.coins -= self.current_bet
    
    def draw(self, deck):
        self.cards.append(deck.deal_card())
    
    def draw_cards(self, deck):
        if self.is_player:
            self.cards.extend(deck.deal_hand(2))
        else:
            self.cards.append(deck.deal_card())
            
    def check_split(self):
        if len(self.cards) == 2:
            return self.cards[0] == self.cards[1]
        return False 
            
    def split(self):
        self.split_cards.append(self.cards.pop())
        
    def get_total_value_aux(self, cards):
        value = sum([card.value() for card in cards])
        
        num_aces = sum(1 for card in cards if card.rank == 'Ace')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value
    
    def get_total_value(self):
        return self.get_total_value_aux(self.cards)
        
    
    def check_bust(self):
        if self.get_total_value() <= 21:
            return False
        return True
    
    def check_blackjack(self):
        if self.get_total_value() == 21:
            return True
        return False
    
    def list_cards(self):
        s = "["
        for card in self.cards:
            s += card.__str__() + ", "
        return s[:-2:] + "]."
            
    def __str__(self): 
        if self.is_player:
            return f"You have {self.list_cards()} A total value of {self.get_total_value()}"
        else:
            return f"The Dealer has {self.list_cards()} A total value of {self.get_total_value()}"
        
    def print_bet(self):
        print("You have a total of {self.coins} coins.")
    
    def determine_winner(self, dealer):
        if self.get_total_value() > dealer.get_total_value():
            print("You scored higher than the dealer. You win!")
            return 1
        elif self.get_total_value() == dealer.get_total_value():
            print("Push, tie game")
            return 0
        else:
            print("The dealer scored higher than you. You lose")
            return -1
            
def print_table_view(dealer_hand, player_hand):
    dealer_value = dealer_hand.get_total_value()
    player_value = player_hand.get_total_value()
    dealer_cards = dealer_hand.cards
    player_hands = []
    player_hands.append(player_hand.cards)
    if player_hand.split_cards:
        player_hands.append(player_hand.split_cards)

    print("-"*60)
    
    # Print dealer's cards with the top cut off
    top_view = [card.ascii_art_cut_top() for card in dealer_cards]
    for i in range(len(top_view[0])):  # Iterate through the lines of ASCII art
        print("   ".join(top_view[j][i] for j in range(len(dealer_cards))))
    
    # Print dealer's total
    print(f"Dealer's Total: {dealer_value}".rjust(len(dealer_cards) * 10 + 15))
    
    # Print some space between dealer's and player's cards
    print("\n" * 2)

    # Gather all player hands' ASCII art together
    all_hands_views = []
    for player_cards in player_hands:
        hand_view = [card.ascii_art_cut_bottom() for card in player_cards]
        all_hands_views.append(hand_view)

    # Determine the number of lines each card view has
    num_lines = len(all_hands_views[0][0])

    # Print each line across all hands side by side
    for i in range(num_lines):
        print("       ".join("   ".join(hand[j][i] for j in range(len(hand))) for hand in all_hands_views))
    
    # Print totals for each hand below the respective hands
    space = "       " + " " * 13 * (len(player_hands[0]) - 2)
    totals_str = space.join(f"Hand {index + 1} Total: {player_hand.get_total_value_aux(hand)}"
                                for index, hand in enumerate(player_hands))
    print(totals_str.rjust(len(totals_str) + 5))
    
    # Print player's total
    # print(f"Player's Total: {player_value}   Player's Bet: {player_hand.current_bet}   Player's Coins: {player_hand.coins}" )
    print("-"*60, flush=True)
    
def pause():
    for _ in range(4):
        time.sleep(.75)
        print(".", end="", flush=True)

def clear():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
    
            
while True: 
    response = input("Welcome to Blackjack, would you like to play? (y/n): ")
    if response == 'n':
        print("Thank you for playing!")
        break
        
    game = True
    deck = Deck(6)
    deck.shuffle()
    player_hand, dealer_hand = Hand(is_player=True, coins=50), Hand()

    while game: 
        
        
        player_hand.discard()
        dealer_hand.discard()
        
        player_hand.acquire_bet()
        
        dealer_hand.draw_cards(deck)
        player_hand.draw_cards(deck)
        # player_hand.cards.append(Card("King","Spades"))
        # player_hand.cards.append(Card("King","Hearts"))
        print_table_view(dealer_hand, player_hand)
        
        if player_hand.check_blackjack():
            print("You got a blackjack! You win")
            win = 1
        else: 
            answer = input(f"Would you like to hit, stand, or double? (h/s/d): ")
            
            while answer != "h" and answer != "s":
            
                # if answer == "sp":
                #     if not player_hand.check_split():
                #         answer = input("You can not split with this hand. You must have two cards of the same rank. Pick another option: ")
                #     else:
                #         pass
                #         player_hand.split()
                #         answer = "h"
    
                if answer == "d":
                    if player_hand.current_bet * 2 > player_hand.coins:
                        answer = input("You don't have enough coins to double. You must pick another option: ")
                    else:
                        player_hand.draw(deck)
                        player_hand.double_bet()
                        answer = "s"
                else:
                    answer = input("Please select a valid option (h/s/d): ")
            
            while answer == "h":
                player_hand.draw(deck)

                print_table_view(dealer_hand, player_hand)
                
                if player_hand.check_bust():
                    break
                answer = input("Would you like to hit or stand? (h/s): ")
                if answer == 's':
                    break
            
            print()
            if player_hand.check_bust():
                print_table_view(dealer_hand, player_hand)
                print(f"You bust and lose the game")
                win = -1
        
            # Dealer's turn
            else:
                while dealer_hand.get_total_value() < 17:
                    dealer_hand.draw(deck)
                    print_table_view(dealer_hand, player_hand)
                    print("The Dealer hits", end="", flush=True)
                    pause()
                    print()
                    
                if dealer_hand.get_total_value() > 21:
                    print ("The Dealer busts. You win!")
                    win = 1
                
                else:
                    win = player_hand.determine_winner(dealer_hand)
        
        player_hand.update_coins(win)
        print(f"You now have {player_hand.coins} coins.")
        if player_hand.coins == 0:
            input("\nYou are out of coins! Game over (press enter to restart)")
            clear()
            game = False
        else:
            answer = input("Would you like to play again? (y/n): ")
            clear()
            if answer == "n":
                game = False
        

                

        

        