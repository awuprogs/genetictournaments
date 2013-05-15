import random
import math
import copy

MOVE_COOP = 1
MOVE_DEFECT = 0

"""An interface for players. Players have parameters that affect how the player
behaves. A Player will return a move given the properties of its opponent."""
class Player(object):
    def __init__(self):
        self.score = 0 # keeps the score throughout each round
        self.weights = [] # 0 - cooperation rate. 1 - constant. 2-n - moves
        self.attrs = []
        self.num_moves = 1
    
    """ take in a player and return either MOVE_COOP or MOVE_DEFECT """
    def returnMove(self, player):
        raise NotImplementedError("This function has not been implemented")

    """Computes the dot product of the players weights with the already
    initialized moves"""
    def playerDot(self):
        num_zeros = self.attrs.count(0)
        num_ones = self.attrs.count(1)
        count = 0
        for i in range(len(self.weights)):
            if(self.attrs[i] != -1):
                count = count + self.weights[i]*self.attrs[i]
        return count/(num_zeros+num_ones)

    # copies a player. includes weighs. 
    def copy(self):
        player = self.__class__(self.num_moves)
        player.weights = copy.deepcopy(self.weights)        
        return player    

    # updates attrs to include the opponent's next move
    def informMove(self, move):
        num_zeros = self.attrs.count(0)
        num_ones = self.attrs.count(1)
        if(num_ones+num_zeros == 1): # no moves played yet
            self.attrs[2] = move
            return

        for i in range(self.num_moves,1,-1): # adjust forward last n moves
            self.attrs[i+1] = self.attrs[i]
        self.attrs[2] = move
        return

"""A class for simple player. Only considers the opponent's last move.
Does not consider cooperation rate or other moves."""
class SimplePlayer(Player):
    def __init__(self, numMoves=1):
        super(SimplePlayer, self).__init__()
        """Sets a player with a constant weight and a last move weight """
        self.weights = [0,random.uniform(-1, 1), random.uniform(-1, 1)]
        self.attrs = [-1,1, -1]
        pass

    # returns a move given the opponent player
    def returnMove(self, p):
        num_zeros = p.attrs.count(0)
        num_ones = p.attrs.count(1)
        if(num_zeros+num_ones == 1): # only stationary weight and coop
            return random.randrange(0,2)
        measure = self.playerDot()
        # uses the formula p = e^c/(1+e^c) where c is the linear combination
        # of attributes
        probability = math.exp(measure)/(1+math.exp(measure))

        # generates move
        if(random.uniform(0,1) < probability):
            return 1
        else:
            return 0

# A class for a player that considers the opponent's last N moves.
class NMovePlayer(Player): # assumes n>0
    def __init__(self,n):
        super(NMovePlayer, self).__init__()
        """Sets a player with a cooperation percentage, a constant, and
        the last n move weights"""
        self.num_moves = n

        # initializes weights to random values
        for i in range(self.num_moves+2):
            self.weights.append(random.uniform(-1,1))
        """First attribute is 1 to ensure the constant is present"""
        self.attrs = [-1, 1]

        # the remaining moves are -1, since round hasn't started
        for i in range(self.num_moves):
            self.attrs.append(-1)

        self.num_moves = n
        self.moves_played = 0 # moves played so far
        self.coops = 0 # number of moves where the player cooperated

    # returns a move given the opponent player
    def returnMove(self, p):
        num_zeros = p.attrs.count(0)
        num_ones = p.attrs.count(1)
        if(num_ones+num_zeros == 1): # no moves played yet
            self.moves_played = 1
            self.coops = random.randrange(0,2) # set number of cooperations
            self.attrs[0] = self.coops
            return self.coops

        # if moves have been played
        measure = self.playerDot()

        # uses the formula p = e^c/(1+e^c) where c is the linear combination
        # of attributes
        probability = math.exp(measure)/(1+math.exp(measure))
        if(random.uniform(0,1) < probability):
            move = 1
        else:
            move = 0

        # updates the number of cooperationsa and moves played  
        self.coops += move
        self.moves_played += 1
        self.attrs[0] = float(self.coops)/self.moves_played

        return move


# A representation for a Blotto player that does not consider the opponent
class BlottoPlayer(Player):
    def __init__(self, num_castles = 10):
        super(BlottoPlayer, self).__init__()

        # assigns a number of soldiers for each castle
        # array[i] represents cumulative number of soldiers from castle 0 to i
        array = [random.randrange(0, 101) for r in range(num_castles - 1)]
        array.sort()

        # number of soldiers in first castle
        self.weights.append(array[0])

        # calculates number of soldiers per castle by taking difference of
        # consecutive elements
        for i in range(1,num_castles-1):
            self.weights.append(array[i]-array[i-1])
        self.weights.append(100-array[num_castles-2])
        
        self.num_moves = num_castles

    # returns the move
    def returnMove(self,p):
        return self.weights
