# adapted from https://thesharperdev.com/implementing-minimax-tree-search/

from random import randint
import time
"""
Setting up Tree Structure
"""
r_max = 15
d = 4 #depth

class Node():
    ## holds a single value and links to a left and right node
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

class Choice():
    ## represents the player's move
    def __init__(self, move, value):
        self.move = move
        self.value = value

    def __str__(self):
        return self.move + ": " + str(self.value)

"""
printing tree stuff
"""
def get_spacing(depth):
    first_num_spacing = 2 ** depth
    other_num_spacing = 0
    if (depth == 1):
        other_num_spacing = 3
    elif (depth == 2):
        other_num_spacing = 7
    elif (depth == 3):
        other_num_spacing = 15
    elif (depth == 4):
        other_num_spacing = 31
    return [first_num_spacing, other_num_spacing]
    

def print_tree(node, depth):
    layer_nodes = [node]
    while (len(layer_nodes) > 0):
        layer_has_nodes = False
        next_layer_nodes = []
        current_values = []
        spacing = get_spacing(depth)
        first_num_spacing = spacing[0]
        other_num_spacing = spacing[1]
        for i in range(len(layer_nodes)):
            n = layer_nodes[i]
            if (n is not None):
                layer_has_nodes = True
                if (n.left != None):
                    next_layer_nodes.append(n.left)
                else:
                    next_layer_nodes.append(None)
                if (n.right != None):
                    next_layer_nodes.append(n.right)
                else:
                    next_layer_nodes.append(None)
                #make every number two chars long
                svalue = str(n.value).rjust(2, ' ')
            else:
                svalue = '  '
            #spacing for layers
            if (len(current_values) == 0):
                svalue = svalue.rjust(first_num_spacing, ' ')
            else:
                svalue = svalue.rjust(other_num_spacing, ' ')
            current_values.append(svalue)
        if (layer_has_nodes):
            print (' '.join(current_values))
        layer_nodes = next_layer_nodes
        depth = depth - 1

"""
MINIMAX ALGORITHM
"""
def minimax(node, is_max):    
    # base case, if no sub nodes, just return the value
    if (node.left is None and node.right is None):
        return Choice("end", node.value)

    # if node has only one child
    if (node.right is None):
        l_choice = minimax(node.left, not is_max)
        return Choice("left", l_choice.value)
    elif (node.left is None):
        r_choice = minimax(node.right, not is_max)
        return Choice("right", r_choice.value)

    # if child nodes exist, run minimax on each child nodes
    l_choice = minimax(node.left, not is_max)
    r_choice = minimax(node.right, not is_max)

    # compare results
    if (is_max):
        if (l_choice.value > r_choice.value):
            return Choice("left", l_choice.value)
        else:
            return Choice("right", r_choice.value)
    else:
        if (l_choice.value < r_choice.value):
            return Choice("left", l_choice.value)
        else:
            return Choice("right", r_choice.value)
"""
ALPHA BETA PRUNING MINIMAX ALGORITHM
"""
MIN = -1000
MAX = 1000
def minimaxAB(node, is_max, alpha, beta):    
    # base case, if no sub nodes, just return the value
    if (node.left is None and node.right is None):
        return Choice("end", node.value)

    # if node has only one child
    if (node.right is None):
        l_choice = minimaxAB(node.left, not is_max, alpha, beta)
        return Choice("left", l_choice.value)
    elif (node.left is None):
        r_choice = minimaxAB(node.right, not is_max, alpha, beta)
        return Choice("right", r_choice.value)

    # if child nodes exist, run minimax on each child nodes
    ##l_choice = minimax(node.left, not is_max)
    ##r_choice = minimax(node.right, not is_max)

    # compare results
    if (is_max):
            # if child nodes exist, run minimax on each child nodes            
            l_choice = minimaxAB(node.left, not is_max, alpha, beta)
            alpha = max(l_choice.value, alpha)
            if (alpha >= beta):
                return Choice("left", l_choice.value)
            r_choice = minimaxAB(node.right, not is_max, alpha, beta)
            if (l_choice.value > r_choice.value):
                return Choice("left", l_choice.value)
            else:
                return Choice("right", r_choice.value)
    else:
        l_choice = minimaxAB(node.left, not is_max, alpha, beta)
        beta = min(l_choice.value, beta)
        if (alpha >= beta):
            return Choice("left", l_choice.value)
        r_choice = minimaxAB(node.right, not is_max, alpha, beta)
        if (l_choice.value < r_choice.value):
            return Choice("left", l_choice.value)
        else:
            return Choice("right", r_choice.value)

