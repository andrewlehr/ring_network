# Copyright 2023 Andrew Lehr
# The MIT License

import numpy as np

class RingNetwork:
    def __init__(self, params):
        self.params = params
        self._built = False
        self.weights = None
        self.I_E = None
        self.I_I = None
        self.P = None
        self.R = None
        
    def _connect(self):

        # determine center of gaussian kernel for neuron j
        c = self.params.shift % self.params.N

        # compute distance (counter clockwise) from neuron j to each of the other neurons i
        d = abs(self.params.x - c)

        # distance on circle is minimum of clockwise and counterclockwise distance
        dx = np.minimum(d, self.params.N-d)

        # compute the weights with gaussian kernel, parameters: w_E, w_I, shift, sigma
        weights = self.params.w_E*np.exp(-0.5 * dx**2/self.params.sigma**2) - self.params.w_I    
        
        # rescale weights by weight factor, computed within parameter class
        weights = self.params.weight_factor * weights
        
        # store weights
        self.weights = weights

    @property
    def W(self):
        W = np.zeros((self.params.N,self.params.N))
        for i in range(self.params.N):
            W[:, i] = np.roll(self.weights, i)
        return W
        
    def _set_inputs(self):   
        self.I_E = self.params.I_E
        self.I_I = self.params.I_I
        self.P = self.params.P
    
    def _after_run(self):
        pass
    
    def _build(self):
        self._connect()
        self._set_inputs()
        self._built = True
        
    def run(self):
        if self._built == False:
            self._build()
        
        W = self.W    
        r_store = np.zeros((self.params.N, self.params.T))
        r = self.params.initial_r
        
        for t in range(self.params.T):
            r_store[:, t] = r
            r = self.P * (W @ r + self.I_E - self.I_I)
            r[r<0] = 0
        
        self.R = r_store
    
        self._after_run()