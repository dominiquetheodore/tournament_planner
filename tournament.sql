-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c tournament

DROP TABLE players, matches CASCADE;

CREATE TABLE players (ID SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE matches (ID SERIAL PRIMARY KEY, winner INTEGER REFERENCES players (ID), loser INTEGER REFERENCES players (ID));

CREATE VIEW standings as select players.id, players.name, count(a.winner) as wins, count(a.winner) + count(b.loser) as matches from players left join matches as a on players.id=a.winner left join matches as b on players.id=b.loser group by players.id order by wins DESC;

CREATE VIEW win_total as SELECT players.name, count(players.name) as win_total from players, matches WHERE players.id=matches.winner group by players.name order by win_total desc;