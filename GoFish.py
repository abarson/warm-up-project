from data_ball import DataBall
from Game_Utilities import Card
from Game_Utilities import Deck
from Game_Utilities import Opponent
from Game_Utilities import Player
from Game_Utilities import formatRank

SENTINEL = "stop"
HELP = "help"
SHOW_RULES = "rules"
SHOW_HAND = "show"
SHOW_SCORE = "score"
SHOW_BOOKS = "books"
GO_FISH = "go fish"
SKIP_TURN = "skip"
CHECK_STOCK = "stock"
HAND_SIZE = 7

DEBUG = False
def main():
    
    print("Welcome to Go Fish!")
    gameGoing = gameStart()
                
    if (gameGoing):
        
        #get the difficulty
        difficulty = -1
        while(difficulty != 0 and difficulty != 1 and difficulty != 2):
            try:
                difficulty = int(input("Enter user difficulty (0 = easy, 1 = smart, 2 = devious): "))
                if (difficulty != 0 and difficulty != 1 and difficulty != 2):
                    print("Please enter either 0, 1, or 2.")
            except:
                print("Please enter either 0, 1, or 2.")
                
        print("Game start!")
        
        #dataBall = DataBall(difficulty)
        #dataBall.update()
        #start creating all the objects
        
        stock = Deck()
        stock.shuffle()
        laidDown = Deck([]) # all the books the have been laid down
        
        if (DEBUG):
            card5 = Card(Card.DIAMONDS, 5)
            card6 = Card(Card.DIAMONDS, Card.QUEEN)
            card7 = Card(Card.CLUBS, Card.KING)
            card8 = Card(Card.CLUBS, Card.ACE)
            card9 = Card(Card.DIAMONDS, Card.ACE)
            card10 = Card(Card.SPADES, Card.ACE)
            card11 = Card(Card.HEARTS, Card.ACE)
            playerTestHand = [card8, card9, card10, card11]
            player = Player(Deck(playerTestHand))
        else:
            player = Player(Deck(stock.deal(HAND_SIZE)))
        
        opponent = Opponent(Deck(stock.deal(HAND_SIZE)), difficulty, laidDown)

        #check for books right away, in the off chance one of the player's has one
        for i in range(2, Card.ACE + 1):
            if (player.deck.hasBook(i)):
                laidDown.addCards(player.deck.removeAll(i))
                player.addBook()
                print("This is incredible! You started the game off with a book.")
            if (opponent.deck.hasBook(i)):
                laidDown.addCards(opponent.deck.removeAll(i))
                opponent.addBook()
                print("This is incredible! The computer player started the game off with a book.")
    request = ""
    while(gameGoing):
        #Player's turn
        player.deck.sort()
        print("-----YOUR TURN-----")
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
                        print("\n~~~~~YOUR HAND~~~~~")
                        player.deck.printDeck()
                        print("~~~~~~~~~~~~~~~~~~~\n")
                    elif (request == SHOW_SCORE):
                        print("\n~~~~~~~SCORE~~~~~~~")
                        print("Player score: ", format(player.books, '4d'))
                        print("Computer score: ", format(opponent.books, '2d'))
                        print("~~~~~~~~~~~~~~~~~~~\n")
                    elif (request == SHOW_BOOKS):
                        print("\n~~~~~~~BOOKS~~~~~~~")
                        if (len(laidDown.cards)==0):
                            print("No books have been laid down, yet!")
                        else:
                            laidDown.printDeck()
                        print("~~~~~~~~~~~~~~~~~~~\n")
                    elif (request == HELP):
                        helpMethods()
                    elif (request == SHOW_RULES):
                        showRules()
                    elif (request == CHECK_STOCK):
                        print("\n~~~~~~~~~~~~~~~~~~~")
                        print("The stock deck has",len(stock.cards),"cards remaining.")
                        print("~~~~~~~~~~~~~~~~~~~\n")
                    elif (request == "cpu"):
                        opponent.deck.printDeck()
                    else:
                        print("Invalid input, please try again.")
                    request = input("What would you like? ")
                    formated_request = parseInput(request)
                if (handEmpty and stockEmpty): # the order of these should be switched up, so that SENTINEL is checked for first
                    if (request != SKIP_TURN):
                        print("The stock and your hand are empty. There is nothing else you can do.")
                    incorrectAsk = False
                elif (request != SENTINEL):
                    #make sure the player is asking for a card they have already
                    if (request != GO_FISH and player.deck.hasCard(formated_request)):
                        #get rid of the question mark so it can be printed
                        #request = request[0:-1]
                        request = formatRank(formated_request)
                        incorrectAsk = False #a valid card was asked for
                        if (opponent.checkDeck(formated_request)): ##let the opponent lie!
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
                            if (len(stock.cards) > 0):
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
                            else:
                                print("The stock is empty. Your turn is over.")
                    #the user's hand is empty
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
                    #if you get here, the user did something wrong
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
        if (len(laidDown.cards) == 52):
            gameGoing = False
        #Opponent's turn
        if (gameGoing):
            print("-----OPPONENT TURN-----")
            opponent.deck.sort()
            request = opponent.ask() #not implemented
            formated_request = formatRank(request)
            print("\"Do you have any ", formated_request, "s?\"", sep='')
            if (player.deck.hasCard(request)):
                amount = player.deck.count(request)
                numString = ""
                plural = ""
                if (amount == 1):
                    numString = "one"
                elif (amount == 2):
                    numString = "two"
                    plural = "s"
                else:
                    numString = "three"
                    plural = "s"
                opponent.deck.addCards(player.deck.removeAll(request))
                print("You hand over ", numString, " ", formated_request, plural, " to the opponent.", sep = '')
                if (opponent.deck.hasBook(request)):
                    print("The opponent has four ", formated_request, "s! +1 point", sep = "")
                    laidDown.addCards(opponent.deck.removeAll(request))
                    opponent.addBook()

            #go fish!                   
            else:
                print("You don't have any ", formated_request, "s. The opponent must go fish!", sep = '')
                if (len(stock.cards) > 0):
                    newCard = stock.dealTop()
                    opponent.deck.addCard(newCard) ##we'll need to update some instance variable in opponent
                    if (opponent.deck.hasBook(newCard.rank)):
                        print("The opponent has four ", formatRank(newCard.rank), "s! +1 point", sep = "")
                        laidDown.addCards(opponent.deck.removeAll(newCard.rank))
                        opponent.addBook()
                else:
                    print("The stock is empty. The opponent's turn is over.")
            if (len(laidDown.cards) == 52):
                gameGoing = False
    print("~~~~~GAME OVER~~~~~")
    if (request != SENTINEL):
        print("All 13 books have been laid down!")
    print("Player Score:", player.books)
    print("Opponent Score:",opponent.books)
    if (player.books > opponent.books):
        print("Congratulations! You won!!")
    else:
        print("The opponent won!")
    print("Goodbye!")

