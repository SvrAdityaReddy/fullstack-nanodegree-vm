#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB=psycopg2.connect("dbname=tournament")
    cur=DB.cursor()
    cur.execute("UPDATE registry set no_matches=0,win=0,loss=0");
    DB.commit();
    DB.close();

def deletePlayers():
    """Remove all the player records from the database."""
    DB=psycopg2.connect("dbname=tournament")
    cur=DB.cursor()
    cur.execute("delete from registry")
    DB.commit();
    DB.close();

def countPlayers():
    """Returns the number of players currently registered."""
    DB=psycopg2.connect("dbname=tournament")
    cur=DB.cursor()
    cur.execute("select count(*) as num from registry")
    row=cur.fetchall();
    #print row
    DB.close();
    return row[0][0];

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB=psycopg2.connect("dbname=tournament")
    cur=DB.cursor()
    cur.execute("insert into registry (name,no_matches,win,loss) values (%s,0,0,0)",(name,));
    DB.commit();
    DB.close();

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB=psycopg2.connect("dbname=tournament")
    cur=DB.cursor()
    cur.execute("select id,name,win,no_matches from registry order by win Desc");
    rows=cur.fetchall();
    list_tuples=[(row[0],row[1],row[2],row[3]) for row in rows]  
    DB.commit();
    DB.close();
    return list_tuples

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB=psycopg2.connect("dbname=tournament")
    cur=DB.cursor()
    cur.execute("UPDATE registry set no_matches=no_matches+1,win=win+1 where id=(%s)",(winner,));
    cur.execute("UPDATE registry set no_matches=no_matches+1,loss=loss+1 where id=(%s)",(loser,));
    DB.commit();
    DB.close();    


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB=psycopg2.connect("dbname=tournament")
    cur=DB.cursor()
    cur.execute("select id,name from registry order by win Desc");
    rows=cur.fetchall();
    length=len(rows)
    i=0;
    list_=[]
    while(i < length):
        tuple_=(rows[i][0],rows[i][1],rows[i+1][0],rows[i+1][1])
        list_.append(tuple_)
        i=i+2
    #print length;
    #print rows;
    #print list_;
    DB.commit();
    DB.close();
    return list_;

#print(countPlayers());
#registerPlayer("super hero");
#registerPlayer("hero");
#deletePlayers();
#reportMatch(7, 8);
#print(playerStandings());
#swissPairings();