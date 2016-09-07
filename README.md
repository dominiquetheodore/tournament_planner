# Tournament Planner
Database schema and functions to keep track of matches and players in a "Swiss Tournament"      
This project was submitted in fulfilment of the requirements for the Intro to Relational Databases course,
which is part of Udacity's Full Stack Developer Nanodegree. 

## Installation
1. Install [Vagrant](http://vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)
2. Power up your Vagrant machine using the command `vagrant up`. Connect with `vagrant ssh`
3. Clone the contents of this repository into your vagrant folder.
4. Create tables using the command `psql -f tournament.sql`
5. Run tournament_test.py against the database to test the functions in tournament.py


## Files

### tournament.py
contains all the functions to keep track of Swiss-system tournament

### tournament.sql
table definitions for the tournament

### tournament_test.sql
test functions for tournament.sql, provided by Udacity


## Functions

The following functions are part of the tournament.py file:

### connect()
connect to the PostgreSQL database and returns a database connection

### deleteMatches()
remove all matches from the database

### deletePlayers()
remove all players from database

### countPlayers()
returns number of players currently registered

### registerPlayer()
adds a player to the database

### playerStandings()
generates a table of players listed sorted by wins. returns a list of tuples each containing player's id, his name, how many matches he has won, and how many matches he has played

### validMatch()
checks if two players have played each other before to prevent rematches


###checkPairing()
jk

### reportMatch()
record the outcome of a match in the matches table

### swissPairings()
returns a list of pairs of players for the next match. Each player is paired with the one closest to him in the standings. In this implementation, it is assumed that there is an even number of players. All players participate in each round, and no rematches are allowed.

## Output
	vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
	1. countPlayers() returns 0 after initial deletePlayers() execution.
	2. countPlayers() returns 1 after one player is registered.
	3. countPlayers() returns 2 after two players are registered.
	4. countPlayers() returns zero after registered players are deleted.
	5. Player records successfully deleted.
	6. Newly registered players appear in the standings with no matches.
	7. After a match, players have updated standings.
		8. After match deletion, player standings are properly reset.
	9. Matches are properly deleted.
	10. After one match, players with one win are properly paired.
	Success!  All tests pass!

