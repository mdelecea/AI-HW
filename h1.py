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

class Pancake:
        size = 0
        orientation = 'w'
        def __init__(self,size,orientation):
            self.size = size
            self.orientation = orientation

class pancake_stack:
    stack = []
    parent = None
    fliploc = 0
    fwd_cost = 0
    heuristic = 0
    total_cost = fwd_cost + heuristic
    def __init__(self,stackstr):
        for i in range(0,len(stackstr),2):
            pancake = Pancake(int(stackstr[i]),stackstr[i+1])
            self.stack.append(pancake)

    def flip(self,index):
        '''reverse list from 0 to index'''
        selfcopy = copy.deepcopy(self)
        selfcopy.stack[:index] = selfcopy.stack[:index][::-1]
        for i in range(0,index):
            if selfcopy.stack[i].orientation == 'w':
                selfcopy.stack[i].orientation = 'b'
            else:
                selfcopy.stack[i].orientation = 'w'
        return selfcopy

    def expandNode(self):
        '''expands a node by adding all possible nodes to stack'''
        subfringes = []
        for i in range(1,len(self.stack)+1):
            newstack = copy.deepcopy(self).flip(i)
            newstack.fliploc = i
            newstack.parent = self
            newstack.settotalcost()
            subfringes.append(newstack)
        return subfringes
    
    def pancake_heuristic(self):
        '''heuristic for pancake sorting'''
        self.heuristic = 0
        for i in range(len(self.stack)):
            if self.stack[i].size-1 != i:
                self.heuristic = max(self.heuristic,self.stack[i].size)

    def __str__(self):
        s = ""
        for i in range(0,len(self.stack)):
            s += str(self.stack[i].size) + self.stack[i].orientation
            if i == self.fliploc-1:
                s+="|"
        return s

    def __eq__(self,other):
        if len(self.stack) != len(other.stack):
            return False
        for i in range(0,len(self.stack)):
            if self.stack[i] != other.stack[i]:
                return False
        return True

    def settotalcost(self):
        self.total_cost = self.fwd_cost + self.heuristic

    def goalCheck(self):
        for i in range(0,len(self.stack)):
            if self.stack[i].orientation == 'b' or i!=self.stack[i].size-1:
                return False
        return True

    def printresult(result):
        '''prints the result of the pancake sorting algorithm'''
        try:
            result.parent.printresult()
            print("")
        except AttributeError:
            pass
        print(str(result))

def pancake_sort(fringe,algo):
    if algo == "a":
        return pancake_sort_a(fringe)
    elif algo == "b":
        return pancake_sort_b(fringe)

def tiebreaker(nodelist):
    '''tiebreaker for a* algorithm'''
    nodenum = [""]*len(nodelist)
    for i in range(0,len(nodelist)):
        for j in range(0,len(nodelist[i].stack)):
            nodenum[i].append(str(nodelist[i].stack[j].size))
            nodenum[i].append("0" if nodelist[i].stack[j].orientation == 'b' else "1")
    mymax = max(map(len,int(nodenum)))
    return [a for a in nodenum if len(a)==mymax]

def pancake_sort_a(fringe):
    '''a* sorting algorithm for pancake flipping'''
    closed_set = []
    minnode = fringe[0]
    while minnode.goalCheck() == False:
        for node in fringe:
            node.pancake_heuristic()
        minnode = min(fringe,key=lambda x: x.total_cost)
        subfringe = copy.deepcopy(minnode).expandNode()
        closed_set.append(minnode)
        fringe.remove(minnode)
        for node in subfringe:
            if node not in closed_set:
                fringe.append(node)
            node.printresult()
        print("")
    return minnode

def pancake_sort_b(fringe):
    '''breadth-first sorting algorithm for pancake flipping'''
    closed_set = []
    while True:
        if fringe[0].goalCheck():
                return fringe[0]
        subfringe = copy.deepcopy(fringe[0]).expandNode()
        closed_set.append(fringe.pop(0))
        for node in subfringe:
            if node not in closed_set:
                fringe.append(node)
            if node.goalCheck():
                return node
            node.printresult()
        print("")

if __name__ == "__main__":
    #stackstr,algo = pancakeparams()
    stackstr = "2b1b3w4w"
    algo = "b"
    node = pancake_stack(stackstr)
    fringe = [node]
    result = pancake_sort(fringe,algo)
    result.printresult()