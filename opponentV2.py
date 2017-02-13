import random
class Opponent():
    def __init__(self, deck, difficulty, laidDown,):
        self.deck = deck
        self.difficulty = difficulty
        self.laidDown = laidDown
        self.books = 0
        self.recentCard = None

    ##depending on difficulty, the Opponent might lie       
    def checkDeck(self, user_input):
        return self.deck.hasCard(user_input)

    ##depending on difficulty and recentCard, the opponent asks the user for a card
    def ask(self):
        #On easy difficulty, the opponent asks for a random card from its hand
        if self.difficulty==0:
            num=random.randint(0,len(self.deck)-1)
            card=self.deck[num].rank
            return card
            
            card=self.deck[-1]
            return card
            
            #On hard or devious difficulty, the opponent asks for the last
            #card added to its hand
        elif self.difficulty==1 or self.difficulty==2:
            if self.recentCard != None:
                card=self.recentCard.rank
            else:
                #do some stuff
            return card
