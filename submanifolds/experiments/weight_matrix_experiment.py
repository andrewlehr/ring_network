# Copyright 2023 Andrew Lehr
# The MIT License

from ..ringnet import Parameters
from ..ringnet import RingNetwork
from ..ringnet import Plot
import itertools
import _pickle as cPickle
from datetime import datetime
import os
import os.path as path

class WeightMatrixExperiment:
    def __init__(self, params_to_set=None, params_to_iterate=None, name='weight_matrix_exp'):
        self.params_to_set = params_to_set
        self.params_to_iterate = params_to_iterate
        self.parameter_settings = {}
        self.datestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        self.name = name
        self.root = path.abspath(path.join(__file__ ,"../../../..")) + '/'
        self.exp_dir = self.root + 'data/' + self.name + '_' + self.datestamp + '/'
        self.meta_dir = self.exp_dir + 'metadata/'
        self.sim_dir = self.exp_dir + 'simulation/'
        self.eig_dir = self.exp_dir + 'eigendecomposition/'
        self.bump_dir = self.exp_dir + 'bump_statistics/' 
        self.setup()
    
    def setup_file_structure(self):
        if not os.path.isdir(self.exp_dir):
            os.mkdir(self.exp_dir)
            print('Created ' + self.exp_dir)
            
        if not os.path.isdir(self.sim_dir):
            os.mkdir(self.sim_dir)
            print('Created ' + self.sim_dir)
            
        if not os.path.isdir(self.meta_dir):
            os.mkdir(self.meta_dir)
            print('Created ' + self.meta_dir)
            
        if not os.path.isdir(self.eig_dir):
            os.mkdir(self.eig_dir)
            print('Created ' + self.eig_dir)
            
        if not os.path.isdir(self.bump_dir):
            os.mkdir(self.bump_dir)
            print('Created ' + self.bump_dir)
    
    def setup_parameter_space(self):
        # combine all parameter settings into one dict
        self.parameter_settings.update(self.params_to_iterate)
        self.parameter_settings.update(self.params_to_set)
        
        # set up list of all possible combinations of the parameters
        self.param_space = list(itertools.product(*self.parameter_settings.values()))
        self.keys = [*self.parameter_settings.keys()]
    
    def save_metadata(self):
        with open(self.meta_dir + 'params_to_set.pkl', "wb") as f:
            cPickle.dump(self.params_to_set, f)  
        with open(self.meta_dir + 'params_to_iterate.pkl', "wb") as f:
            cPickle.dump(self.params_to_iterate, f)
        with open(self.meta_dir + 'param_space.pkl', "wb") as f:
            cPickle.dump(self.param_space, f)  
        with open(self.meta_dir + 'keys.pkl', "wb") as f:
            cPickle.dump(self.keys, f)
        
    def save_data(self, counter, net):
        with open(self.sim_dir + str(counter) + '.pkl', "wb") as f:
            cPickle.dump(net, f)
            
    def setup(self):
        self.setup_file_structure()
        self.setup_parameter_space()
        self.save_metadata()
        
    def iterate(self):
        for counter, setting in enumerate(self.param_space):
            
            params_to_update = {'keys':     self.keys, 
                                'setting':  setting}
            
            print('\rCurrent setting: ' + str(self.keys) + str(setting), end='')
            
            parameters = Parameters(params_to_update)
            net = RingNetwork(parameters)
            net.run()
            
            self.save_data(counter, net)
        