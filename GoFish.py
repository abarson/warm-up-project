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
GO_FISH = "draw"
SKIP_TURN = "skip"
CHECK_STOCK = "stock"
HAND_SIZE = 7

def main():
    dataBall = DataBall()
    print("Welcome to Go Fish!")
    request = gameStart(dataBall)
    gameGoing = (request == "go")
                
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

        dataBall.difficulty =   difficulty             
        print("Game start!")
        
        stock = Deck()
        stock.shuffle()
        laidDown = Deck([]) # all the books the have been laid down
        
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
    
    while(gameGoing):
        #Player's turn
        player.deck.sort()
        print("-----YOUR TURN-----")
        #if the player asks for a card they don't have, set this to true.
        incorrectAsk = True
        handEmpty = (len(player.deck.cards) == 0)
        stockEmpty = (len(stock.cards) == 0)
        while(incorrectAsk):
            print("\n~~~~~YOUR HAND~~~~~")
            player.deck.printDeck()
            print("~~~~~~~~~~~~~~~~~~~\n")
            if (handEmpty and stockEmpty):
                print("Your deck and the stock deck are empty. Type \"", SKIP_TURN, "\".", sep = "")
            elif (handEmpty):
                print("Your deck is empty. Type \"", GO_FISH, "\".", sep = "")
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
                        print("\n~~~~~~~~~~~~~~BOOKS~~~~~~~~~~~~~~~")
                        if (len(laidDown.cards)==0):
                            print("No books have been laid down, yet!")
                        else:
                            laidDown.printDeck()
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    elif (request == HELP):
                        helpMethods()
                    elif (request == SHOW_RULES):
                        showRules()
                    elif (request == CHECK_STOCK):
                        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print("The stock deck has",len(stock.cards),"cards remaining.")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
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
                        request = formatRank(formated_request)
                        incorrectAsk = False #a valid card was asked for
                        if (opponent.checkDeck(formated_request)): ##let the opponent lie!
                            #if we obtained the last card the opponent picked up from going
                            #fish, then the opponent should no longer try and ask for it.
                            if (formated_request == opponent.recentCard):
                                opponent.setRecentCard(None)
                            #just so it prints out grammatically correct
                            amount = opponent.deck.count(formated_request)

                            #update the databall
                            dataBall.update(amount)
                            
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
                            print("The opponent has ", numString, " ", request, plural,
                                  "! They hand over ", numString, " ", request, plural, ".", sep = "")
                            
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
        #when laidDown has all the cards, the game is over
        if (len(laidDown.cards) == 52):
            gameGoing = False
        #Opponent's turn
        if (gameGoing):
            print("-----OPPONENT TURN-----")
            opponent.deck.sort()
            if(len(opponent.deck.cards) > 0):
                request = opponent.ask() 
                formated_request = formatRank(request)
                print("\"Do you have any ", formated_request, "s?\"", sep='')
                if (player.deck.hasCard(request)):
                    opponent.setRecentCard(None)
                    amount = player.deck.count(request)

                    #update the databall
                    dataBall.update(amount)
                    
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
                        opponent.setRecentCard(None)
                        newCard = stock.dealTop()
                        firstCard = not (opponent.deck.hasCard(newCard.rank))
                        opponent.deck.addCard(newCard) ##we'll need to update some instance variable in opponent
                        if (opponent.deck.hasBook(newCard.rank)):
                            print("The opponent has four ", formatRank(newCard.rank), "s! +1 point", sep = "")
                            laidDown.addCards(opponent.deck.removeAll(newCard.rank))
                            opponent.addBook()
                        elif (firstCard):
                            opponent.setRecentCard(newCard.rank)
                    else:
                        print("The stock is empty. The opponent's turn is over.")
            elif (len(stock.cards) == 0):
                print("The stock and the opponent's hand are empty. There is nothing else they can do.")
            else:
                print("The opponent has no cards! They must go fish.")
                opponent.setRecentCard(None)
                newCard = stock.dealTop()
                firstCard = not (opponent.deck.hasCard(newCard.rank))
                opponent.deck.addCard(newCard) 
                if (opponent.deck.hasBook(newCard.rank)):
                    print("The opponent has four ", formatRank(newCard.rank), "s! +1 point", sep = "")
                    laidDown.addCards(opponent.deck.removeAll(newCard.rank))
                    opponent.addBook()
                        
            if (len(laidDown.cards) == 52):
                gameGoing = False
    print("~~~~~GAME OVER~~~~~")
    if (request != SENTINEL):
        print("All 13 books have been laid down!")
        print("Player Score:", player.books)
        print("Opponent Score:",opponent.books)
        win = 0
        if (player.books > opponent.books):
            print("Congratulations! You won!!")
            win = 1
        elif (player.books < opponent.books):
            print("The opponent won!")
        else:
            print("It's a tie!")
        answer = input("Would you like to see your stats? (y/n) ")
        while(answer!="y" and answer!="n" and answer!="yes" and answer!="no"):
            s = "Please enter either \"y\" or \"n\" "
            answer = input(s)
        
        dataBall.close(win)
    else:
        answer = input("Would you like to see your stats? (y/n) ")
        while(answer!="y" and answer!="n" and answer!="yes" and answer!="no"):
            s = "Please enter either \"y\" or \"n\" "
            answer = input(s)
        print("Goodbye!")
        #don't save results
        dataBall.hard_close()
    