"""
HARDCODING A GAME TREE
"""
# 4th layer
def createleafs(layer_num):
    # last_num = 2**(layer_num-1)
    all_num = []
    for i in range(1, layer_num):
        nodelayer = 2**i
        nodenum = 0
        leaves = []
        while nodenum < nodelayer:
            leaves.append(Node(randint(0,r_max)))
            nodenum += 1
        all_num.append(leaves)
    return all_num

leaf = createleafs(d)
# leaf = [[Node(2)]*2, [Node(4)]*4, [Node(8)]*8,[Node(16)]*16]#, [Node(32)]*32 ]
##### creating last layer

def testthis():
    leafTotal = []
    nodeCount = 0

    for i in range(-2,-len(leaf)-1,-1):
        # print(f'i = {i}')
        if i == -2:
            leafArray = []
            leafCount = 0
            for leafLevel in leaf[i]:
                leafLevel.left = leaf[i+1][leafCount]
                leafCount +=1
                leafLevel.right = leaf[i+1][leafCount]
                leafCount +=1
                
                leafArray.append(leafLevel)
                # print_tree(leafLevel,2)
            leafTotal.append(leafArray)
            # print(f'len =># {len(leafTotal)}')
        else:
            leafArray = []
            leafCount = 0
            # print(f'******* leaftotal = {len(leafTotal)}')
            for leafLevel in leaf[i]:
                # print(len(leafTotal), nodeCount, leafCount)
                # print(leafTotal)
                # leafLevel.left = leafArray[leafCount]
                leafLevel.left = leafTotal[nodeCount][leafCount]
                leafCount +=1
                leafLevel.right = leafTotal[nodeCount][leafCount]

                # leafLevel.right = leafArray[leafCount]
                leafCount +=1

                leafArray.append(leafLevel)
                # print_tree(leafLevel,4)

                # print(f'learfarray {leafArray}')
            nodeCount +=1

            leafTotal.append(leafArray)
            # print(f'len =>{len(leafTotal)}')

        # print(len(leafArray))

    root = Node(None)
    root.left = leafTotal[-1][-1]
    root.right = leafTotal[-1][-2]
    return root
    # print_tree(leafTotal[-1][-1], 5)
    # print_tree(leafTotal[-1][-2], 5)


root = testthis()
print_tree(root, d)

# """
# CREATING TREE, DEPTH = 5
# """
# LLL = []
# # ---- creating last layer (4 -> 5)
# leafcount = 0
# LL_leaves = []
# for LL in leaf[-2]:
#     LL.left = leaf[-1][leafcount]
#     leafcount += 1
#     LL.right = leaf[-1][leafcount]
#     leafcount += 1
#     # print(leafcount)
#     LL_leaves.append(LL)
#     # print_tree(LL,2)
# LLL.append(LL_leaves)

# # ----- creating layer above (3 -> 4)
# leaf2count = 0
# LN_leaves = []
# for LN in leaf[-3]:
#     LN.left = LL_leaves[leaf2count]
#     leaf2count += 1
#     LN.right = LL_leaves[leaf2count]
#     leaf2count += 1
#     LN_leaves.append(LN)
#     # print_tree(LN,3)
# LLL.append(LN_leaves)

# # ----- creating layer above (2 -> 3)
# leaf3count = 0
# LNN_leaves = []
# for LNN in leaf[-4]:
#     LNN.left = LN_leaves[leaf3count]
#     leaf3count += 1
#     LNN.right = LN_leaves[leaf3count]
#     leaf3count += 1
#     LNN_leaves.append(LNN)
#     # print_tree(LN,3)
# LLL.append(LNN_leaves)

# # ----- creating initial layer (1 -> 2)
# root = Node(None)
# root.left = LLL[-1][0]
# root.right = LLL[-1][1]


"""
RUNNING THE PROGRAM
"""
def run_tree():
    print_tree(root,d)
    print ("\n")
    # initialize our state
    current_node = root
    is_max = True
    st = time.time()
    while (True):
        # run minimax on current node
        # choice = minimax(current_node, is_max)

        choice = minimaxAB(current_node, is_max, alpha = MIN, beta = MAX)
        
        # make choice based on mini max outcome
        if (choice.move == "left"):
            print ("ismax? " + str(is_max) + " | Moving left to node with value " + str(current_node.left.value))
            current_node = current_node.left
        elif (choice.move == "right"):
            print ("ismax? " + str(is_max) +" | Moving right to node with value " + str(current_node.right.value))
            current_node = current_node.right
        elif (choice.move == "end"):
            print ("Game ends with a score of " + str(choice.value))
            break
        # flip players turn
        is_max = not is_max
    et = time.time()
    elapsed_time = et - st
    final_res = elapsed_time * 1000
    print('Execution time:', final_res, 'milliseconds')
# run_tree()