import copy

def pancakeparams(String = ""):
    if String == "":
        String = input("Please enter a string: ")
    if String == "":
        print("You did not enter a string.\n")
        return pancakeparams()
    elif String == "exit":
        return String
    elif String == "help":
        print("To analyze a string, enter a string.\n")
        print("To exit, enter 'exit'.\n")
        print("To see this help, enter 'help'.\n")
        return pancakeparams()
    else:
        stackstr,algo =String.split('-',1)
        if algo != "a" and algo != "b":
            print("You did not enter a valid algorithm.\n")
            return pancakeparams()
        return stackstr,algo

class pancake_stack:
    parent = None
    fliploc = 0
    fwd_cost = 0
    heuristic = 0
    total_cost = fwd_cost + heuristic

    def __init__(self,stackstr,fwd_cost = 0,heuristic = 0):
        self.stack = []
        self.fwd_cost = fwd_cost # initialize the forward cost
        self.heuristic = heuristic # initialize the heuristic cost
        for i in range(0,len(stackstr),2):
            pancake = [int(stackstr[i]),stackstr[i+1]] # add pancake to stack from string
            self.stack.append(pancake)

    def flip(self,index):
        '''reverse list from 0 to index'''
        selfcopy = copy.deepcopy(self)
        selfcopy.stack[:index] = selfcopy.stack[:index][::-1] # reverse list from 0 to index
        for i in range(0,index):    # changes pancake burnt side to opposite side
            if selfcopy.stack[i][1] == 'w':
                selfcopy.stack[i][1] = 'b'
            else:
                selfcopy.stack[i][1] = 'w'
        return selfcopy

    def expandNode(self):
        '''expands a node by adding all possible nodes to stack'''
        subfringes = []
        oldstr = str(self)
        for i in range(1,len(self.stack)+1):
            newstack = pancake_stack(oldstr) # create new stack from string to avoid mutating original
            newstack = newstack.flip(i) # flip the stack 
            newstack.fliploc = i    # store the location of the flip
            newstack.parent = self # store the parent of the new pancake
            newstack.fwd_cost = self.fwd_cost+i # store the forward cost
            newstack.pancake_heuristic()    # calculate heuristic
            newstack.total_cost = newstack.fwd_cost + newstack.heuristic # calculate total cost
            subfringes.append(newstack) 
        return subfringes
    
    def pancake_heuristic(self):
        '''heuristic for pancake sorting'''
        self.heuristic = 0
        for i in range(len(self.stack)):
            if self.stack[i][0]-1 != i:
                self.heuristic = max(self.heuristic,self.stack[i][0]) # finds the max pancake out of place
        self.total_cost = self.fwd_cost + self.heuristic # recalculates total cost just in case

    def __str__(self):
        '''stringify the object'''
        s = ""
        for i in range(0,len(self.stack)):
            s += str(self.stack[i][0]) + self.stack[i][1] # stringify each pancake and add to stack
        return s
    
    def __eq__(self,other):
        '''custom comparison func'''
        if len(self.stack) != len(other.stack): # if the lengths are different, they are not equal
            return False
        for i in range(0,len(self.stack)):  # compare each pancake
            if self.stack[i] != other.stack[i]:
                return False
        return True

    def goalCheck(self):
        '''checks if stack is desired stack'''
        for i in range(0,len(self.stack)):
            if self.stack[i][1] == 'b' or i!=self.stack[i][0]-1: # if any pancake is not in place or is not burnt
                return False
        return True

    def printresult(result,algo = "b",fliploc = 0):
        '''prints the end result of the pancake sorting algorithm recursively'''
        try:
            result.parent.printresult(algo,result.fliploc) # recursively call the parent
        except AttributeError:
            pass
        outstring = " g:%d, h:%d"%(result.fwd_cost,result.heuristic) # print the costs
        s = ""
        for i in range(0,len(result.stack)):
            s += str(result.stack[i][0]) + result.stack[i][1] # stringify each pancake
            if not result.goalCheck():
                if i == fliploc-1: # if the pancake is the one that was flipped
                    s+="|"
        print(s if algo == "b" else s+outstring)

def pancake_sort(fringe,algo):
    '''select which pancake sorting algorithm to use'''
    if algo == "a":
        return pancake_sort_a(fringe)
    elif algo == "b":
        return pancake_sort_b(fringe)

def tiebreaker(nodelist):
    '''tiebreaker for a* algorithm'''
    nodenum = []
    for i in range(0,len(nodelist)):
        for j in range(0,len(nodelist[i].stack)):
            nodenum.append(str(nodelist[i].stack[j][0])) # adds each pancake value as a string
            nodenum.append("0" if nodelist[i].stack[j][1] == 'b' else "1") # adds each pancake orientation as a string
    return nodelist[0] if int(nodenum[0])>int(nodenum[1]) else nodelist[1] # returns the node with the highest "value"

def pancake_sort_a(fringe):
    '''a* sorting algorithm for pancake flipping'''
    closed_set = []
    while fringe:
        minnode = min(fringe,key=lambda x: x.total_cost) # find the node with the lowest total cost
        fringe.remove(minnode) # remove the node from the fringe
        if minnode.goalCheck(): # if the node is the goal
            return minnode
        subfringe = copy.deepcopy(minnode).expandNode() # expand the node
        for node in subfringe:
            if node not in closed_set:
                fringe.append(node) # add the new node to the fringe if it is not in the closed set
        if minnode not in closed_set:
                closed_set.append(minnode) # add the old node to the closed set


def pancake_sort_b(fringe):
    '''breadth-first sorting algorithm for pancake flipping'''
    closed_set = []
    while True:
        if fringe[0].goalCheck(): # if the node is the goal
                return fringe[0]
        subfringe = copy.deepcopy(fringe[0]).expandNode() # expand the node
        closed_set.append(fringe.pop(0)) # remove the node from the fringe
        for node in subfringe:
            if node not in closed_set:
                fringe.append(node) # add the new node to the fringe if it is not in the closed set
            if node.goalCheck(): # if the node is the goal
                return node

if __name__ == "__main__":
    stackstr,algo = pancakeparams()
    node = pancake_stack(stackstr)
    fringe = [node]
    result = pancake_sort(fringe,algo)
    result.printresult(algo)