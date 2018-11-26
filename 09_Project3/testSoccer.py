# testSoccer.py
#
# implements the two-player game proposed by Littman & used by Greenwald
#
# OMSCS - Reinforcement Learning, Fall 2018
# Rocko Graziano, rockograziano@gatech.edu
#
# Command line:
#
# python testSoccer.py  [littman|greenwald]  [verbose] [graphic]
#
# where    littman or greenwalk choose between ame size
#          verbose turns on logging
#          graphic makes the logging more entertaining to watch

import random
import numpy as np
import sys
import time

import SoccerWorld

if __name__ == "__main__":

    verbose = True
    graphic = True

    # the greenwald world
    game = SoccerWorld.game(verbose=verbose, rows=2, columns=4, goalRstart=0, goalRend=1, aGoal=0, bGoal=3,aPosition=[0,2], bPosition=[0,1])

    mySeed = 11111994
    random.seed(mySeed)
    np.random.seed(mySeed)

    results = []
    for x in range(10):

        if verbose and graphic:
            print ("\033[2J")

        initialState = game.reset()

        numSteps = 0
        while True:
            if verbose:
                game.printgrid()
                if graphic:
                    time.sleep(.2)
                    print ("\033[2J")
            numSteps += 1

            state, score, done = game.move(np.random.randint(5), np.random.randint(5))
            if done:
                if verbose:
                    game.printgrid()
                    print ("Score {} {} in {} Steps...".format(score[0], score[1], numSteps))
                    sys.stdout.flush()
                    if graphic: time.sleep(3)
                else:
                    print ("Score {} {} in {} Steps...".format(score[0], score[1], numSteps))
                results.append((score[0], score[1], numSteps))
                break

    results = np.array(results)

    print (np.average(results, axis=0))

