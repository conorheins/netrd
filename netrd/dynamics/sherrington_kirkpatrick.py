"""
sherrington_kirkpatrick.py
---------------------
Generate an ising model-like time series on a graph

author: Brennan Klein
email: brennanjamesklein at gmail dot com
submitted as part of the 2019 NetSI Collabathon
"""
from .base import BaseDynamics
import networkx as nx
import numpy as np

class SherringtonKirkpatrickIsing(BaseDynamics):

    def __init__(self):
        self.results = {}

    def simulate(self, G, L, noisy=False):
        """
        Simulate Kinetic Ising model dynamics on a ground truth network.
        from D. Sherrington and S. Kirkpatrick, Phys. Rev. Lett. 35, 1792 (1975)
        
        and from Hoang, D.T., Song, J., Periwal, V. and Jo, J., Network inference 
        in stochastic systems from neurons to currencies: Improved performance at 
        small sample size. (2019)

	    Generates an N x L time series.

        The results dictionary also stores the ground truth network as `'ground_truth'`.

	    Example Usage:
		#######
		G = nx.ring_of_cliques(4,16)
		L = 2001
		dynamics = SherringtonKirkpatrickIsing()
		TS = dynamics.simulate(G, L)
		#######
		
        Params
        ------
        G (nx.Graph): the input (ground-truth) graph with $N$ nodes.
        L (int): the length of the desired time series.

        Returns
        -------
        TS (np.ndarray): an $N \times L$ array of synthetic time series data.
        """

        N = G.number_of_nodes()
        
        # get transition probability matrix of G
        A = nx.to_numpy_array(G) 
        W = np.zeros(A.shape)
        for i in range(A.shape[0]):
            if A[i].sum()>0:
                W[i] = A[i]/A[i].sum()
        
        # initialize a time series of ones
        ts = np.ones((L, N))
        for t in range(1, L-1):
            h = np.sum(W[:,:] * ts[t,:], axis=1) # Wij from j to i
            p = 1 / ( 1 + np.exp(-2*h) )
            if noisy:
                ts[t+1,:] = p - np.random.rand(N)
            else:
                ts[t+1,:] = sign_vec(p - np.random.rand(N))


        self.results['ground_truth'] = G
        self.results['TS'] = ts.T

        return self.results['TS']


def sign(x):
    """
    np.sign(0) = 0 but here to avoid value 0, 
    we redefine it as def sign(0) = 1
    """
    return 1. if x >= 0 else -1.

def sign_vec(x):
    """
    Binarize an array
    """
    x_vec = np.vectorize(sign)
    return x_vec(x)
