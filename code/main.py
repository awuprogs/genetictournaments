#!/usr/bin/env python
# -*- coding: utf-8 -*-

from evolution import *
from player import *
from tournament import *
import math
import sys

numPlayers = 300 # total number of players at each generation
generations = 100 # how many times do we evolve?
matches = 10 # how many rounds in a generation of a tournament?
rounds = 20 # number of times players play each other in a match
numToEvolve = 48 # how many of the best players should go to next generation
numClones = 6 # number of (mutated) clones in next generation

# parameters
coopcoop = 4 # payoff if both cooperate
coopdef = 0 # payoff to Player 1 if he cooperates and Player 2 defects
defdef = 1 # payoff if both defect
defcoop = 5 # payoff to Player 1 if he defects and Player 2 cooperates

MOVE_MEMORY = 4

# map from evolution string to class type
evol = {
       'simpleevol':SimpleEvolution,
       'simplesex':SimpleSex,
       'complex':ComplexSex,
       }

"""For 1-move memory players, calculates probabilities given the log odds
formula shown in the specs."""
def calcCoopDef(player):
    val = math.exp(player.weights[1] + player.weights[2])
    print "P(cooperate|defect) = ", (math.exp(player.weights[1]) / \
      (1 + math.exp(player.weights[1])))
    print "P(cooperate|cooperate) = ", (val / (1 + val))

print "This simulation prints out the best strategy at each generation"

""" running genetic algorithm for SimplePlayer """
def runSimple(evolType='simpleevol'):
    """ determining evolution type based on argument """
    try:
        evolv = evol[evolType]
    except KeyError:
        print "invalid evolution type. defaulting to SimpleEvolution"
        evolv = evol['simpleevol'] 
    print "Using Evolution type", evolv.__name__

    players = []
    for i in range(numPlayers):
        players.append(SimplePlayer())

    """ run all generations of tournament """
    for i in range(generations):
        print "########### Generation", i," started"
        print "Best Strategy: "
        calcCoopDef(players[0])
        tournament = PrisonersDilemmaTournament(players, 0, coopcoop, coopdef,\
            defdef, defcoop, matches, rounds)
        tournament.runTournament()
        evolution = evolv(players, numToEvolve, numClones, SimplePlayer)
        players = evolution.evolve()
        
    print "The simple approach only looks at the last move. "
    print "We print out the probability "
    print "that we cooperate given that the opponent just cooperated and the "
    print "probability that we cooperate given that the opponent just defected"

""" running genetic algorithm for NMovesPlayer """
def runNMoves(evolType='simpleevol', memory=MOVE_MEMORY):
    try:
        evolv = evol[evolType]
    except KeyError:
        print "invalid evolution type. defaulting to SimpleEvolution"
        evolv = evol['simpleevol']
    print "Using Evolution type", evolv.__name__

    players = []
    for i in range(numPlayers):
        players.append(NMovePlayer(memory))

    for i in range(generations):
        print "########### Generation", i," started"
        print "Best Strategy: ", players[0].weights
        tournament = PrisonersDilemmaTournament(players, 0, coopcoop, coopdef,\
            defdef, defcoop, matches, rounds)
        tournament.runTournament()
        evolution = evolv(players, numToEvolve, numClones, NMovePlayer, memory)
        players = evolution.evolve()

    print "The NMoves approach looks at the opponent's overall cooperation "
    print "percentage and the last n moves (here, by default, n = 4). This "
    print "strategy prints out the coefficients of our strategy. The first "
    print "coefficient is the overall cooperation probability, the second is "
    print "a constant, and 3rd to 6th represent the four moves. In general, "
    print "a positive coefficient means that we are more likely "
    print "to cooperate based on that variable while a negative means "
    print "we are more likely to defect."

""" runs genetic algorithm with half NMovePlayer's and half SimplePlayer's """
def runMixed(evolType='simpleevol', memory=MOVE_MEMORY):
    players = []
    for i in range(numPlayers/2):
        players.append(NMovePlayer(memory))
        players.append(SimplePlayer())

    for i in range(generations):
        print "########### Generation", i," started"
        print "Best Strategy: ", players[0].weights
        tournament = PrisonersDilemmaTournament(players, 0, coopcoop, coopdef,\
            defdef, defcoop, matches, rounds)
        tournament.runTournament()
        """ alternating generations, add SimplePlayer and NMovePlayer to
            fill the rest of the players for the next generation """
        if i % 2 == 0:
            evolution = SimpleEvolution(players, numToEvolve, numClones,\
                NMovePlayer, memory)
        else:
            evolution = SimpleEvolution(players, numToEvolve, numClones,\
                SimplePlayer)
        players = evolution.evolve()

    if len(players[0].weights) == 3:
        calcCoopDef(players[0])
        print "On this run, a player with 1-move memory was best"
    else:
        print "On this run, a player with multiple-move memory was best"
        
    print "A mixed approach seeing if players of longer memory are better"
    print "than those with shorter memory. The convergent strategy at the"
    print "end will give us a good idea of this."

""" runs Blotto tournament """
def runBlotto():
    players = []
    for i in range(numPlayers):
        players.append(BlottoPlayer())

    for i in range(generations):
        print "########### Generation", i," started"
        print "Best Strategy: ", sorted(players[0].weights)
        tournament = BlottoTournament(players, 0, matches, rounds, 10, 100)
        tournament.runTournament()
        evolution = BlottoEvolution(players, numToEvolve, numClones, 10)
        players = evolution.evolve()

""" if passed in, sets payoffs """
if (len(sys.argv) == 7):
    coopcoop = int(sys.argv[3])
    coopdef = int(sys.argv[4])
    defdef = int(sys.argv[5])
    defcoop = int(sys.argv[6])

if (len(sys.argv) == 6):
    coopcoop = int(sys.argv[2])
    coopdef = int(sys.argv[3])
    defdef = int(sys.argv[4])
    defcoop = int(sys.argv[5])

print "Using payoffs ", coopcoop, " ", coopdef, " ", defdef, " ", defcoop

if (len(sys.argv) < 2):
    print "you must specify game/player type"
    exit(0)

if (sys.argv[1] == 'simple'):
    if len(sys.argv) == 7 or len(sys.argv) == 3:
        if sys.argv[2] != 'simpleevol':
            numToEvolve = 20
        runSimple(sys.argv[2])
    else:
        runSimple()
elif (sys.argv[1] == 'nmoves'):
    if len(sys.argv) == 7 or len(sys.argv) == 3:
        if sys.argv[2] != 'simpleevol':
            numToEvolve = 20
        runNMoves(sys.argv[2])
    else:
        runNMoves()
elif (sys.argv[1] == 'mixed'):
    runMixed()
elif (sys.argv[1] == 'blotto'):
    runBlotto()
else:
    print "you entered an invalid game. look at README for possibilities"