#helps the user get oriented upon opening the application. Should eventually include commands for database.
def gameStart():
    command = ""
    while (command != "go" and command != SENTINEL):
        command = input("Enter \"go\" to start the game, or \"help\" for more options: ")
        if (command != "go" and command != SENTINEL):
            if (command == "help"):
                helpMethods()
            elif (command == SHOW_RULES):
                showRules()
            elif (command == SHOW_HAND or command == SHOW_SCORE or command == SHOW_BOOKS or command == GO_FISH
                  or command == SKIP_TURN or command == CHECK_STOCK):
                print("This command can only be used while a game is ongoing.")
            else:
                print("Please enter a valid option.")
    return command == "go"
# prints out the rules of the game
def showRules():
    print("The objective of Go Fish is to obtain as many \"books\", or four of a kinds, as possible.")
    print("During your turn, you may ask the opponent for one card. This card MUST be in your hand.")
    print("If the opponent has one or more of the card you asked for, they must turn it over to you.")
    print("If they have none of the card you ask for, you must \"go fish\", or take a card from the stock deck.")
    print("During the opponent's turn, they will do the same for you.")
    print("To start the game, both you and the opponent will receive", HAND_SIZE, "cards.")
    print("The game ends when all 13 books have been obtained.")

# prints out every command the user can give to the console
def helpMethods():
    print("Type \"", SHOW_RULES,"\" to display the rules of the game.",sep="")
    print("Type \"", SHOW_HAND,"\" to show the contents of your hand.",sep="")
    print("Type \"", CHECK_STOCK,"\" to show how many cards the stock deck has remaining.",sep="")
    print("Type \"", SHOW_SCORE,"\" to show the score of you and your opponent.",sep="")
    print("Type \"", SHOW_BOOKS,"\" to show the books that have already been laid down.",sep="")
    print("Type \"", GO_FISH,"\" if it is your turn, and you have no cards remaining in your hand.",sep="")
    print("Type \"", SKIP_TURN,"\" if it is your turn, you have no cards remaining in your hand, and the"
          ," stock deck is empty. (Note, at this point, there is nothing else you can do in the game.)", sep="")
    print("Type \"", SENTINEL,"\" to exit the game at any time without saving.", sep="")
            
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