#helps the user get oriented upon opening the application. Should eventually include commands for database.
def gameStart(dataBall):
    command = ""
    while (command != "go" and command != SENTINEL):
        command = input("Enter \"go\" to start the game, \"stats\" to enter STATISTIC CENTER, or \"help\" for more options: ")
        if (command != "go" and command != SENTINEL):
            if (command == "stats"):
                dataBall.stats_center()
                #helpMethods()
            elif (command == "help"):
                helpMethods()
            elif (command == SHOW_RULES):
                showRules()
            elif (command == SHOW_HAND or command == SHOW_SCORE or command == SHOW_BOOKS or command == GO_FISH
                  or command == SKIP_TURN or command == CHECK_STOCK):
                print("This command can only be used while a game is ongoing.")
            else:
                print("Please enter a valid option.")
    return command
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
    print("\n~~~~~~~~~~~COMMANDS~~~~~~~~~~~")
    print("To ask your opponent if they have a card, format your input with a question mark following the value.")
    print("**For example** \"king?\" means you wish to ask for a king, and \"2?\" means you wish to ask for a 2.", sep='') 
    print("Type \"", SHOW_RULES,"\" to display the rules of the game.",sep="")
    print("Type \"", SHOW_HAND,"\" to show the contents of your hand.",sep="")
    print("Type \"", CHECK_STOCK,"\" to show how many cards the stock deck has remaining.",sep="")
    print("Type \"", SHOW_SCORE,"\" to show the score of you and your opponent.",sep="")
    print("Type \"", SHOW_BOOKS,"\" to show the books that have already been laid down.",sep="")
    print("Type \"", GO_FISH,"\" if it is your turn, and you have no cards remaining in your hand.",sep="")
    print("Type \"", SKIP_TURN,"\" if it is your turn, you have no cards remaining in your hand, and the"
          ," stock deck is empty. (Note, at this point, there is nothing else you can do in the game.)", sep="")
    print("Type \"", SENTINEL,"\" to exit the game at any time without saving.", sep="")
    print("~~~~~~~~~~~COMMANDS~~~~~~~~~~~\n")
            
# this method should take the user's input and return a value that can be checked, or false if it's invalid
# for example, user_input = kings? should return 13
def parseInput(user_input):
    if (user_input == "2?" or user_input == "2" or user_input == "two?"
        or user_input == "two" or user_input == "Two" or user_input == "Two?"):
        return 2
    elif (user_input == "3?" or user_input == "3" or user_input == "three?"
        or user_input == "three" or user_input == "Three" or user_input == "Three?"):
        return 3
    elif (user_input == "4?" or user_input == "4" or user_input == "four?"
        or user_input == "four" or user_input == "Four" or user_input == "Four?"):
        return 4
    elif (user_input == "5?" or user_input == "5" or user_input == "five?"
        or user_input == "five" or user_input == "Five" or user_input == "Five?"):
        return 5
    elif (user_input == "6?" or user_input == "6" or user_input == "six?"
        or user_input == "six" or user_input == "Six" or user_input == "Six?"):
        return 6
    elif (user_input == "7?" or user_input == "7" or user_input == "seven?"
        or user_input == "seven" or user_input == "Seven" or user_input == "Seven?"):
        return 7
    elif (user_input == "8?" or user_input == "8" or user_input == "eight?"
        or user_input == "eight" or user_input == "Eight" or user_input == "Eight?"):
        return 8
    elif (user_input == "9?" or user_input == "9" or user_input == "nine?"
        or user_input == "nine" or user_input == "Nine" or user_input == "Nine?"):
        return 9
    elif (user_input == "10?" or user_input == "10" or user_input == "ten?"
        or user_input == "ten" or user_input == "Ten" or user_input == "Ten?"):
        return 10
    elif (user_input == "jack?" or user_input == "jack" or user_input == "j?"
        or user_input == "j" or user_input == "Jack" or user_input == "Jack?"
          or user_input == "J?" or user_input == "J"):
        return Card.JACK
    elif (user_input == "queen?" or user_input == "queen" or user_input == "q?"
        or user_input == "q" or user_input == "Queen" or user_input == "Queen?"
          or user_input == "Q?" or user_input == "Q"):
        return Card.QUEEN
    elif (user_input == "king?" or user_input == "king" or user_input == "k?"
        or user_input == "k" or user_input == "King" or user_input == "King?"
          or user_input == "K?" or user_input == "K"):
        return Card.KING
    elif (user_input == "ace?" or user_input == "ace" or user_input == "a?"
        or user_input == "a" or user_input == "Ace" or user_input == "Ace?"
          or user_input == "A?" or user_input == "A"):
        return Card.ACE
    else:
        return False
main()
