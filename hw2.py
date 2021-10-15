MAXINT = 2147483647
MININT = -2147483648

# Gets tree from user
def treein(String = ""):
    if String == "":
        String = input()
    if String == "":
        print("You did not enter a string.\n")
        return treein()
    else:
        return list(map(int,String.split(' ')))

class alphaBetaPruning:
    def __init__(self, values):
        self.values = values
        self.pruneList = []
        self.best = self.minimax(0, 0, True) #initializes class and calls minimax

    def minimax(self, depth, index, isMax, alpha=MININT, beta=MAXINT):
        '''Recursive function to perform minimax with alpha-beta pruning'''
        if depth == 3: #If the depth is 3, then we have reached the end of the tree
            return self.values[index] #Return the value of the node
        elif depth == 0: #If the depth is 0, then we are at the root of the tree, and have 3 branches instead of 2
            branches = 3
        else:
            branches = 2
        if isMax: # If the node is a maximizer, use this side
            best = MININT # Set the best value to the minimum possible value
            for i in range(0, branches): # For each branch
                best = max(best, self.minimax(depth + 1, index * 2 + i,False, alpha, beta)) #Recursively call the minimax function on the children
                alpha = max(alpha, best) # Update the alpha value
                if beta <= alpha and i == 0:
                    self.getPruneList(depth+1, index*2+1,2) #If the alpha value is greater than the beta value, then we have pruned the tree
                    break
            return best
        else: #If the node is a minimizer, use this side
            best = MAXINT # Set the best value to the maximum possible value
            for i in range(0, 2):
                best = min(best, self.minimax(depth + 1, index * 2 + i,True, alpha, beta))
                beta = min(beta, best)
                if beta <= alpha and i == 0:
                    self.getPruneList(depth+1, index*2+1,2)
                    break
            return best

    def getPruneList(self,depth,nodeIndex,branches):
        '''Dives down further into the tree to collect the pruned nodes'''
        if depth == 3:
            self.pruneList.append(nodeIndex)
            return 
        for i in range(0, 2):
            self.getPruneList(depth + 1, nodeIndex * branches + i,branches)

if __name__ == "__main__":
    values = treein()
    alphaBeta = alphaBetaPruning(values)
    #print(*alphaBeta.best)
    print(*alphaBeta.pruneList)