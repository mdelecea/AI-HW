import numpy as np
import re

def regex_input(inp):
    data = ["".join(x.split()) for x in re.split(r'[()]',inp[1:]) if x.strip()]
    return np.array([[int(x) for x in y.split(',')] for y in data])

def printout(out):
    for i in range(len(out)-1):
        print(str(round(out[i],2))+" ",end='')
    print(str(round(out[-1],2)))

if __name__ == "__main__":
    inp = input()
    data = regex_input(inp)
    if inp[0] == 'P':
        weights = np.zeros(2)
        i = 0
        while i < len(data)*100:
            g = np.dot(weights,data[i%len(data),:-1])
            if g >= 0:
                g = 1
            else:
                g = -1
            if g != data[i%len(data),-1]:
                weights = weights + -g*data[i%len(data),:-1]
            i = i+1
        
        printout(weights)
    else:
        weights = np.array([0.0,0.0])
        feats = data[:,0:-1]
        v = np.array(data[:,-1])
        i = 0
        for j in range(len(v)):
            if v[j] != 1:
                v[j] = 0
        while i <= 100:
            for i in range(len(v)):
                g = np.dot(weights,feats[i].T)
                for j in range(2):
                    weights[j] = weights[j] + 0.1*(v[i]-(1.0/(1+np.exp(-g))))*feats[i,j]
            i = i+1
        
        printout(1.0/(1+np.exp(-np.dot(weights, feats.T))))