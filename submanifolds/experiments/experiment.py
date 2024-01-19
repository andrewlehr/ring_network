# Copyright 2023 Andrew Lehr
# The MIT License

from ..ringnet import Parameters
from ..ringnet import RingNetwork
from ..ringnet import Plot
import itertools

class Experiment:
    def __init__(self, params_to_set=None, params_to_iterate=None):
        self.params_to_set = params_to_set
        self.params_to_iterate = params_to_iterate
        self.parameter_settings = {}
        self.parameter_log = {}
        self.activity = {}
        
    def iterate(self):
        
        # combine all parameter settings into one dict
        self.parameter_settings.update(self.params_to_iterate)
        self.parameter_settings.update(self.params_to_set)
        
        # set up list of all possible combinations of the parameters
        self.param_space = list(itertools.product(*self.parameter_settings.values()))
        self.keys = [*self.parameter_settings.keys()]
        
        for setting in self.param_space:
            
            params_to_update = {'keys':     self.keys, 
                                'setting':  setting}
            
            print('\rCurrent setting: ' + str(self.keys) + str(setting), end='')
            
            parameters = Parameters(params_to_update)
            net = RingNetwork(parameters)
            net.run()
            
            #plot = Plot()
            #plot.activity_raster(net.R)
            
            self.parameter_log[setting] = parameters
            self.activity[setting] = net.R 
        