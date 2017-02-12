from data_ball import DataBall
from Game_Utilities import Card
from Game_Utilities import Deck
from Game_Utilities import Opponent
from Game_Utilities import Player

SENTINEL = "stop"
HELP = "help"
SHOW_RULES = "rules"
SHOW_HAND = "show"
SHOW_SCORE = "score"
SHOW_BOOKS = "books"
GO_FISH = "go fish"
SKIP_TURN = "skip"
HAND_SIZE = 7

def main():

    print("Welcome to Go Fish!")
    command = ""
    while (command != "go"):
        command = input("Enter \"go\" to start the game, or \"help\" for more options: ")
        if (command != "go"):
            if (command == "help"):
                helpMethods()
            elif (command == SHOW_RULES):
                showRules()
            else:
                print("Please enter a valid option.")
    
    #get the difficulty
    difficulty = int(input("Enter user difficulty (0 = easy, 1 = smart, 2 = devious): "))
    #dataBall = DataBall(difficulty)
    #dataBall.update()
    #start creating all the objects
    
    stock = Deck()
    stock.shuffle()
    laidDown = Deck([]) # all the books the have been laid down
    
    #make two more decks out of the card lists
    card5 = Card(Card.DIAMONDS, 5)
    card6 = Card(Card.DIAMONDS, Card.QUEEN)
    card7 = Card(Card.CLUBS, Card.KING)
    card8 = Card(Card.CLUBS, Card.ACE)
    card9 = Card(Card.DIAMONDS, Card.ACE)
    card10 = Card(Card.SPADES, Card.ACE)
    card11 = Card(Card.HEARTS, Card.ACE)
    playerTestHand = [card8, card9, card10, card11]
    
    #playerHand = Deck(stock.deal(HAND_SIZE))
    #opponentHand = Deck(stock.deal(HAND_SIZE))
            
    player = Player(Deck(stock.deal(HAND_SIZE)))
    opponent = Opponent(Deck(stock.deal(HAND_SIZE)), difficulty, laidDown)

    #check for books right away, in the off chance one of the player's has one
    for i in range(2, Card.ACE + 1):
        if (player.deck.hasBook(i)):
            laidDown.addCards(player.deck.removeAll(i))
            player.addBook()
            print("Wow you already have a book")
        if (opponent.deck.hasBook(i)):
            laidDown.addCards(opponent.deck.removeAll(i))
            opponent.addBook()
            print("Wow they already have a book")
    
    gameGoing = True
    while(gameGoing):
        #Player's turn
        player.deck.sort()
        print("Your turn!")
        #if the player asks for a card they don't have, set this to true.
        incorrectAsk = True
        handEmpty = (len(player.deck.cards) == 0)
        stockEmpty = (len(stock.cards) == 0)
        while(incorrectAsk):
            request = input("What would you like? ")
            if (request != SENTINEL):
                formated_request = parseInput(request)
                while (request != SENTINEL and request != SKIP_TURN and request != GO_FISH and not formated_request):
                    #check commands
                    if (request == SHOW_HAND):
                        print("\nYour hand:")
                        player.deck.printDeck()
                        print("The stock deck has",len(stock.cards),"cards remaining.\n")
                    elif (request == SHOW_SCORE):
                        print("Player score: ", player.books)
                        print("Computer score: ", opponent.books)
                    elif (request == SHOW_BOOKS):
                        print("\nLaid Down Books:")
                        laidDown.printDeck()
                    elif (request == HELP):
                        helpMethods()
                    elif (request == SHOW_RULES):
                        showRules()
                    else:
                        print("Invalid input, please try again.")
                    request = input("What would you like? ")
                    formated_request = parseInput(request)
                if (handEmpty and stockEmpty):
                    if (request != SKIP_TURN):
                        print("The stock and your hand are empty. There is nothing else you can do.")
                elif (request != SENTINEL):
                    #make sure the player is asking for a card they have already
                    if (request != GO_FISH and player.deck.hasCard(formated_request)):
                        #get rid of the question mark so it can be printed
                        request = request[0:-1]
                        incorrectAsk = False #a valid card was asked for
                        if (opponent.checkDeck(formated_request)):
                            amount = opponent.deck.count(formated_request)
                            #just so it prints out grammatically correct
                            if (amount == 1):
                                print("The opponent has a ", request, "!", sep = "")
                            else:
                                print("The opponent has ", amount, " ", request, "s!", sep = "")
                            player.deck.addCards(opponent.deck.removeAll(formated_request))
                            #check for a book
                            if (player.deck.hasBook(formated_request)):
                                print("You have four ", request, "s! +1 point", sep = "")
                                laidDown.addCards(player.deck.removeAll(formated_request))
                                player.addBook()
                                
                        #Go fish!
                        else:
                            print("The opponent does not have any ", request,"s. Go fish!", sep = "")
                            newCard = stock.dealTop()
                            print("You picked up a ", newCard.toString(), ".", sep = "")
                            player.deck.addCard(newCard)
                            
                            #got the card you asked for originally
                            if (newCard.checkEquals(formated_request)):
                                print("You picked up the card you originally asked for! Wow!")
                                
                            if (player.deck.hasBook(newCard.rank)):
                                print("You have four ", newCard.rankToString(), "s! +1 point", sep = "")
                                laidDown.addCards(player.deck.removeAll(newCard.rank))
                                player.addBook()
                    elif (handEmpty and request != SKIP_TURN):
                        if (request != GO_FISH):
                            print("Your hand is empty! You will have to go fish.")
                        newCard = stock.dealTop()
                        print("You picked up a ", newCard.toString(), ".", sep = "")
                        player.deck.addCard(newCard)
                        handEmpty = False
                        if (player.deck.hasBook(newCard.rank)):
                            print("You have four ", newCard.rankToString(), "s! +1 point", sep = "")
                            laidDown.addCards(player.deck.removeAll(newCard.rank))
                            player.addBook()
                        incorrectAsk = False
                    else:
                        incorrectAsk = True #either the player tried to go fish when they still
                        #had cards, tried to skip when the game wasn't over, or they asked for a card they didn't have
                        if (request == GO_FISH):
                            print("You can only request to go fish when you have no cards remaining.")
                        elif (request == SKIP_TURN):
                            print("You can only skip your turn when you have no cards left, and the stock is empty.") 
       
                        else:
                            print("You need to ask for a card that you already have!")
                        
                else:
                    gameGoing = False
                    incorrectAsk = False
            else:
                gameGoing = False
                incorrectAsk = False
        #Opponent's turn
        if (gameGoing):
            print("Opponent's turn.")
            opponent.deck.sort()
            #request = opponent.ask()
