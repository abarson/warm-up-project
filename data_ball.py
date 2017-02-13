
import sqlite3
import datetime

class DataBall :
    
    """
    An all encapsulating ball of data used to produce player statistics for games 
    of 'Go Fish'.The DataBall is instantiated at the beginning of the game and closed 
    at the end. During this time, DataBall is collecting specific measurements about
    the game.
    
    The class is divided into two parts, methods used in game and methods used 
    in order to query statistics. 
    
    Current list of statistics offered: 
        -Games played
        -games won by user (lost by user)
        -average number of cards dealt per request per game 
        -Longest/shortest game (time/turns)
        -Average number of turns
        -Average time played per game
        -Longest streak of guesses resulting in 'Go Fish' (empty guesses)
            - out of all games
            
        -Average value for longest streaks of empty guesses
       
"""

    def __init__(self,difficulty=0):
         
        """
        DataBall constructor, connect to the go_fish database, define a cursor,
        and get the start time of the game. Initialize several other fields used in the database.
        8
        Parameters:         data type   purpose
        
            difficulty         int      assign integer value to difficulty field
        ------------------------------------------------------------------------
        
        Fields:             data type             purpose
        
        conn                sqlite3 connection    connect to database
        ------------------------------------------------------------------------
        curs                sqlite3 cursor        manipulate/query database
        ------------------------------------------------------------------------
        ts                  datetime              start time of game
        ------------------------------------------------------------------------
        won                 int                   boolean integer value 
                                                  (1 for win, 0 for loss)
        ------------------------------------------------------------------------
        cards_per_request   int                   running total for both players
                                                  of number of cards recieved upon
                                                  request     
        ------------------------------------------------------------------------
        turn_number         int                   incrementer on number of turns 
        ------------------------------------------------------------------------
        difficulty          int                   number indicating opponent difficulty
        ------------------------------------------------------------------------
        empty_guesses       int                   running streak of turns that recieved
                                                  no cards from the opponent
        ------------------------------------------------------------------------  
        top_empty_guess_ct  int                   highest streak of guesses that
                                                  recieve 0 cards
        ------------------------------------------------------------------------                             
                                        
        """
        self.conn = sqlite3.connect('go_fish.db') #Connect to database
        self.curs = self.conn.cursor()
        
        # start time of game
        self.ts  = datetime.datetime.now()
        
        # initialize other fields/qualifiers of the game
        self.won = None
        self.cards_per_request = 0
        self.turn_number = 1
        self.difficulty = difficulty
        
        # 'empty guess' tracking variable- an empty guess is a guess for which the 
        #  player had to 'go fish'
        self.empty_guesses = 0
        self.top_empty_guess_ct = 0
    
    
################################################################################
############################## In Game Methods #################################
################################################################################
    
    def close(self,win=0):
        
        """
        Close all counting processes, run final calculations, and write information
        to the database 
        
        Parameters:         data type   purpose
        
            win                int      act as boolean (1 for win, 0 for loss)
                                        used as integer for sqlite3 data type constraints
                                        and future computational ease.
        ------------------------------------------------------------------------                                
        
        """
        # get time past during game
        elapsed         = datetime.datetime.now() - self.ts
        # convert timestamps to strings (hour:minute:second - day/month/year)
        elapsed_str     = str(elapsed)
        ts_str          = self.ts.strftime("%H:%M:%S - %d/%m/%Y")
        
        # computer average number of cards per request
        avg_per_request = self.cards_per_request/self.turn_number    
        
        # check one last time for empty guess streak
        if (self.empty_guesses > self.top_empty_guess_ct):
                self.top_empty_guess_ct = self.empty_guesses
        
        # write game stats to database
        self.curs.execute("INSERT INTO game_stats (ts_begin,ts_elapsed, user_win,"+
                          "longest_draw, avg_per_request, difficulty,num_turns)"+
                          " VALUES (?,?,?,?,?,?,?)",(ts_str,elapsed_str,win,
                                                   self.top_empty_guess_ct,
                                                   avg_per_request, 
                                                   self.difficulty,
                                                   self.turn_number))
                                                   
        # commit the changes
        self.conn.commit()
        
        # close connection to database
        self.conn.close()
        
    def hard_close(self):
        """
        Close the DataBall class without saving anything to the database.
        
        """
        
        self.conn.close()
        
        
    def update(self,cards_on_req=0):
        
        """
        Called at the end of each turn. Increments the turn count and adds to the
        sum of cards on request. Increments/resets empty guess streak.
        
        Parameters:         data type   purpose
        
          cards_on_req         int      add to the sum of cards recieved on request
          ------------------------------------------------------------------------
                          
        """
        
        # increment streak if guess is empty
        if (cards_on_req==0):
            self.empty_guesses += 1
        
        # otherwise check for a new max streak
        else:
    
            if (self.empty_guesses > self.top_empty_guess_ct):
                self.top_empty_guess_ct = self.empty_guesses
            
            self.empty_guesses = 0
        
        # increment number of cards per request and turn number
        self.cards_per_request += cards_on_req
        self.turn_number += 1
    
