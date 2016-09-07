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
    DB = connect()
    c = DB.cursor()
    query = 'DELETE FROM matches;'
    c.execute(query)
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    query = 'DELETE FROM players CASCADE;'
    c.execute(query)
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    query = 'SELECT COUNT(*) FROM players;'
    c.execute(query)
    cnt = c.fetchall()[0][0]
    DB.close()
    return cnt


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    query = "INSERT INTO players (name) VALUES ('%s');" % name
    c.execute(query)
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first
    place, or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    DB = connect()
    c = DB.cursor()
    # use a left join to capture zero wins
    query = """ select players.id, players.name, count(a.winner) as wins,
    count(a.winner) + count(b.loser) as matches from players
    left join matches as a on players.id=a.winner
    left join matches as b on players.id=b.loser
    group by players.id order by wins DESC; """
    c.execute(query)
    return c.fetchall()
    DB.close()


def validMatch(playerid_1, playerid_2):
    """ rematches not allowed: a pair is only valid if two players have not
    played each other before. Return true if pair is valid """
    DB = connect()
    c = DB.cursor()
    query = """ SELECT winner, loser from matches
    WHERE (winner=%s AND loser=%s)
    OR (winner=%s AND loser=%s);"""
    c.execute(query, (playerid_1, playerid_2, playerid_2, playerid_1))
    matches = c.rowcount
    DB.close()
    if matches > 0:
        return False
    return True


def checkPairing(playerid_1, playerid_2, standings):
    """
    playerid_2 is potential match for playerid_1
    standings is the standings table. if the pair is valid,
    return playerid_2, else run through the  standings list
    until a match is found
    """
    if playerid_2 >= len(standings):
        return playerid_1
    elif validMatch(standings[playerid_1][0], standings[playerid_2][0]):
        return playerid_2
    else:
        return checkPairing(playerid_1, playerid_2 + 1, standings)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);" % (
        winner, loser)
    c.execute(query)
    DB.commit()
    DB.close()


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
    pairings = []
    standings = playerStandings()
    while len(standings) > 1:
        # match top players in the standings table until list is empty
        validMatch = checkPairing(0, 1, standings)
        player1 = standings.pop(0)
        player2 = standings.pop(validMatch - 1)
        pairings.append((player1[0], player1[1], player2[0], player2[1]))
    return pairings
