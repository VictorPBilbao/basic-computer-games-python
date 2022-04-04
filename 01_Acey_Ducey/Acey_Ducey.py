import itertools
from dataclasses import dataclass
from enum import Enum
from random import choice
import os

class Suit(Enum):
    HEARTS = "♥️"
    DIAMONDS = "♦️"
    CLUBS = "♣️"
    SPADES = "♠️"

class Value(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


YELLOW = '\033[33m'
RED = '\033[31m'
END_COLOR = '\033[0m'


@dataclass
class Card():
    suit: Suit
    value: Value
    
    def __str__(self):
        return f"{YELLOW}{self.value.name} OF {self.suit.name} {self.value.value , self.suit.value}{END_COLOR}"

class Deck():
    def __init__(self) -> None:
        self.cards = [
            Card(suit, value) for suit, value in itertools.product(Suit, Value)
        ]
    
    def __str__(self) -> str:
        return "\n".join(str(card) for card in self.cards)

class Game():
    def __init__(self) -> None:
        self.money = 100
        self.round = 0
        self.deck = Deck()
        self.discard = []
        self.discard_bet = []
    
    def play(self) -> None:
        while self.money > 0 and len(self.deck.cards) >= 3:
            self.next_round()
            self.text()
    
    def select_random_card(self) -> Card:
        crd = choice(self.deck.cards)
        self.deck.cards.remove(crd)
        return crd
    
    def text(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nRound {self.round} : Current Money: {self.money}")
        print(f"Here are your two next cards: {self.discard[-1]} and {self.discard[-2]}")
        bet = int(input("How much would you like to bet? "))
        while bet > self.money:
            bet = int(input("You don't have enough money. How much would you like to bet? "))
        self.check_bet(bet)
        
    def next_round(self) -> None:
        self.round += 1
        self.discard = self.discard + [self.select_random_card() for _ in range(2)]
    
    def check_bet(self, bet: int) -> None:
        random_card = self.select_random_card()
        print(f"The random card is: {random_card}")
        cards_in_between = self.cards_range(
            self.discard[-1].value.value, random_card.value.value + 1)
        if random_card.value.value not in cards_in_between:
            self.money -= bet + self.round * 2
            print(f"you lost ${bet + self.round * 2}")
        else:
            print(f"you won ${bet // len(cards_in_between)}")
            self.money += bet // len(cards_in_between)
        input("Press Enter to continue...")
    
    def cards_range(self, start: int, end: int) -> list:
        rn = sorted([start, end])
        return range(rn[0], rn[1] + 1)
    
def main():
    game = Game()
    game.play()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{RED}\nGAME OVER{END_COLOR}')

if __name__ == '__main__':
    main()