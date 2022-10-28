# Credit : Trevor Payne https://www.youtube.com/watch?v=fInYh90YMJU&noredirect=1
# Modified & annotated by Annie Chu, Olin College of Engineering 

# from sys import maxsize #originally to set game state values

maxsize = 1000 
    #player 1 wants +1000
    # 0 is neutral
    #comp wants -1000

#creation of node object
class Node(object):
    def __init__(self, i_depth, i_playerNum, i_sticksRemaining, i_value=0):
        #number of levels, typically Root Node = Level 0, then Level 1, 2, .. last level is terminal node is reversed here
        #how deep we are into the tree, start with 4, then decrease with each iteration
        self.i_depth = i_depth 
        
        #computer (-1) or player (1)
        self.i_playerNum = i_playerNum 

        self.i_sticksRemaining = i_sticksRemaining
        self.i_value = i_value #each value that each terminal node holds, aka game state, -inf, 0, inf
        self.children = []
        self.createChildren()

    def createChildren(self):
        #stops recursive function, once reaches a given depth's terminal nodes
        if self.i_depth < 0:
            return
        for i in range(1, 3): #for the following options of picking either 1 or 2 sticks
            v = self.i_sticksRemaining - i
            self.children.append(Node(self.i_depth - 1, -self.i_playerNum, v, self.realVal(v)))

    def realVal(self, value):
        #if player has won and got the last stick
        if value == 0:
            return maxsize * self.i_playerNum #assign it the player's goal value
        #if player has overdrawn and lost
        elif value < 0:
            return maxsize * -self.i_playerNum #assign it the opponent's goal value
        return 0

def minimax(node, i_depth, i_playerNum):
    if (i_depth == 0) or (abs(node.i_value) == maxsize): 
        #depth of 0 (terminal nodes) OR reach win or lose condition, then return value if so
        return node.i_value

    #first assign opposite best value of what you want it to be
    i_bestValue = maxsize * -i_playerNum

    for child in node.children: #iterating through all the child nodes
        #drill down to bottom of tree via recursion
        i_val = minimax(child, i_depth - 1, -i_playerNum)
        #check if close to goal and if its the better choice, then i_value is then passed back up the tree
        if abs(maxsize * i_playerNum - i_val) < abs(maxsize * i_playerNum - i_bestValue):
            i_bestValue = i_val
    print(f'Depth Level = {i_depth} | Player {i_playerNum} | Max Heuristic Value {i_bestValue}') 
    return i_bestValue

def winCheck(i_sticks, i_playerNum):
    if i_sticks <= 0:
        print("*" * 30)
        if i_playerNum > 0:
            if i_sticks == 0:
                print("\t You WIN!")
            else:
                print("\t Too many ! You lose..")
        else:
            if i_sticks == 0:
                print("\t Comp Wins... Try again.")
            else:
                print("\t COMP ERROR!")
        print("*" * 30)
        return 0
    return 1


if __name__ == '__main__':
    i_stickTotal = 11 #can change this #
    i_depth = 2 # can change this # --> how many "moves ahead" to look at (4 ->3 -> 2 -> 1 -> 0)
    i_curPlayer = 1 #human player starts
    print("INSTRUCTIONS : Pick up one or two sticks at time.")
    while i_stickTotal > 0:
        print("\n%d sticks remain. How many would you like to pick up ?" % i_stickTotal)
        i_choice = input("\n1 or 2:")
        i_stickTotal -= int(float(i_choice))
        if winCheck(i_stickTotal, i_curPlayer): #if the player hasn't won ...
            i_curPlayer *= -1 #flip to computer's turn
            node = Node(i_depth, i_curPlayer, i_stickTotal) #create tree again
            bestChoice = 0 #dummy variable will be replaced to store either 1 or 2
            i_bestValue = -i_curPlayer * maxsize
            for i in range(len(node.children)):
                n_child = node.children[i]
                i_val = minimax(n_child, i_depth, -i_curPlayer)
                if abs(i_curPlayer * maxsize - i_val) <= abs(i_curPlayer * maxsize - i_bestValue):
                    i_bestValue = i_val
                    bestChoice = i
            #will result in 0 or 1, so add 1 to choose 1 or 2
            bestChoice += 1
            print("Comp chooses: " + str(bestChoice) + "\tBased on max heuristic value: " + str(i_bestValue))
            i_stickTotal -= bestChoice
            winCheck(i_stickTotal, i_curPlayer)
            i_curPlayer *= -1