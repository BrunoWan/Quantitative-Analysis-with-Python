"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4DT(seed=1489683273):
    np.random.seed(seed)
    X = np.random.random((100, 4))

    Y = np.random.randn(100, )
   
    #for i in range(50):
    #        temp=float(np.random.randint(100, size=1)) 
    #        Y[np.min(X[:,1])+0.02*float(i)*(np.max(X[:,1])-np.min(X[:,1])) <X[:,1],]=temp
    Y=np.sqrt(1-(X[:,1])**2)     
    #Y = np.sin(X[:, 1]*100)
    #Y = 1/np.absolute(X[:, 0]) + 1/np.absolute(X[:, 1]) + 1/np.absolute(X[:, 2]) + 1/np.absolute(X[:, 3])
    #Y = X[:,0] + np.sin(X[:,1]) + X[:,2]**2 + X[:,3]**3
    return X, Y

def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    X = np.random.randn(100, 4)
    Y = X[:, 0] + X[:, 1]*float(np.random.randint(20, size=1))+ X[:, 2] *2 + X[:, 3] * 3
    #Y = np.random.random(size = (100,))*200-100
    return X, Y

def author():
    return 'ywan43' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
