"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0
####################################################
        self.num_states=num_states
        self.num_actions=num_actions
        self.alpha=alpha
        self.gamma=gamma
        self.q_table=np.zeros([self.num_states,self.num_actions])
        self.rar=rar
        self.radr=radr
####################################################
        self.dyna=dyna
        self.tc_table=0.00001*np.ones([num_states,num_actions,num_states])
        self.t_table=self.tc_table/self.tc_table.sum(axis=2,keepdims=True)
        self.r_table=-1.0*np.ones([num_states,num_actions])

    def get_action(self, states):
        if rand.uniform(0.0, 1.0) <= self.rar:  # going rogue
            action = rand.randint(0, 3)
        else:
            action = self.q_table[states].argmax()

        self.rar = self.rar * self.radr
        return action


    def proc_dyna(self):
        s_samples = np.random.randint(0, self.num_states, int(1.02*self.dyna))
        a_samples = np.random.randint(0, self.num_actions, int(1.02*self.dyna))
        for i in range(int(1.02*self.dyna)):
            s = s_samples[i]
            a = a_samples[i]
            # Simulate an action with the transition model and land on an s_prime
            s_prime = np.argmax(np.random.multinomial(1, self.t_table[s, a, :]))
            # Compute reward of simulated action.
            r = self.r_table[s, a]
            # Update Q
            self.q_table[s, a] = (1 - self.alpha) * self.q_table[s, a] + self.alpha * (r + self.gamma * np.max(self.q_table[s_prime,:]))



    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        self.a=self.get_action(s)
        action =self.a
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """

        action = self.get_action(s_prime)
        self.q_table[self.s,self.a ] = (1 - self.alpha) * self.q_table[self.s, self.a] + self.alpha * (r + self.gamma * (self.q_table[s_prime, action]))

        if self.dyna!=0:
            self.tc_table[self.s, self.a,s_prime]= self.tc_table[self.s, self.a,s_prime]+1
            self.t_table=self.tc_table/self.tc_table.sum(axis=2,keepdims=True)
            self.r_table[self.s, self.a]=(1-self.alpha)*self.r_table[self.s, self.a]+self.alpha*r
            self.proc_dyna()


        self.s=s_prime
        self.a=action
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action



    def author(self):
        return 'ywan43'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"

