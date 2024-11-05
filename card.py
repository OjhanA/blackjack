import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        

    def __str__(self):
        return f"{self.rank} of {self.suit}" 
    
    def __eq__(self, other):
        # Check if ranks are equal, ignores suits
        if isinstance(other, Card):
            return self.rank == other.rank
        return False
    
    def value(self):
        if self.rank in ["Jack", "Queen", "King"]:
             return 10
        elif self.rank == "Ace":
                return 11 
        else:
            return int(self.rank)
    
    
    def ascii_art(self):
        suit_symbols = {
            'Hearts': '♥',
            'Diamonds': '♦',
            'Clubs': '♣',
            'Spades': '♠'
        }
        rank = f'{self.rank[0]}' if self.rank != '10' else self.rank
        suit = suit_symbols[self.suit]

        return [
            "+--------+",
            f"|{rank:<2}      |",
            "|        |",
            f"|    {suit}   |",
            "|        |",
            f"|      {rank:>2}|",
            "+--------+"
        ]

    def ascii_art_cut_top(self):
        art = self.ascii_art()
        return art[2:]  # Remove the top 2 lines

    def ascii_art_cut_bottom(self):
        art = self.ascii_art()
        return art[:-1]  # Remove the bottom 2 lines

    
        

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, num_decks=1):
        self.cards = [Card(rank, suit) for _ in range(num_decks) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None

    def deal_hand(self, hand_size):
        return [self.deal_card() for _ in range(hand_size)]

    def __str__(self):
        return f"Deck with {len(self.cards)} cards"


# Example usage:
if __name__ == "__main__":
    deck = Deck()
    print(deck)  # Output: Deck with 52 cards

    deck.shuffle()
    hand = deck.deal_hand(5)
    for card in hand:
        print(card)

    print(deck)  # Output: Deck with 47 cards