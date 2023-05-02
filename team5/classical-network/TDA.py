import sys, os
import numpy as np
import pandas as pd
from scipy import sparse
import gudhi

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from gtda.graphs import KNeighborsGraph
from scipy.sparse import coo_matrix
from gtda.homology import VietorisRipsPersistence
from gtda.diagrams import PersistenceLandscape

def generate_subgraphs(two_hop, A):
    #print(two_hop)
    n = len(two_hop)

    list_of_arrs = []
    for i in range(n): # this is looping over every vertex to find subgraph
        neighbor_indices = []
        for j_other in range(n): # looping through columns to find instances of 1 (which means it is a neighbor)
            if j_other == i or two_hop[i][j_other] == 1:
                neighbor_indices.append(j_other)
        
        n_prime = len(neighbor_indices)
        new_arr = np.zeros((n_prime, n_prime))
        for i_prime in range(n_prime):
            for j_prime in range(n_prime):
                new_arr[i_prime][j_prime] = A[ neighbor_indices[i_prime] ][ neighbor_indices[j_prime] ]
        
        #pgnew_arr = sparse.csr_matrix(new_arr)
        list_of_arrs.append(new_arr)
    
    return list_of_arrs




def two_hop_matrices(A):

    A_dense = A.A
    #print(A_dense)
    n = len(A_dense)
    two_hop_adj_matrix = np.zeros((n, n))

    for i_node in range(n):
        one_hop = np.nonzero(A_dense[i_node])[0]
        two_hops = []
        for i_other in one_hop:
            two_hops.append(i_other)
            two_hops.extend(np.nonzero(A_dense[i_other])[0])

        two_hops = np.unique(two_hops)
        for adj in two_hops:
            two_hop_adj_matrix[i_node][adj] = 1
    
    two_hop_adj_matrix -= np.eye(n)
    assert (two_hop_adj_matrix.T == two_hop_adj_matrix).all()

    out = generate_subgraphs(two_hop_adj_matrix, A_dense)

    return out
        



def get_topology_giotto(A):
    dist_mat = 1 - (A + np.eye(A.shape[0]))

    subs = two_hop_matrices(A)
    #print("subs", subs)
    VR = VietorisRipsPersistence("precomputed")
    return VR.fit_transform(subs)




import gudhi

def get_topology_gudhi(A):
    """
    Computes Betti numbers for all subgraphs of two-hop neighborhoods of nodes in a graph using Gudhi.
    Args:
        A: A numpy array representing an adjacency matrix of a graph.
    Returns:
        A list of Betti numbers (second homology groups) for all subgraphs of two-hop neighborhoods of nodes in the input graph.
    """

    # Get all subgraphs of two-hop neighborhoods of nodes in the graph
    subs = two_hop_matrices(A)

    # Visualize the subgraphs
    #visualize_graphs(subs)

    # Compute Betti numbers for each subgraph using Gudhi
    betti_features = []
    for sub in subs:
        # Compute the distance matrix for the subgraph
        sub = 1 - (sub + np.eye(sub.shape[0]))

        # Create a Rips complex using Gudhi
        rips_complex = gudhi.RipsComplex(distance_matrix=sub, max_edge_length=.5)

        # Create a simplex tree from the Rips complex
        simplex_tree = rips_complex.create_simplex_tree(max_dimension=1)

        # Print information about the Rips complex and its filtration
        result_str = 'Rips complex is of dimension ' + repr(simplex_tree.dimension()) + ' - ' + \
        repr(simplex_tree.num_simplices()) + ' simplices - ' + \
        repr(simplex_tree.num_vertices()) + ' vertices.'
        #print(result_str)

        # Compute the persistence of the simplex tree
        simplex_tree.compute_persistence(persistence_dim_max=5)

        # Append the Betti numbers to the list of features
        betti_features.append(simplex_tree.betti_numbers())

    # Return the second Betti number for each subgraph as the features
    return [[feature[1]] for feature in betti_features]


def visualize_graphs(adjacency_matrices):
    """
    Visualizes a list of graphs represented by adjacency matrices using NetworkX.
    Args:
        adjacency_matrices: A list of adjacency matrices, where each matrix represents a graph.
    Returns:
        None.
    """
    num_graphs = len(adjacency_matrices)
    fig, axs = plt.subplots(1, num_graphs, figsize=(4*num_graphs, 4))

    for i, adj_matrix in enumerate(adjacency_matrices):
        # Create a new graph object
        G = nx.Graph()

        # Add nodes to the graph
        num_nodes = adj_matrix.shape[0]
        G.add_nodes_from(range(num_nodes))

        # Add edges to the graph based on the adjacency matrix
        for j in range(num_nodes):
            for k in range(j, num_nodes):
                if adj_matrix[j, k] == 1:
                    G.add_edge(j, k)

        # Set the position of the nodes using the spring layout algorithm
        pos = nx.spring_layout(G)

        # Draw the graph
        nx.draw(G, pos=pos, with_labels=True, ax=axs[i])
        axs[i].set_title(f'Graph {i+1}')

    plt.show()


def add_value_to_inputs(inputs, value):
    """
    Adds a value at the end of every input in a set of inputs.
    Args:
        inputs: A list of input lists, where each input list contains parameters for an example.
        value: A list of values to be appended to each input.
    Returns:
        A new list of input lists with the value appended to each input.
    """
    # Check that the length of inputs and value are the same
    if len(inputs) != len(value):
        raise ValueError('The length of inputs and value must be the same.')

    # Create a new list of inputs with the value appended to each input
    new_inputs = [input_list + value[i] for i, input_list in enumerate(inputs)]

    return new_inputs




if __name__ == "__main__":

    DATA_PATH = '/data/experiment1/case30/graph_structured/'
    DATA_PATH = os.path.dirname(__file__)[:-11] + DATA_PATH

    A_train = np.load(DATA_PATH + 'A_train.npy', allow_pickle=True)

    mat = A_train[0]


    row  = np.array([0, 1, 2, 1, 3, 2, 0, 3, 4, 1])
    col  = np.array([1, 0, 1, 2, 2, 3, 3, 0, 1, 4])
    data = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    K4 = coo_matrix((data, (row, col)), shape=(5, 5))
    TDA = get_topology_gudhi(K4)

    # features = PersistenceLandscape(n_bins=10).fit_transform_plot(TDA)

    print(TDA)
    # print(features)
    # PersistenceLandscape(n_bins=10).plot(features[[0]])
