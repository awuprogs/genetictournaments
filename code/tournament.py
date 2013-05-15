import random
import thread
import threading
import datetime
from player import *

"""Interface. A class that runs a tournament. A match is defined as a single
instance of the game between two people. In each round, we create a perfect
pairing of the players, and run multiple matches between each pair. In the
tournament, we run multiple rounds. We return the cumulative score over all
rounds for each player."""

class Tournament(object):
    def __init__(self, players, parallelism):
        self.players = players # input list of players
        self.parallelism = parallelism # use parallelism
        pass

    # runs a specified number of rounds
    def runTournament(self):
        for i in range (0, self.numRounds):
            # if not in parallel, run rounds where matches are sequential
            if (self.parallelism == 0):
                self.runRound()
            # otherwise, run rounds where matches are parallelized
            else:
                self.runRoundParallelism()
        return self.players    

    # creates a perfect pairing of the players
    def createPairing(self):
        #creates a pairing by using sample to get a permutation of the players
        return random.sample(self.players, len(self.players))

    # creates a perfect pairing and runs a specified number of
    # matches between every pair
    def runRound(self):
        # a perfect pairing
        randomizedPlayers = self.createPairing()

        # loops through all pairs
        for i in range (0, len(self.players), 2):
            # runs matches between a pair
            for j in range (0,self.numMatches, 1):
                self.runSingleMatch(i, i+1)
        return

    # runs a number of matches between pairs. helper for parallelized matches.
    def runMatches(self, i):
        for j in range (0,self.numMatches, 1):
            self.runSingleMatch(i,i+1)

    # runs a round, but parallelizes each pair
    def runRoundParallelism(self):
        # a perfect pairing
        randomizedPlayers = self.createPairing()

        # creates a new thread for each pair and runs matches between the pair
        for i in range (0, len(self.players), 2):
            thread.start_new_thread(self.runMatches,(i,))

        # makes sure all threads are finished
        while (threading.activeCount() > 1):
            pass

"""A specific Tournament for Prisoner's Dilemma"""
class PrisonersDilemmaTournament(Tournament):
    
    def __init__(self, players, parallelism, coopcoop, coopdef, defdef,
                 defcoop, numMatches, numRounds):
        super(PrisonersDilemmaTournament, self).__init__(players, parallelism)
        # payoff values
        self.coopcoop = coopcoop # p1: coop, p2: coop
        self.coopdef = coopdef # p1: coop, p2: def
        self.defdef = defdef # p1: def, p2: def
        self.defcoop = defcoop # p1: def, p2: coop
        self.numMatches = numMatches # number of matches to run for each pair
        self.numRounds = numRounds # number of rounds in a tournament

    # runs a single match of Prisoner's Dilemma between two players
    def runSingleMatch(self, p1, p2):
        # the moves the players will choose
        move1 = self.players[p1].returnMove(self.players[p2])
        move2 = self.players[p2].returnMove(self.players[p1])

        # updates player's information to keep track of opponent's last moves
        self.players[p1].informMove(move2)
        self.players[p2].informMove(move1)

        # determines the outcome of the match and updates the scores
        if (move1 == move2):
            # both cooperate
            if(move1 == MOVE_COOP):
                self.players[p1].score += self.coopcoop
                self.players[p2].score += self.coopcoop
            # both defect
            else:
                self.players[p1].score += self.defdef
                self.players[p2].score += self.defdef
        else:
            # p1 cooperates, p2 defects
            if(move1 == MOVE_COOP):
                self.players[p1].score += self.coopdef
                self.players[p2].score += self.defcoop
            # p1 defects, p2 cooperates
            else:
                self.players[p1].score += self.defcoop
                self.players[p2].score += self.coopdef
        return


"""A specific Tournament for Blotto"""
class BlottoTournament(Tournament):

    def __init__(self, players, parallelism, numMatches, numRounds, castles,\
                 soldiers):
        super(BlottoTournament, self).__init__(players, parallelism)
        self.numMatches = numMatches # number of matches to run between a pair
        self.numRounds = numRounds # number of rounds in a tournament
        self.castles = castles # number of castles. 
        self.soldiers = soldiers # number of soldiers.

    # runs a single instance of Blotto between two players
    def runSingleMatch(self, p1, p2):
        # the moves the players will choose
        move1 = self.players[p1].returnMove(self.players[p2])
        move2 = self.players[p2].returnMove(self.players[p1])

        # the number of castles p1 won
        castlesWon = 0

        # loops through the castles
        for i in range (0, self.castles):
            # if p1 has more soldiers in the castle, add one to castles won
            if (move1[i] > move2[i]):
                castlesWon += 1
            # if p1, p2 have equal soldiers in the castle, add 0.5
            elif (move1[i] == move2[i]):
                castlesWon += 0.5
                
        # updates scores        
        self.players[p1].score += castlesWon
        self.players[p2].score += 10 - castlesWon

        return
