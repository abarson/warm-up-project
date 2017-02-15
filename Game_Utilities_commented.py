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


    def ask(self):
        """Returns the rank of a card to ask for, depending on the difficulty.  If the
        lowest difficulty, it choses a random rank from its hand.  If the top two difficulties,
        choses the rank of the latest card it recieved, or the rank of a card it has in its hand
        based on a continuing card rotation"""
        
        if (self.difficulty == 0):
            rand = len(self.deck.cards)-1
            index = randint(0, rand)
            return self.deck.cards[index].rank
        
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
    """A class that constructs a list of cards and provides different ways to
    manipulate this list"""
    
    def __init__(self, i = None):
        """Deck constructor, makes a default deck with 52 unique cards added to the list.
        It also contains the ability to pass in a list to form a custom deck"""
        if i is None:
            self.cards = []
            for i in range(Card.DIAMONDS + 1):
                for j in range(2, Card.ACE + 1):
                    self.cards.append(Card(i, j))
        else:
            self.cards = i
        
              
    def hasCard(self, rank):
        """ Checks through the deck to see if it contains cards of a certain rank,
        with said rank as an the input variable, and returning either true or false."""
        for i in range(len(self.cards)):
            if(self.cards[i].checkEquals(rank)):
                return True
        return False
    
    def printDeck(self):
        """print all cards that are contained in the deck as strings"""
        for i in range(len(self.cards)):
            print(self.cards[i].toString())

    def removeAll(self, rank):
        """Takes rank as an input variable and removes all cards of that rank that are
        contained in the deck as a list of cards"""
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
    
    def addCards(self, newCards):
        """Takes a card as in input variable and adds that card to the deck"""
        for i in range(len(newCards)):
            self.cards.append(newCards[i])

            
    def hasBook(self, rank):
        """Takes a rank as an input variable and checks over the whole deck to see if
        four cards of this rank are contained in the deck"""
        return (self.count(rank) == 4)

    
    def count(self, rank):
        """Takes a rank as an input variable and checks how many cards of that rank are
        in the deck.  Returns that number."""
        counter=0
        for i in range(len(self.cards)):
            if self.cards[i].checkEquals(rank):
                counter+=1
        return counter


    def addCard(self, card):
        """Takes a card as an input variable and adds it to the deck."""
        self.cards.append(card)


    def sort(self):
        """Sorts the cards in the deck based on their rank, from lowest to highest."""
        self.cards = sorted(self.cards, key=lambda card: card.rank)
    

    def shuffle(self):
        """Randomizes the order of cards in the deck"""
        shuffle(self.cards)

        

    def deal(self,size):
        """takes some int size as an input and removes the top n=size cards from the deck,
        returning these cards as a list"""
        if (len(self.cards) > size):
            dealt = []
            for i in range(size):
                dealt.append(self.cards.pop())
            return dealt
        else:
            print("Deck is too small!")
    

    def dealTop(self):
        """Removes the top card from the deck and returns it"""
        card=self.cards.pop()
        return card

class Player():
    def __init__(self, deck):
        self.deck = deck
        self.books = 0
    def addBook(self):
        self.books += 1
