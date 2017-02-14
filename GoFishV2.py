class Opponent():
    def __init__(self, deck, difficulty, laidDown):
        self.deck = deck
        self.difficulty = difficulty
        self.laidDown = laidDown
        self.books = 0
        self.recentCard = None

    ##depending on difficulty, the Opponent might lie       
    def checkDeck(self, user_input):
        return self.deck.hasCard(user_input)
    
    def setRecentCard(self, user_input):
        self.recentCard = user_input
        
    ##depending on difficulty and recentCard, the opponent asks the user for a card
    def ask():
        return 2
    
class Card():
    
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    
    SPADES = 0
    CLUBS = 1
    HEARTS = 2
    DIAMONDS = 3
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def checkEquals(self, otherRank):
        return self.rank == otherRank
    
    def toString(self):
        formated_suit = ""
        if (self.suit == Card.SPADES):
            formated_suit = "Spades"
        elif (self.suit == Card.CLUBS):
            formated_suit = "Clubs"
        elif (self.suit == Card.HEARTS):
            formated_suit = "Hearts"
        elif (self.suit == Card.DIAMONDS):
            formated_suit = "Diamonds"
        else:
            formated_suit = "what"

        formated_rank = ""
        if (self.rank >= Card.JACK):
            if (self.rank == Card.JACK):
                formated_rank = "Jack"
            elif (self.rank == Card.QUEEN):
                formated_rank = "Queen"
            elif (self.rank == Card.KING):
                formated_rank = "King"
            else:
                formated_rank = "Ace"
        else:
            formated_rank = self.rank
        output = str(formated_rank) + " of " + str(formated_suit)
        return output
                
class Player():
    def __init__(self, deck):
        self.deck = deck
        self.books = 0
    def addBook(self):
        self.books += 1
#This class has list of cards, and methods for creating, viewing, and manipulating the list
#in various ways important to how Go Fish is played
from random import shuffle
class Deck():
    #this allows default construction, where 52 cards are added to a list, or it allows a list to be passed in
    def __init__(self, i = None):
        if i is None:
            self.cards = []
            for i in range(Card.DIAMONDS + 1):
                for j in range(2, Card.ACE + 1):
                    self.cards.append(Card(i, j))
        else:
            self.cards = i
            
    #Checks through the deck to see if it contains a certain card   
    def hasCard(self, rank):
        for i in range(len(self.cards)):
            if(self.cards[i].checkEquals(rank)):
                return True
        return False
    
    #Prints the deck as a string list, showing the cards in the deck
    def printDeck(self):
        for i in range(len(self.cards)):
            print(self.cards[i].toString())

    #removes all instances of rank and returns them in a list
    def removeAll(self, rank):
        removed = []
        if (self.hasCard(rank)):
            newList = []
            for i in range(len(self.cards)):
                if self.cards[i].checkEquals(rank):
                    removed.append(self.cards[i])
                else:
                    newList.append(self.cards[i])
            self.cards = newList
        return removed
        #required some major changes because python is dumb
    
    #adds newCards to this Deck's cards
    def addCards(self, newCards):
        for i in range(len(newCards)):
            self.cards.append(newCards[i])

        #fixed: can't append a list to a list?
            
    #checks to see if this Deck has four of the same rank card
    def hasBook(self, rank):
        return (self.count(rank) == 4)
    
        #fixed using count
    
    #counts the occurrence of rank Card in the deck and returns it
    def count(self, rank):
        counter=0
        for i in range(len(self.cards)):
            if self.cards[i].checkEquals(rank):
                counter+=1
        return counter

        #fixed: compare cards[i] and rank with checkEquals

    def sort(self):
        self.cards = sorted(self.cards, key=lambda card: card.rank)
    
    #randomizes the order of cards in the deck
    def shuffle(self):
        shuffle(self.cards)

        #fixed: shuffle is an in-place "unsort", doesn't return anything
        
    #removes the top n=size cards from the deck and returns them as a list
    def deal(self,size):
        if (len(self.cards) > size):
            dealt = []
            for i in range(size):
                dealt.append(self.cards.pop())
            return dealt
        else:
            print("Deck is too small!")
        #fixed: dealt needed append method
    
    #removes only the top card from the deck and returns it
    def dealTop(self):
        card=self.cards.pop()
        return card
