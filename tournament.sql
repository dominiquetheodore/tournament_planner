-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (ID SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE matches (ID SERIAL PRIMARY KEY, winner INTEGER REFERENCES players (ID), loser INTEGER REFERENCES players (ID));

-- helpful views to check out query results

CREATE VIEW standings as select players.id, players.name, count(a.winner) as wins, count(a.winner) + count(b.loser) as matches from players left join matches as a on players.id=a.winner left join matches as b on players.id=b.loser group by players.id order by wins DESC;
