
"""
AUTHOR: Dan Berenberg
"""
import sqlite3 # database module
import sys,os  # overwrite checking

class BuildDB:
    
    """
    Build a database that stores game statistics for a game of go fish. 
    
    """    
    
    # initialize build process
    def __init__(self):
    
        # name the database
        db_wrapper = 'go_fish.db'
        
        # if the database file exists, exit so there's no overwrite.
        if os.path.exists(db_wrapper):
            sys.exit('Database already exists!')
            
        # otherwise create the file
        conn = sqlite3.connect(db_wrapper)
        curs = conn.cursor()
        
        # build a table inside database called game_stats
        # game_stats consists of
        #    - a time_stamp (time started game)
        #    - a boolean value indicating whether the user won the game
        #    - longest draw streak count (longest streak of turns where a player had to "go fish"
        #    - average card yield per request from either player
        #    - a string that denotes the difficulty of the computer
    
        curs.execute("CREATE TABLE game_stats (ts_begin text, ts_elapsed text, user_win int,"+
                                         "longest_draw int, avg_per_request real,"+
                                         "difficulty text,num_turns int)")
    
        #commit to the changes
        conn.commit()
    
        #load in default db values for each difficulty
        
        #diff 0
        ts = "00:00:00 - 2/13/2017"
        ts_elapsed = '0:00:00 - 2/13/2017'
        user_win = 0
        longest_draw = 1
        avg_per_request = 1
        difficulty = 0
        num_turns = 0
        
        #diff 1
        ts1 = "00:00:00 - 2/13/2017"
        ts_elapsed1 = '0:00:00 - 2/13/2017'
        user_win1 = 0
        longest_draw1 = 1
        avg_per_request1 = 1
        difficulty1 = 1
        num_turns1 = 0
        
        #diff 2
        ts2 = "00:00:00 - 2/13/2017"
        ts_elapsed2 = '0:00:00 - 2/13/2017'
        user_win2 = 0
        longest_draw2 = 1
        avg_per_request2 = 1
        difficulty2 = 2
        num_turns2 = 0
        
        curs.execute("INSERT INTO game_stats (ts_begin,ts_elapsed, user_win,"+
                            "longest_draw, avg_per_request, difficulty,num_turns)"+
                            " VALUES (?,?,?,?,?,?,?)",(ts,ts_elapsed,user_win,longest_draw,avg_per_request,difficulty,num_turns))
        
        curs.execute("INSERT INTO game_stats (ts_begin,ts_elapsed, user_win,"+
                            "longest_draw, avg_per_request, difficulty,num_turns)"+
                            " VALUES (?,?,?,?,?,?,?)",(ts1,ts_elapsed1,user_win1,longest_draw1,avg_per_request1,difficulty1,num_turns1))
        
        curs.execute("INSERT INTO game_stats (ts_begin,ts_elapsed, user_win,"+
                            "longest_draw, avg_per_request, difficulty,num_turns)"+
                            " VALUES (?,?,?,?,?,?,?)",(ts2,ts_elapsed2,user_win2,longest_draw2,avg_per_request2,difficulty2,num_turns2))
        conn.commit()
        
        #close the connection
        conn.close()