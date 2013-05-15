import random
from player import SimplePlayer, BlottoPlayer, NMovePlayer
import math

# An interface for classes that implements different evolution methods.
class Evolution(object):
    def __init__(self, players):
        self.players = players
        pass
    
    """Return new set of players"""
    def evolve(self):
        raise NotImplementedError("This function has not been implemented")

# Class for Simple Evolution. Randomly perturbs the weights slightly.
class SimpleEvolution(Evolution):
    def __init__(self, players, numToEvolve, numClones,\
                 playerType, numMoves=1):
        super(SimpleEvolution, self).__init__(players)
        self.numToEvolve = numToEvolve # how many players to evolve
        self.numClones = numClones # how many clones to make of each player
        self.playerType = playerType # Simple or NMove
        self.numMoves = numMoves 
        pass

    """Return new set of players"""
    def evolve(self):
        # if creates more players than original
        if self.numToEvolve*self.numClones > len(self.players):
            raise BadBoundsException("Too many players")

        # sorts the players by their score
        sortedPlayers = sorted(self.players, key=lambda player: -player.score)

        # creates new set of players
        newPlayers = []

        # chooses top players
        for i in range(self.numToEvolve):
            # evolves each player selected by cloning and perturbing slightly
            for j in range(self.numClones):
                newPlayers.append(self._evolve_player(sortedPlayers[i]))
        # adds random new players        
        for i in range(self.numToEvolve*self.numClones, len(sortedPlayers)):
            newPlayers.append(self.playerType(self.numMoves))
        return newPlayers

    # evolves a player by cloning / perturbing a randomly chosen weight by .01
    def _evolve_player(self, player):
        # clones
        newPlayer = player.copy()
        # perturbs a random weight by 0.01
        index = random.randrange(0, len(newPlayer.weights))
        newPlayer.weights[index] += random.uniform(-0.01, 0.01)
        return newPlayer

"""Each of the players selected to reproduce will sexually reproduce with
each of the other players selected to reproduce, and each couple will have
a certain number of children"""
class SimpleSex(Evolution):
    def __init__(self, players, numToEvolve, numClones=-1, \
                 playerType=SimplePlayer, numMoves=1):
        super(SimpleSex, self).__init__(players)
        self.numToEvolve = numToEvolve
        self.playerType = playerType
        self.numMoves = numMoves
        pass

    """Return new set of players"""
    def evolve(self):
        print self.numToEvolve, self.__choose(self.numToEvolve, 2)
        if self.__choose(self.numToEvolve,2) > len(self.players):
            raise BadBoundsException("Too many players")

        # sorts the players
        sortedPlayers = sorted(self.players, key=lambda player: -player.score)
        newPlayers = []
        # loops through top players
        for i in range(self.numToEvolve):
            # creates children with each of the other players
            for j in range(i + 1, self.numToEvolve):
                newPlayers.append(self._evolve_player(sortedPlayers[i],\
                                                      sortedPlayers[j]))
        # adds randomly generated players
        for i in range(self.__choose(self.numToEvolve,2), len(sortedPlayers)):
            newPlayers.append(self.playerType(self.numMoves))
        return newPlayers

    """Create a child by averaging all the weights of the two parents."""
    def _evolve_player(self, player1, player2):
        # clones player 1
        newPlayer = player1.copy()
        for i in range(len(newPlayer.weights)):
            # averages the weights of the parent players
            newPlayer.weights[i] = \
                (player1.weights[i] + player2.weights[i]) / 2
        return newPlayer

    #calculates nCr
    def __choose(self,n,r):
        f = math.factorial
        return f(n) / f(r) / f(n-r)

"""Each of the players selected to reproduce will sexually reproduce with
each of the other players selected to reproduce, and each couple will have
a certain number of children. The child's attributes will be determined using
a weighted average of all the parents attributes based on score. Assumes scores
are nonnegative."""
class ComplexSex(SimpleSex):
    def __init__(self, players, numToEvolve, numClones=-1,
                 playerType=SimplePlayer, numMoves=1):
        super(ComplexSex, self).__init__(players, numToEvolve,
                                         numClones, playerType, numMoves)
        pass

    """Create a child by using a weighted average of the parents' attributes,
    based on parents' score. """
    def _evolve_player(self, player1, player2):
        newPlayer = player1.copy()
        score1 = player1.score
        score2 = player2.score
        """If both scores are zero, weight each parent equally by artificially
        setting both scores to 1"""
        if (score1 == 0 and score2 == 0):
            score1 = 1
            score2 = 1

        # takes a weighted average of the two parent's attributes    
        for i in range(len(newPlayer.weights)):
            weight1 = player1.weights[i]
            weight2 = player2.weights[i]
            newPlayer.weights[i] = \
                (weight1 * score1 + weight2 * score2) / (score1 + score2)
        return newPlayer

"""A class to evolve Blotto players"""
class BlottoEvolution(SimpleEvolution):
    def __init__(self, players, numToEvolve, numClones, numCastles=10):
        super(BlottoEvolution, self).__init__(players, numToEvolve, numClones,\
                                              BlottoPlayer, numCastles)
        pass

    def _evolve_player(self, player):
        newPlayer = player.copy()
        # chooses 2 castles to shift soldiers between
        index1 = random.randrange(0, len(newPlayer.weights))
        index2 = random.randrange(0, len(newPlayer.weights))

        # how many soldiers to shift
        change = random.randrange(0, 2)

        # moves soldiers from one castle to another
        if (newPlayer.weights[index1] < 100 and newPlayer.weights[index2] > 0):
            newPlayer.weights[index1] += change
            newPlayer.weights[index2] -= change
        return newPlayer

