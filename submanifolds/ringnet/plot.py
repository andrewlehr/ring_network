# Copyright 2023 Andrew Lehr
# The MIT License

import numpy as np
import matplotlib.pyplot as plt

class Plot:
    def __init__(self):
        self.tick_size = 13
        self.label_size = 16
        
    def weight_matrix(self, W, storage_loc=None, tick_sep=200):
        fig, ax = plt.subplots()
        im = ax.imshow(W, cmap='Greys')
        cb = plt.colorbar(im)
        cb.ax.tick_params(labelsize=self.tick_size)
        plt.xticks(np.arange(0,np.shape(W)[1]+1,tick_sep), fontsize=self.tick_size)
        plt.yticks(np.arange(0,np.shape(W)[0]+1,tick_sep), fontsize=self.tick_size)
        plt.xlabel('source', fontsize=self.label_size)
        plt.ylabel('target', fontsize=self.label_size)
        
        if storage_loc != None:
            plt.savefig(storage_loc, bbox_inches="tight")
        
        plt.show()
        
        
    def activity_raster(self, R, storage_loc=None, figsize=(6,3), title=None, xlabel='time step', interpolation='gaussian'):
        fig, ax = plt.subplots(figsize=figsize)
        im = ax.imshow(R, aspect='auto', cmap='Greys', origin='lower', interpolation=interpolation)
        cb = plt.colorbar(im)
        cb.ax.tick_params(labelsize=self.tick_size)
        cb.ax.get_yaxis().labelpad = 15
        cb.ax.set_ylabel('firing rate', fontsize=15)
        plt.xlim(0,)
        plt.xticks(fontsize=17)
        plt.yticks(fontsize=17)
        plt.xlabel(xlabel, fontsize=18)
        plt.ylabel('neuron', fontsize=18)
        
        if title != None:
            plt.title(title, fontsize=18)
        
        if storage_loc != None:
            plt.savefig(storage_loc, bbox_inches="tight")
        
        plt.show()
        
        
    def eigenspectrum(self, evals, storage_loc=None, figsize=(4,4), color='black', alpha=0.7, ylim=1.6, xlim=1.9, title=None):
        fig, ax = plt.subplots(figsize=figsize)

        # eigenvalues of weight matrix, W
        plt.scatter(evals.real, 
                    evals.imag, s=120, color=color, alpha=alpha)

        # formatting plot
        plt.xlabel('real part', fontsize=self.label_size)
        plt.ylabel('imaginary part', fontsize=self.label_size)
        ax.tick_params(axis='both', which='major', labelsize=self.tick_size)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_position('center')

        plt.grid(alpha=0.4)
        plt.ylim(-ylim, ylim)
        plt.xlim(-0.1, xlim)
        #plt.legend(fontsize=labelsize, frameon=False)

        if title != None:
            plt.title(title)
        
        if storage_loc != None:
            plt.savefig(storage_loc, bbox_inches="tight")
        plt.show()