# Copyright 2023 Andrew Lehr
# The MIT License

import itertools
import warnings
import numpy as np

class Parameters:
    def __init__(self, params_to_update=None):
        '''
        define main parameters, derived parameters are computed below
        '''
        self.seed = 0              # seed for random number generator, affects which neurons get input
        self.T = 25                # number of time steps to run simulation
        self.N = 1000              # number of neurons
        self.shift_percent = 0.1  # percent shift of each neurons connectivity center
        self.sigma_percent = 0.15  # percent of distance on ring for gaussian kernel sigma, width
        self._w_E = 2.75           # exc recurrent weight factor, gets normalized below
        self._w_I = 1              # inh recurrent weight factor, gets normalized below
        self.N_E_in = 100          # number of excitatory input neurons, additive
        self.N_I_in = 100          # number of inhibitory input neurons, additive
        self.r_E_in = 0            # firing rate of excitatory input population, additive
        self.r_I_in = 0            # firing rate of excitatory input population, additive
        self.p_inh = 1             # percentage of neurons receiving inhibitory input
        self.p_exc = 1             # percentage of neurons receiving excitatatory input
        self.type = 'additive'     # type of interaction between neurons, additive or multiplicative
        self.stim = 'transient'    # type of input, persistent or transient
        self.rescale = True        # flag controls whether recurrent weights are rescaled based on sparsity
        
        '''
        if parameter updates are required, then update them
        '''
        self._update_params(params_to_update)
        
        '''
        based on main parameters compute the derived parameters
        '''
        self._compute_derived_params()
    
    def _update_params(self, params_to_update):
        # TODO should check that derived parameters are changed correctly
        if params_to_update is not None:
            for key_i, key in enumerate(params_to_update['keys']):
                if hasattr(self, key):
                    setattr(self, key, params_to_update['setting'][key_i])
                else:
                    warnings.warn("'" + key + "' is a derived parameter or doesn't exist. Setting derived parameters is not tested. \
                                  Could lead to unexpected effects due to parameter dependencies. Proceed with caution.")
            
    def _compute_derived_params(self):
        '''
        space parameters
        '''
        self.x = np.arange(self.N)                # defines each neurons position on the ring
        self.sigma = self.sigma_percent * self.N  # defines the std of the excitatory gaussian connectivity
        self.shift = self.shift_percent * self.N  # defines the amount of shift in the connectivity profile
        
        '''
        recurrent weights
        '''
        self.area = 2 * int(np.sum(np.exp(-0.5 * self.x**2/self.sigma**2))) # area under the gaussian connectivity kernel
        self.w_E = self._w_E/self.area                                # normalize exc weights
        self.w_I = self._w_I/self.area                                # normalize inh weights
        
        # compute rescaling for the recurrent weights if neurons are silenced
        #if self.p_exc != 0 and self.p_inh != 0:
        #    raise Exception("Simultaneous selective excitation and inhibition not yet implemented.")
        #else:
        
        if self.stim == 'transient' and self.p_inh != 1 and self.rescale == True:
            warnings.warn('Recurrent weights were rescaled due to selective inhibition and transient excitatory burst input.')
            self.weight_factor = (1 / (1 - self.p_inh)) #if self.p_inh <= 0.9 else 10 # removed this
        #elif self.stim == 'transient' and self.p_exc != 1:
        #    warnings.warn('Recurrent weights were rescaled due to selective excitation and transient excitatory burst input.')
        #    self.weight_factor = 1 + 0.15*np.exp(- self.p_exc)
        else:
            self.weight_factor = 1
        
        '''
        subset receiving selective input
        '''
        # set random number generator seed
        np.random.seed(self.seed)
        
        # calculate number of neurons that get selective exc or inh
        n_exc = int(self.p_exc * self.N)
        n_inh = int(self.p_inh * self.N)
        
        if (n_exc != self.p_exc * self.N): 
            warnings.warn('Number of neurons receiving selective excitation was rounded to ' + str(n_exc) + '.')
        if (n_inh != self.p_inh * self.N):
            warnings.warn('Number of neurons receiving selective inhibition was rounded to ' + str(n_inh) + '.')
        
        # select a subset from the N neurons to receive the input
        exc_neuron_indices = np.random.choice(self.N, n_exc, replace=False)
        inh_neuron_indices = np.random.choice(self.N, n_inh, replace=False)
        
        # initialize vectors for the selective subsets 
        self.sel_exc_subset = np.zeros(self.N)
        self.sel_inh_subset = np.zeros(self.N)
        
        # populate with ones for selected neurons
        self.sel_exc_subset[exc_neuron_indices] = 1
        self.sel_inh_subset[inh_neuron_indices] = 1
        
        # old way, problem is you get different sized subsets depending on random vector generated
        #self.sel_exc_subset = (np.random.rand(self.N) <= self.p_exc).astype(float)  # draw subset of neurons to receive selective excitation
        #self.sel_inh_subset = (np.random.rand(self.N) <= self.p_inh).astype(float)  # draw subset of neurons to receive selective inhibtion
        
        '''
        external inputs
        '''
        if self.type == 'additive':
            self.P = 1                 # set P to one for additive case
            self.w_E_in = self.w_E     # set exc input weight same as recurrent weight
            self.w_I_in = self.w_E     #self.w_I     # set inh input weight same as recurrent weight
            
            # calculate excitatory and inhibitory inputs
            self.I_E = self.w_E_in * self.r_E_in * self.N_E_in * self.sel_exc_subset
            self.I_I = self.w_I_in * self.r_I_in * self.N_I_in * self.sel_inh_subset
            
            if self.stim == 'transient':
                self.I_E = 0
            
        elif self.type == 'projection':
            if self.p_inh != 1:
                # neurons receiving inhibition get set to zero in P vector
                self.P = 1 - self.sel_inh_subset
            else:
                self.P = 1
            self.I_E = 0
            self.I_I = 0
        else:
            raise Exception("Keyword '" + str(self.type) + "' is not a valid type of input drive to the neurons. Please choose 'additive' or 'projection'.")
        
        
        '''
        initial rate distribution
        '''
        self.initial_bump_center = self.sigma # where the bump should start
        self.initial_bump_std = self.sigma    # width of the initial bump
        
        # initial rate distribution
        if np.sum(self.sel_inh_subset) == len(self.sel_inh_subset):                 # global inhibition
            active_neurons = self.sel_exc_subset
        elif np.sum(self.sel_inh_subset) != 0:                                      # selective inhibition
            active_neurons = 1 - self.sel_inh_subset
        elif np.sum(self.sel_inh_subset) == 0 and np.sum(self.sel_exc_subset) != 0: # no inhibition, selective excitation
            active_neurons = self.sel_exc_subset
        elif np.sum(self.sel_inh_subset) == 0 and np.sum(self.sel_exc_subset) == 0: # no inhibition or excitation
            active_neurons = 1
        else:
            warnings.warn('Something went wrong. Initial rate distribution is not set correctly.')
         
        # set initial rate dist
        self.initial_r = active_neurons * np.exp(-0.5 * (self.x - self.initial_bump_center)**2 / self.initial_bump_std**2)
        
        
        ''' WEIGHT FACTOR '''
        if self.stim == 'persistent' and self.rescale == True:
            if np.sum(active_neurons) != len(active_neurons): # and self.p_inh != 1:
                warnings.warn('Recurrent weights were rescaled.')
                percent_active = np.sum(active_neurons)/len(active_neurons)
                self.weight_factor = (1 / percent_active) # if percent_active >= 0.1 else 10 #removed this