################################################################################
########################## Statistics Methods ##################################
################################################################################
    
    def games_played(self,difficulties=[0,1,2]):
        """
        Get the total number of games for the specified difficulties.
        
        Parameters:         data type   purpose
        
            difficulties    list      specified difficulties to query
        ------------------------------------------------------------------------
        
        """
        
        total = 0
        for diff in difficulties:
            # query database for these difficulties
            self.curs.execute("SELECT * FROM game_stats WHERE difficulty = ?",(str(diff),))
            total += len(self.curs.fetchall())
        
        return total
    
    def games_won(self,difficulties=[0,1,2]):
        """
        Get the total number of games won by the user for the specified difficulties.
        
        Parameters:         data type   purpose
        
            difficulties    list      specified difficulties to query
        ------------------------------------------------------------------------
        """
        total = 0
        for diff in difficulties:
            # query database
            self.curs.execute("SELECT user_win FROM game_stats WHERE difficulty = ?",(str(diff),))
            
            # get sum of wins for that difficulty
            for row in self.curs.fetchall():
                total+=row [0]
        
        return total
    
    def win_loss_ratio(self,difficulties=[0,1,2],choice='win'):
        """
        Compute the win/overall or loss/overall ratios for game stored in the database
        for a given set of difficulties.
        
         Parameters:         data type   purpose
         
            difficulties     list      specified difficulties to query 
        ------------------------------------------------------------------------
        """
        if (choice == 'win'):
            return self.games_won(difficulties)/self.games_played(difficulties)
        
        return (self.games_played(difficulties) - self.games_won(difficulties)/self.games_played(difficulties))
        
    def average_avg_per_req(self,difficulties=[0,1,2]):
        """
         Compute and return the average of the average number of cards per request per game
         for a given set of difficulties.
        
         Parameters:         data type   purpose
         
            difficulties     list      specified difficulties to query 
        ------------------------------------------------------------------------
    
        """
        avgs = []
        
        for diff in difficulties:
            # query database
            self.curs.execute("SELECT avg_per_request FROM game_stats WHERE difficulty = ?",(str(diff),))
            
            for avg in self.curs.fetchall():
                avgs.append(avg[0])
            
        return sum(avgs)/len(avgs)
        
    def superlative_game_len(self,time_metric,superl, difficulties=[0,1,2]):
        """
        
        Compute the max/min game length for some set of difficulties under one 
        of two time metrics (number of turns or traditional time) for a given
        superlative (aka max or min)
        
        Parameters:         data type   purpose
            
            time_metric      string     denote whether to measure in 'turns' or 'tradit'
                                        'num_turns'  --->  turn wise duration
                                        'ts_elapsed' --->  traditional time scale
        ------------------------------------------------------------------------
            superl           string     denote whether to take max or min of set
                                        'max'    --->  maximum
                                        'min'    --->  minimum
        ------------------------------------------------------------------------
            difficulties     list       specified difficulties to query 
        ------------------------------------------------------------------------
        Returns:
            superl_elt  <---- the longest/shortest game, temporally/turnwise and
                              its corresponding timestamp
            
        """
        time_metrics = {1:'num_turns',2:'ts_elapsed'}
        time_metric  = time_metrics[time_metric]
        
        superls = {1:'min',2:'max'}
        supel   = superls[superl]
        
        # dictionary to map timestamps ---> game durations
        times = dict()
        
        # validate parameter input
        if (time_metric in ['num_turns','ts_elapsed'] and superl in ['max','min']):
            
            # iterate through difficulties and query database for desired values
            for diff in difficulties:
                self.curs.execute("SELECT {}, ts_begin FROM game_stats WHERE difficulty = ?".format(time_metric),(diff,))
                
                # map each timestamp to its game duration
                for time in self.curs.fetchall():
                    times[time[1]] = time[0]
            
            #isolate timestamps
            keys = [k for k in times.keys()]
            
            #define a superlative element to compare against
            superl_elt = [times[keys[0]],keys[0]]
            
            # iterate through timestamps, check if its corresponding duration
            # is greater or less than superl_elt
            for k in keys:
                if superl == 'max': # <--- max case
                    print(times[k])
                    if times[k] > superl_elt[0]:
                       superl_elt = [times[k],k]
                
                else: # <---- min case
                    if times[keys[k]] < superl_elt[0]:
                        superl_elt = [times[k],k]
            
            return superl_elt #return the superlative (min/max) element
            
        else: # <--- display error message
            print("Time metric or superlative incorrectly specified!\n"+
                  "Time metric:\n"+
                  "- 'ts_elapsed' ---> traditional temporal duration"+
                  "- 'num_turns'  ---> turn-wise duration")
    
    def avg_game_len(self,time_metric,difficulties=[0,1,2]):
        """
        Compute and return the average game length (in temporal time or turnwise)
        over a specific domain of difficulties.
        
         Parameters:         data type   purpose
            
            time_metric      string     denote whether to measure in 'turns' or 'tradit'
                                        'num_turns'  --->  turn wise duration
                                        'ts_elapsed' --->  traditional time scale
        ------------------------------------------------------------------------
            difficulties     list       specified difficulties to query 
        ------------------------------------------------------------------------
        
        """
        time_metrics = {1:'num_turns',2:'ts_elapsed'}
        time_metric  = time_metrics[time_metric]
        
        total       = 0 # running total of times
        total_games = 0 # number of games
        
        if (time_metric in ['num_turns','ts_elapsed']):
            # iterate through difficulties and query database for desired values
            for diff in difficulties:
                self.curs.execute("SELECT {} FROM game_stats WHERE difficulty = ?".format(time_metric),(diff,))
                games = [l[0] for l in self.curs.fetchall()]
                
                total         += sum(games)
                total_games   += len(games)
                
        return total/total_games
        
        
    def longest_streak(self,overall=False,difficulties=[0,1,2]):
        """
        
        Find the overall longest streak of empty guesses for a given domain of difficulties
        
        OR
        
        Find the longest streak of empty guesses for the current game.
        
        Parameters:         data type   purpose
            
            overall          boolean    denote whether to report the overall longest
                                        or longest in current game 
                                        (overall=True => report overall)
                                      
        ------------------------------------------------------------------------
            difficulties     list       specified difficulties to query 
        ------------------------------------------------------------------------
        
        Returns:
            the maximum length of a streak and the time stamp of the game.
        
        """
        if (overall): # if overall specified, query database and find max
            
            streaks = []  
            for diff in difficulties: # iterate through difficulties, query db and 
                                      # append fetched data to a list of streaks
                                      
                self.curs.execute("SELECT longest_draw,ts_begin FROM game_stats WHERE difficulty = ?",
                                      (diff,))
                                      
                streaks+=self.curs.fetchall() # append
            
            max_streak = max(streaks) # find overall max
            
            return max_streak
            
        return self.top_empty_guess_ct # eitherwise return the current max streak
        
        
    def avg_streak(self,difficulties=[0,1,2]):
        """
        
        Compute and return the average length of max empty guess streaks for 
        a given domain of difficulties.
        
        Parameters:         data type   purpose
            
            difficulties     list       specified difficulties to query 
        ------------------------------------------------------------------------
        
        """
        streaks = []
        for diff in difficulties:
            
            self.curs.execute("SELECT longest_draw FROM game_stats WHERE difficulty = ?",(diff,))
            streaks+=[l[0] for l in self.curs.fetchall()]
            
        return sum(streaks)/len(streaks)
            
