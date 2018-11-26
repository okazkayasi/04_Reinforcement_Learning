# SoccerWorld

by Rocko Graziano, RockoGraziano@gatech.edu

Recreates the two-player markov soccer game as propsed by Littman and used to demonstrate
multi-agent reinforcement learning.

All rights reserved, no guarentees that it works.

## SoccerWorld.py

This is the markov game framework.  It includes classes for the game and the players.

To initialize the game call  **YourGame = SoccerWorld.game( variables )**  where the variables are as follows:
 * verbose   -->  True/False  enables logging
 * rows=n, columns=n --> Define size of pitch (game field)
 * goalRstart=n, goalRend=n -->  Define which rows the goal covers
 * aGoal=n, bGaol=n -->  define the column for the goal.  Note these may be outside the pitch
 * aPosition=[r,c], bPosition=[r,c] -->  Define starting position for players

The primary methods for interaction are:
* game.reset() - put players back to initial state, randomly select possession, returns state of two players
* game.availableMoves() - returns list of move descriptions
* game.numActions() - returns the number of legal actions
* game.numStates() - returns the number of states.  Location on grid; if player has possession this (rows*columns) is added to the location
* game.printgrid() - displays the current game state
* game.move(moveA, moveB) - accepts two moves, executes move, returns subsequent state and rewards

The default values create the game as described by Littman.

## testSoccer.py

An example program, two players go at it with random moves

python testSoccer.py littman|greenwald  [verbose] [graphic]

