# SoccerWorld.py
#
# implements the two-player game proposed by Littman & used by Greenwald
#
# OMSCS - Reinforcement Learning, Fall 2018
# Rocko Graziano, rockograziano@gatech.edu

# future enhancements
#    -- allow for > 2 players (aka teams)
#
# assumptions
#    -- random choice which player begins with the ball
#    -- random choice which player moves first
#    -- play continues until a goal is scored
#    -- +100 to score a goal, -100 to score a wrong goal;  opponent receives opposite reward
#    -- players cannot stand in a goal  [no longer true with V1.1 and beyond]
#    -- if a player with possession bumps into other player, the ball changes hands
#    -- if both players move toward the same square (state), 
#            the first player will end up with the ball
#    -- if two players abut and move toward eachother, the first player ends up with the ball
#
# change log
#    V1.1 -- fixed calculation of state
#    V1.2 -- adapting to allow standing in goal (greenwald)
#    V1.3  -- maybe fixed unicode format errors

import random
import numpy as np

class player:
    def __init__(self, name, x, y, goal):
        self.name = name
        self.x = x
        self.y = y
        self.goal = goal
        self.possession = False

    def displayName(self):
        if self.possession:
            # return "\033[1;4m{}\033[0m".format(self.name)
            if self.name == "A":
                return 'A'
            else:
                return 'B'
        else:
            return self.name

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setPosession(self, possession):
        self.possession = possession

class game:
    def __init__(self, verbose, rows=4, columns=5, goalRstart=1, goalRend=2, aGoal=-1, bGoal=5, aPosition=[1,3], bPosition=[2,1]):
        self.rows = rows       # define size of field
        self.columns = columns
        self.goalRstart = goalRstart
        self.goalRend = goalRend
        self.aGoal = aGoal
        self.bGoal = bGoal
        self.playerA = []
        self.playerB = []
        self.aPosition = aPosition
        self.bPosition = bPosition
        self.verbose = verbose
        self.legalMoves = ['N', 'S', 'E', 'W', 'stick']
        self.gameBoard = np.empty((self.rows, self.columns), dtype='str')
        self.gameBoard[:,:] = ' '


    def availableMoves(self):
        return self.legalMoves

    def numActions(self):
        return len(self.legalMoves)

    def numStates(self):
        return (self.columns * self.rows * 2)

    def possession(self):
        if self.playerA.possession:
            return self.playerA.name
        else:
            return self.playerB.name

    def playerState(self, thePlayer):
        state = (thePlayer.x * self.columns) + thePlayer.y
        if thePlayer.possession: state = state + (self.columns*self.rows)
        return state

    def reset(self):
        self.playerA = player("A", self.aPosition[0], self.aPosition[1], "W")
        self.playerB = player("B", self.bPosition[0], self.bPosition[1], "E")

        if random.random() > 0.5:
            self.playerA.setPosession(True)
        else:
            self.playerB.setPosession(True)

        if self.verbose:
            print ("Soccer Game Reset with Initial Posession by {}".format(self.possession()))

        state = [self.playerState(self.playerA), self.playerState(self.playerB)]
        return state

    def printgrid(self):
        for r in range(self.rows):
            if r >= self.goalRstart and r <= self.goalRend:
                print ("#", end=" ")
            else:
                print (" ", end=" ")
            for c in range(self.columns):
                if self.playerA.x == r and self.playerA.y == c:
                    print (self.playerA.displayName(), end=" ")
                elif self.playerB.x == r and self.playerB.y == c:
                    print (self.playerB.displayName(),end=" ")
                else:
                    print ('-', end=" ")
            if r >= self.goalRstart and r <= self.goalRend:
                print ("#")
            else:
                print
                
        print (self.playerA.possession)

    def movePlayer(self, thePlayer, theOpponent, action):
        score = 0

        if   action == 0:   # north
            newX = max(0, thePlayer.x - 1)
            newY = thePlayer.y
        elif action == 1:   # south
            newX = min(self.rows-1, thePlayer.x+1)
            newY = thePlayer.y
        elif action == 2:   # east
            newX = thePlayer.x
            newY = thePlayer.y+1 # min(thePlayer.y+1, self.columns-1)
        elif action == 3:   # west
            newX = thePlayer.x
            newY = thePlayer.y-1 # max(0, thePlayer.y-1)
        else:               # stand
            newX = thePlayer.x
            newY = thePlayer.y

        # check for collision

        strResults = ""

        if newX == theOpponent.x and newY == theOpponent.y:
            if self.verbose: strResults += " Collision!"
            newX = thePlayer.x
            newY = thePlayer.y
            if thePlayer.possession:
                if self.verbose: strResults += " Steal!"
                thePlayer.setPosession(False)
                theOpponent.setPosession(True)

        # check for goal

        if newY == self.aGoal:
            if thePlayer.possession and (newX >= self.goalRstart and newX <= self.goalRend):
                if thePlayer.goal == "W":
                    if self.verbose: strResults += " GOOOOOAL!"
                    score = 100
                else:
                    if self.verbose: strResults += " WRONG GOAL!"
                    score = -100

        if newY == self.bGoal:
            if thePlayer.possession and (newX >= self.goalRstart and newX <= self.goalRend):
                if thePlayer.goal == "E":
                    if self.verbose: strResults += " GOOOOOAL!"
                    score = 100
                else:
                    if self.verbose: strResults += " WRONG GOAL!"
                    score = -100


        # set new location, bump back onto field if necessary

        if newY == -1: newY = 0
        if newY == self.columns:  newY = self.columns-1

        thePlayer.setPosition( newX, newY)

        if self.verbose:
            print ("Moved Player {} via action {:5s} to state {} {}".format(thePlayer.name, self.legalMoves[action], self.playerState(thePlayer), strResults))

        return score

    def move(self, actionPlayerA, actionPlayerB):
        if random.random() > 0.5:
            firstMove = "A"
        else:
            firstMove = "B"

        if self.verbose:
            # print "A: {}  B:  {}".format(self.legalMoves[actionPlayerA], self.legalMoves[actionPlayerB]),
            print ("**First move by ", firstMove)

        scoreA = 0
        scoreB = 0
        if firstMove == "A":
            scoreA = self.movePlayer(self.playerA, self.playerB, actionPlayerA)
            if scoreA == 0: scoreB = self.movePlayer(self.playerB, self.playerA, actionPlayerB)
        else:
            scoreB = self.movePlayer(self.playerB, self.playerA, actionPlayerB)
            if scoreB == 0: scoreA = self.movePlayer(self.playerA, self.playerB, actionPlayerA)

        if scoreA != 0: scoreB = scoreA * -1
        if scoreB != 0: scoreA = scoreB * -1

        state = [self.playerState(self.playerA), self.playerState(self.playerB)]

        return (state, [scoreA, scoreB], (scoreA == 100 or scoreB == 100) )