################################################################################
############################ Statistics Center #################################                    
################################################################################                    
            
    def stats_center(self):
        """
        A method to service statistics queries off the database. 
        Validates input unless an egregious mistake is made, in which case
        the statistics center is closed and the user is returned to the main loop
        
        --ABOUT 90% FINISHED--
        
        --- need to have the rest of the game fully functional before being able to finish
        
        Design:
            
            -Command line input from sequence of menus
            -Enter query selections as comma separated list
            -Enter difficulty domain as comma sep. list
            -Displays stats in a pretty way then asks user if they want to
                    -a see the menu again and query more stats
                    -or return to home
            
            ** Stats are displayed by iterating through the queries list
             and calling the appropriately following the condition tree 
             associated with the query on the menu
             
            
            
        So far i have finished valdating
        """
        
        # opening header for stats center
        title_str = "\n**Welcome to your Go Fish Statistics Center**\n" 
        
        keep_going = [1]
        
        while keep_going[0] == 1:
            menu      = "*-------------------------------------------*\n"+\
                        "|              *~Stats Menu~*               |\n"+\
                        "|               ------------                |\n"+\
                        "|-------------------------------------------|\n"+\
                        "| 1 - Games Played                          |\n"+\
                        "|-------------------------------------------|\n"+\
                        "| 2 - Games Won by user                     |\n"+\
                        "|-------------------------------------------|\n"+\
                        "| 3 - Average cards dealt per turn overall  |\n"+\
                        "|-------------------------------------------|\n"+\
                        "| 4 - Longest/Shortest Game in time         |\n"+\
                        "|     - by minutes, seconds, etc..          |\n"+\
                        "|     - by turns                            |\n"+\
                        "|-------------------------------------------|\n"+\
                        "| 5 - Average game length                   |\n"+\
                        "|     - by minutes, seconds, etc..          |\n"+\
                        "|     - by turns                            |\n"+\
                        "|-------------------------------------------|\n"+\
                        "| 6 - Longest # turns where no cards traded |\n"+\
                        "|     out of all games                      |\n"+\
                        "|-------------------------------------------|\n"+\
                        "| 7 - Average # turns where no card traded  |\n"+\
                        "|-------------------------------------------|\n"+\
                        "| 8 - back to home                          |\n"+\
                        "|                                           |\n"+\
                        "*-------------------------------------------*"
            
            print(title_str)       
            print(menu)
            LONGEST_SHORTEST = 4
            AVG_GAME_LEN = 5
            # attempt to get the desired menu choices of the user, validate the input
            # in the case of an egregious exception, return to the main loop
            try:
                menu_choices = str(input("** Please enter query choices as comma separated list: "))
                # comes in as string representation of a tuple ^^ 
                                                                                
                menu_choices = menu_choices.rstrip(")").lstrip("(")  # <-- peel off ( and ) from tuple
                
                # split into a list based on the ',' as a separating value,
                # make set into iterable object (list)
                queries = list(q for q in menu_choices.split(",")) 
                
                # validate the user's input
                queries = self.validate_input(queries,'menu option')
                
                # remove duplicates
                queries = list(set(q for q in queries))
                
                # if the user chose 8 (to return to home), find out if they want to
                # do so now or after displaying all statistics
                queries,ret = self.chosen_8(queries)
                if (ret):
                    return
                
                superl = 1
                time_metric = 1
                time_metric_2 = 1 
                if LONGEST_SHORTEST in queries:
                    print("You entered [ 4 - Longest/Shortest Game ]\n"+\
                        "Do you want the longest game (1) or shortest game (2)")
                    superl = [input("Longest, shortest or both? : ")]
                    superl = self.validate_input(superl,'option')
                    
                    print("Do you want this in turns (1) or time (2)")
                    time_metric = [input("Turns or time? : ")]
                    time_metric = self.validate_input(time_metric,'option')
                
                if AVG_GAME_LEN in queries:
                    print("You entered [ 5 - Average Game Length]\n"+\
                        "Do you want the length in turns (1) or time (2)")
                    time_metric_2 = [input("Turns or time : ")]
                    time_metric_2 = self.validate_input(time_metric_2,'option')
                    
                #difficulty menu
                diff_menu=  "\n"+\
                            "*-------------------------------------------*\n"+\
                            "|            *~Difficulty Menu~*            |\n"+\
                            "|-------------------------------------------|\n"+\
                            "|0 - Simple                                 |\n"+\
                            "|-------------------------------------------|\n"+\
                            "|1 - Smart                                  |\n"+\
                            "|-------------------------------------------|\n"+\
                            "|2 - Devious                                |\n"+\
                            "*-------------------------------------------*"
        
                print(diff_menu)
                # get the domain of difficulties user wants to get stats on
                diffs = str(input("** enter difficulties (comma separated) you want stats on: "))
                diffs = diffs.rstrip(")").lstrip("(")
                    
                # split into list, validate input, and remove duplicates
                diffs = diffs.split(',')
                diffs = self.validate_input(diffs,'difficulty')
                diffs = list(set(diffs))
                
                # maps for string formatting
                times = {1:'turns',2:'time'}
                superls = {1:'Highest',2:'Lowest'}
                
                print('======= GAME STATISTICS REPORT =======')
                
                for q in queries: # execute each query
                    
                    if q == 1:
                        print('Games played by user: {}'.format(self.games_played(difficulties=diffs)))
                        
                    elif q == 2:
                        print('Games won by user: {}'.format(self.games_won(difficulties=diffs)))
                    
                    elif q == 3:
                        print('Average # cards dealt per turn: {}'.format(self.average_avg_per_req(difficulties=diffs)))
                    
                    elif q == 4:
                        print('{} game length ({}): {}'.format(superls[superl],times[time_metric[0]],self.superlative_game_len(time_metric[0],superl[0],difficulties=diffs)))
                    
                    elif q == 5:
                        print('Average game length ({}): {}'.format(times[time_metric_2[0]],self.avg_game_len(time_metric_2[0],difficulties=diffs)))
                    
                    elif q == 6:
                        print('Longest streak of zero-trade turns: {}'.format(self.longest_streak(difficulties=diffs)))
                    
                    elif q == 7:
                        print('Average number of turns with zero trades: {}'.format(self.avg_streak(difficulties=diffs)))
                        
                    elif q == 8:
                        print('Exiting game center!')
                        return
                        
                keep_going = [input('Do you want to get more stats (1) or keep going (2)? : ')]       
                keep_going = self.validate_input(keep_going,'option')
                
            except Exception as e:
                print('Oops! an error occurred, sending back to main menu...')
                print(e)
                return
           
    def validate_input(self,elts,c):
        """
        Validate the elements of a list as integers.
        
        Parameters      data type       purpose
        ------------------------------------------------------------------------
         elts             list          the list of (string) elements to be verified as integers
        ------------------------------------------------------------------------
         c                string        either 'difficulty', 'menu option',
                                        'option for returning',or 'option' used for formatting
                                        the validation message and verifying input
        
        ** values of 'difficulty' and 'menu option' are self explanatory
            'option for returning' --> validates input coming from chosen_8
            'option' -> validates general input for the shortest/longest game in turns/time
                                
        """
        
        # choice dictionary used to format validation message
        choices = {'difficulty':'0 and 2',
                   'menu option':'1 and 8',
                   'option for returning':'1 and 2',
                   'option':'1 and 2'}
        
        # iterate throughout list
        for i in range(len(elts)):
            
            #attempt to verify the element as integer
            try:
                
                elts[i] = int(elts[i])
                
                # dictionary of conditions to be compared against the 
                # elements that are not yet integers
                #
                # Ex:
                # Suppose elts[i] = '12' and c = 'menu option'. 
                #
                # Then condits[c] = False. This will raise an
                # exception, forcing a while loop (line 558) to get good input.
            
                condits = {'difficulty':elts[i] in [n for n in range(3)],
                       'menu option':elts[i] in [n for n in range(1,9)],
                       'option for return':elts[i] in [1,2],
                       'option':elts[i] in [1,2]}
                       
                if condits[c]:
                    pass
                    
                else:
                    raise NameError
                    
            except NameError: # if element fails to be verified

                while not condits[c]: # as long as the input is not valid, keep asking
                                      # for input
                    
                    # formatted validation message
                    print("{} is not an option. Choose a(n) {} between {}.".format(elts[i],c,choices[c]))
                    
                    # get more input
                    elts[i] = input('Enter option : ')
                    
                    # update conditions dictionary
                    condits = {'difficulty':elts[i] in [n for n in range(3)],
                       'menu option':elts[i] in [n for n in range(1,9)],
                       'option for return':elts[i] in [1,2],
                       'option':elts[i] in [1,2]}
                       
            # cast this validated input as an int
            elts[i] = int(elts[i])
        
        return elts
        
    def chosen_8(self,queries):
        
        """
        Find out if the return command (option 8) has been called off the menu. If so,
        ask the user if they would like to display the statistics or go back to the home
        loop.
        
        Parameters      data type       purpose

        queries         list            the list of commands that may or may not 
                                        contain 8
        ------------------------------------------------------------------------
        
        """
        if 8 in queries: #check if user will want to return
            
            if len(queries) != 1: # if user entered more than just 8, check if 
                                  # want to execute the other commands
                                  
                print("\nYou entered [ (8) - back to home ] as an option\n"+\
                        "Would you like to go back now or after the other queries?")
                
                quit = [input("Type 1 for 'now' or 2 for 'later' and press enter: ")]
                
                # validate the input
                quit = self.validate_input(quit,'option for return')
                
                if quit[0] == 1: # if user wants to leave now, return true to
                                 # quit out of stats_center
                                 
                    return queries,True
                    
                else: #otherwise move return to home to the back of the list
                    ind_8 = queries.index(8)
                    temp = queries[len(queries)-1]
                    queries[len(queries)-1] = 8
                    queries[ind_8] = temp
            
            else: # if 8 is the only command, return to true to leave 
                  # stats_center
                return queries,True
        
        # if 8 not in queries, just leave this method
        return queries,False

d1=DataBall()
d1.stats_center()