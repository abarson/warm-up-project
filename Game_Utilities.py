from random import randint
class Opponent():
    def __init__(self, deck, difficulty, laidDown):
        self.deck = deck
        self.difficulty = difficulty
        self.laidDown = laidDown
        self.books = 0
        self.recentCard = None
        self.lastAskedFor = None
        self.lieCounter = 4
    #add a book
    def addBook(self):
        self.books += 1

    #the most recent card from going fish
    def setRecentCard(self, user_input):
        self.recentCard = user_input
        
    #should find the next card in the rotation of the opponent's deck
    def findNextCard(self):
        if (self.lastAskedFor == None):
            i = 2
            while (not self.deck.hasCard(i)):
                i+=1
            self.lastAskedFor = i
        else:
            self.lastAskedFor += 1
            while(not self.deck.hasCard(self.lastAskedFor)):
                self.lastAskedFor += 1
                if (self.lastAskedFor > Card.ACE):
                    self.lastAskedFor = 2
                
            
    
    ##depending on difficulty, the Opponent might lie       
    def checkDeck(self, user_input):
        hasCard = self.deck.hasCard(user_input)
        if (self.difficulty < 2):
            return hasCard
        else:
            #print("Lie counter:", self.lieCounter)
            #lie every third time
            if (hasCard and self.lieCounter % 3 == 0):
                print(">:-)")
                self.lieCounter+=1
                return False
            elif (hasCard):
                self.lieCounter+=1
                return hasCard
            else:
                return hasCard

    ##depending on difficulty and recentCard, the opponent asks the user for a card
    def ask(self):
        #just choose a random card from its hand
        if (self.difficulty == 0):
            rand = len(self.deck.cards)-1
            index = randint(0, rand)
            return self.deck.cards[index].rank
        #either ask for the last card picked up thru going fish, or continue in card
        #rotation
        elif (self.difficulty == 1 or self.difficulty == 2):
            if (self.recentCard != None):
                return self.recentCard
            else:
                self.findNextCard()
                return self.lastAskedFor
    
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

    def rankToString(self):
        return formatRank(self.rank)
    
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

#takes an int and prints out the corresponding rank
def formatRank(rank):
    formated_rank = ""
    if (rank == 2):
        formated_rank = "two"
    elif (rank == 3):
        formated_rank = "three"
    elif (rank == 4):
        formated_rank = "four"
    elif (rank == 5):
        formated_rank = "five"
    elif (rank == 6):
        formated_rank = "six"
    elif (rank == 7):
        formated_rank = "seven"
    elif (rank == 8):
        formated_rank = "eight"
    elif (rank == 9):
        formated_rank = "nine"
    elif (rank == 10):
        formated_rank = "ten"
    elif (rank == Card.JACK):
        formated_rank = "Jack"
    elif (rank == Card.QUEEN):
        formated_rank = "Queen"
    elif (rank == Card.KING):
        formated_rank = "King"
    elif (rank == Card.ACE):
        formated_rank = "Ace"
    else:
        formated_rank = "what"
    return formated_rank

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

    #adds a single card to this deck
    def addCard(self, card):
        self.cards.append(card)

    #sorts card based on rank
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

class Player():
    def __init__(self, deck):
        self.deck = deck
        self.books = 0
    def addBook(self):
        self.books += 1
