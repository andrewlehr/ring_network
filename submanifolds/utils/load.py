# Copyright 2023 Andrew Lehr
# The MIT License

import os
import os.path as path
import _pickle as cPickle

class DataManager:
    def __init__(self, exp_data_dir):
        self.root = path.abspath(path.join(__file__ ,"../../../..")) + '/'
        self.data_dir = self.root + 'data/'
        self.exp_dir = self.data_dir + exp_data_dir + '/'
        self.meta_dir = self.exp_dir + 'metadata/'
        self.sim_dir = self.exp_dir + 'simulation/'  
        self.eig_dir = self.exp_dir + 'eigendecomposition/' 
        self.bump_dir = self.exp_dir + 'bump_statistics/' 
        self.load_metadata()
    
    def load_metadata(self):
        with open(self.meta_dir + 'param_space.pkl', "rb") as f:
            self.param_space = cPickle.load(f)
        with open(self.meta_dir + 'params_to_set.pkl', "rb") as f:
            self.params_to_set = cPickle.load(f)
        with open(self.meta_dir + 'params_to_iterate.pkl', "rb") as f:
            self.params_to_iterate = cPickle.load(f)
        with open(self.meta_dir + 'keys.pkl', "rb") as f:
            self.keys = cPickle.load(f)
    
    def load_data(self, parameter_setting):
        filename = self.param_space.index(parameter_setting)
        name = self.sim_dir + str(filename) + '.pkl'
        with open(name, "rb") as f:
            return cPickle.load(f)
        
    def load(self, filename, location):
        name = str(location) + str(filename) + '.pkl'
        with open(name, "rb") as f:
            return cPickle.load(f)
        
    def save(self, data, filename, location):
        name = str(location) + str(filename) + '.pkl'
        with open(name, "wb") as f:
            return cPickle.dump(data, f)
        
        
        
        
        