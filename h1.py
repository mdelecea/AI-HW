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
    def __init__(self,stackstr):
        for i in range(0,len(stackstr),2):
            pancake = Pancake(int(stackstr[i]),stackstr[i+1])
            self.stack.append(pancake)

    def flip(self,index):
        '''reverse list from 0 to index'''
        #cost = sum(self.stack[:index].size)
        self.stack[:index] = self.stack[:index][::-1]
        for i in range(0,index):
            if self.stack[i].orientation == 'w':
                self.stack[i].orientation = 'b'
            else:
                self.stack[i].orientation = 'w'
    
    def pancake_heuristic(self):
        '''heuristic for pancake sorting'''
        heuristic = 0
        for i in range(len(self.stack)):
            if self.stack[i].size-1 != i:
                heuristic = max(heuristic,self.stack[i].size)
        return heuristic

    def goalCheck(self):
        for i in range(0,len(self.stack)):
            if self.stack[i].orientation == 'b' or i!=self.stack[i].size-1:
                return False
        return True

def pancake_sort(fringe,algo):
    if algo == "a":
        return pancake_sort_a(fringe)
    elif algo == "b":
        return pancake_sort_b(fringe)

def tiebreaker(node1,node2):
    '''tiebreaker for a* algorithm'''
    node1num = ""
    for i in range(0,len(node1.stack)):
        node1num.append(str(node1.stack[i].size))
        node1num.append("0" if node1.stack[i].orientation == 'b' else "1")
    node2num = ""
    for i in range(0,len(node2.stack)):
        node2num.append(str(node2.stack[i].size))
        node2num.append("0" if node2.stack[i].orientation == 'b' else "1")
    return True if int(node1num)>int(node2num) else False

def expandNode(node):
    '''expands a node by adding all possible nodes to stack'''
    subfringe = []
    for i in range(1,len(node.stack)+1):
        node.parent = copy.deepcopy(node)
        node.fliploc = i
        newnode = copy.deepcopy(node)
        newnode.flip(i)
        subfringe.append(newnode)
    return subfringe

def printresult(result):
    '''prints the result of the pancake sorting algorithm'''
    for i in range(0,len(result.stack)):
        #print("Pancake",i,"size",result.stack[i].size-1,"orientation",result.stack[i].orientation)
        print(result.stack[i].size,result.stack[i].orientation,sep="",end="")
        if i == result.fliploc-1:
            print("|",end="")
    print("")
    
def pancake_sort_a(fringe):
    '''a* sorting algorithm for pancake flipping'''
    



def pancake_sort_b(fringe):
    '''breadth-first sorting algorithm for pancake flipping'''
    closed_set = []
    while True:
        if fringe[0].goalCheck():
                return fringe[0]
        subfringe = expandNode(copy.deepcopy(fringe[0]))
        closed_set.append(fringe.pop(0))
        for node in subfringe:
            if node not in closed_set:
                fringe.append(node)
            if node.goalCheck():
                return node
            printresult(node)
        print("")



if __name__ == "__main__":
    #stackstr,algo = pancakeparams()
    stackstr = "2b1b3w4w"
    algo = "b"
    node = pancake_stack(stackstr)
    fringe = [node]
    result = pancake_sort(fringe,algo)
    printresult(result)