def test():
    card1 = Card(Card.HEARTS, 5)
    card2 = Card(Card.DIAMONDS, 6)
    card3 = Card(Card.DIAMONDS, 7)
    card4 = Card(Card.DIAMONDS, Card.KING)
    card5 = Card(Card.SPADES, Card.QUEEN)
    card6 = Card(Card.CLUBS, 8)
    card7 = Card(Card.SPADES, Card.ACE)
    cardList = [card1, card2, card3, card4, card5, card6, card7]
    deck = Deck(cardList)
    print("Contents of this deck:")
    deck.printDeck()
    print("\nTesting shuffle:")
    deck.shuffle()
    deck.printDeck()

    print("\nTesting sort:")
    deck.sort()
    deck.printDeck()
    
    print("\nTesting dealTop:")
    newCard = deck.dealTop()
    print(newCard.toString(),"was dealt from the deck.")

    print("Remainder of deck:")
    deck.printDeck()

    print("\nTesting deal:")
    deck2 = Deck(deck.deal(5))
    print("Contents of new deck with 4 cards dealt from old deck:")
    deck2.printDeck()
    print("Contents of original deck:")
    deck.printDeck()
    print("If deal tries to fetch too many cards:")
    deck.deal(5)

    card1 = Card(Card.HEARTS, 5)
    card2 = Card(Card.SPADES, 5)
    card3 = Card(Card.HEARTS, Card.KING)
    card4 = Card(Card.CLUBS, 5)
    card5 = Card(Card.DIAMONDS, 5)
    card6 = Card(Card.DIAMONDS, Card.QUEEN)
    card7 = Card(Card.CLUBS, Card.KING)
    card8 = Card(Card.CLUBS, Card.ACE)
    card9 = Card(Card.DIAMONDS, Card.ACE)
    card10 = Card(Card.SPADES, Card.ACE)
    card11 = Card(Card.HEARTS, Card.ACE)
    cardList = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10, card11]
    print("\nStarting over. New deck:")
    deck = Deck(cardList)
    deck.printDeck()
    print("\nTesting count:")
    amountOfFives = deck.count(5)
    amountOfKings = deck.count(Card.KING)
    amountOfQueens = deck.count(Card.QUEEN)
    amountOfTwos = deck.count(2)
    amountOfAces = deck.count(Card.ACE)
    print("This deck has", amountOfFives, "fives")
    print("This deck has", amountOfKings, "kings")
    print("This deck has", amountOfQueens, "queens")
    print("This deck has", amountOfTwos, "twos")
    print("This deck has", amountOfAces, "aces")

    print("\nTesting hasBook")
    if (deck.hasBook(5)):
        print("This deck has four fives!")
    else:
        print("This deck doesn't have four fives.")
    if (deck.hasBook(Card.KING)):
        print("This deck has four kings!")
    else:
        print("This deck doesn't have four kings.")
    if (deck.hasBook(Card.QUEEN)):
        print("This deck has four queens!")
    else:
        print("This deck doesn't have four queens.")
    if (deck.hasBook(Card.ACE)):
        print("This deck has four aces!")
    else:
        print("This deck doesn't have four aces.")
        
    print("\nTesting removeAll:")
    deck3 = Deck(deck.removeAll(Card.KING))
    print("New deck made up Kings from old deck:")
    deck3.printDeck()
    print("Old deck:")
    deck.printDeck()

    print("\nTesting addCards:")
    deck.addCards(deck3.removeAll(Card.KING))
    print("New deck with Kings removed")
    deck3.printDeck()
    print("Old deck with Kings returned:")
    deck.printDeck()

    laidDown = Deck([])
    print("\nSome game functionality:")
    print("check from 2 - Card.ACE + 1 (15) for books and remove them...")
    for i in range(2, Card.ACE + 1):
        if (deck.hasBook(i)):
            laidDown.addCards(deck.removeAll(i))
    print("old deck after this runs:")
    deck.printDeck()
    print("The books that were removed:")
    laidDown.printDeck()
    
test()




    