def showRules():
    print("The objective of Go Fish is to obtain as many \"books\", or four of a kinds, as possible.")
    print("During your turn, you may ask the opponent for one card. This card MUST be in your hand.")
    print("If the opponent has one or more of the card you asked for, they must turn it over to you.")
    print("If they have none of the card you ask for, you must \"go fish\", or take a card from the stock deck.")
    print("During the opponent's turn, they will do the same for you.")
    print("To start the game, both you and the opponent will receive", HAND_SIZE, "cards.")
    print("The game ends when all 13 books have been obtained.")
def helpMethods():
    print("Type \"", SHOW_RULES,"\" to display the rules of the game.",sep="")
    print("Type \"", SHOW_HAND,"\" to show the contents of your hand.",sep="")
    print("Type \"", SHOW_SCORE,"\" to show the score of you and your opponent.",sep="")
    print("Type \"", SHOW_BOOKS,"\" to show the books that have already been laid down.",sep="")
    print("Type \"", GO_FISH,"\" if it is your turn, and you have no cards remaining in your hand.",sep="")
    print("Type \"", SKIP_TURN,"\" if it is your turn, you have no cards remaining in your hand, and the"
          ," stock deck is empty. (Note, at this point, there is nothing else you can do in the game.)", sep="")
            
# this method should take the user's input and return a value that can be checked, or false if it's invalid
# for example, user_input = kings? should return 13
def parseInput(user_input):
    if (user_input == "2?"):
        return 2
    elif (user_input == "3?"):
        return 3
    elif (user_input == "4?"):
        return 4
    elif (user_input == "5?"):
        return 5
    elif (user_input == "6?"):
        return 6
    elif (user_input == "7?"):
        return 7
    elif (user_input == "8?"):
        return 8
    elif (user_input == "9?"):
        return 9
    elif (user_input == "10?"):
        return 10
    elif (user_input == "jack?"):
        return Card.JACK
    elif (user_input == "queen?"):
        return Card.QUEEN
    elif (user_input == "king?"):
        return Card.KING
    elif (user_input == "ace?"):
        return Card.ACE
    else:
        return False
main()
