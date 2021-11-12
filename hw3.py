import numpy as np

class state:
    def __init__(self, type, location):
        #initialize the state variables
        self.type = type
        self.location = location
        self.actions = [self.location+4, self.location+1, self.location-4,self.location-1]
        
        #setting rewards and actions for special states
        self.reward = -0.1
        if self.type == 'W':
            self.actions = [None]
        elif self.type == 'F':
            self.reward = -100
            self.actions = [None]
        elif self.type == 'G':
            self.reward = 100
            self.actions = [None]
        #initializing Q-values
        self.Q_vals = [0.0 for x in self.actions]
    
    def outofbounds(self,action):
        #check if action is out of bounds
        if self.location in [0,1,2,3] and action == self.location-4:
            return True
        if self.location in [12,13,14,15] and action == self.location+4:
            return True
        if self.location in [0,4,8,12] and action == self.location-1:
            return True
        if self.location in [3,7,11,15] and action == self.location+1:
            return True
        return False

    def __str__(self):
        #printing the state
        qstr = '\n'
        words = ["up", "right", "down", "left"]
        for i in range(4):
            val = str(round(self.Q_vals[i],2))
            qstr += words[i] + val +'\n'
        return str(self.location)+ " " + self.type+ " " + str(self.reward)


def print_policy():
    for i in range(16):
        if board[i].type == "W":
            print(str(i+1)+("    wall-square"))
        elif board[i].type == "G":
            print(str(i+1)+("    goal"))
        elif board[i].type == "F":
            print(str(i+1)+("    forbid"))
        else:
            action = board[i].actions[np.argmax(board[i].Q_vals)]
            if action == i+4:
                print(str(i+1)+("    up"))
            elif action == i+1:
                print(str(i+1)+("    right"))
            elif action == i-1:
                print(str(i+1)+("    left"))
            elif action == i-4:
                print(str(i+1)+("    down"))

def print_Q(stateloc):
    state = board[stateloc]
    words = ["up", "right", "down", "left"]
    for i in range(4):
        val = str(round(state.Q_vals[i],2))
        print(words[i],val)

def q_Learning():
    '''set up q-learning for 4x4 board'''
    discount_rate = 0.1
    learning_rate = 0.3
    max_episodes = 100000
    epsilon = 0.5
    episodes = 0
    while episodes < max_episodes:
        currState = board[1]
        while not (currState.type == 'G' or currState.type == 'F'):
            if np.random.uniform() < epsilon: #Take random action
                action_I = np.random.choice(currState.actions)
            else: #Take action with highest Q-value
                action_I = currState.actions[np.argmax(currState.Q_vals)]
            if currState.outofbounds(action_I):
                newState = currState
            else:
                newState = board[action_I]
            if newState.type == "W":
                    newState = currState
            currState.Q_vals[currState.actions.index(action_I)] = round((1-learning_rate)*currState.Q_vals[currState.actions.index(action_I)]+learning_rate*(newState.reward + discount_rate*max(newState.Q_vals)),4)
            if newState.type != "W":
                currState = newState
        episodes += 1
        

if __name__ == '__main__':
    #boardpoi = "12 7 5 6 p".split()
    boardpoi = input().split()
    board = [state(' ',x) for x in range(16)]
    board[1] = state('S', 1)
    board[int(boardpoi[0])-1] = state('G', int(boardpoi[0])-1)
    board[int(boardpoi[1])-1] = state('G', int(boardpoi[1])-1)
    board[int(boardpoi[2])-1] = state('F', int(boardpoi[2])-1)
    board[int(boardpoi[3])-1] = state('W', int(boardpoi[3])-1)
    board = np.array(board)

    q_Learning()

    if boardpoi[4] == 'q':
        print_Q(int(boardpoi[5])-1)
    else:
        print_policy()