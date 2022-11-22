# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:07:05 2022

@author: kshah23
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

# Trust Networks
trust_network = pd.read_csv('../datasets/interpolation/masterEdgeList.csv', header=None)
trust_network.columns = ['from','to','weight']

# Transaction Networks
transaction_network = pd.read_csv('../datasets/Transactions/transaction_data_normalized.csv')
trans_nodes = transaction_network.Source.unique()

ma = max(max(trust_network['from']), max(trust_network['to']))
trans_numbers = []
for ite in range(1, ma+1):
    random_number = random.randrange(1,len(trans_nodes))
    while(random_number in trans_nodes):
        random_number = random.randrange(1,len(trans_nodes))
    trans_numbers.append(random_number)
#print(trans_numbers)

new_trans_nodes = []
for trans_number in trans_numbers:
    new_trans_nodes.append(trans_nodes[trans_number])

i = 0
network_nodes = []
for tn in new_trans_nodes:
    network_nodes.append(transaction_network[transaction_network['Source'] == tn])


trust_edges = []
for i in range(1,ma+1):
    tr_edge = pd.DataFrame(trust_network[trust_network['from']==i])
    tr_edge.columns = ['from','to','weight']
    for i,j in tr_edge.iterrows():  
        trust_edges.append((int(j['from']),int(j['to']),j['weight']*100))

G = nx.DiGraph()
G.add_weighted_edges_from(trust_edges, arrows=True)

edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())

options = {
    'node_color': 'orange',
    'node_size': 300,
    'width': 1,
    'arrowstyle': '-|>',
    'arrowsize': 10,
}
nx.draw(G, nx.circular_layout(G), with_labels = True, edge_color=weights, edge_cmap=plt.cm.Blues, arrows=True,  **options)
plt.show() # display


categories = set(transaction_network['Transaction_Type'])
default_attrs = {}
for cat in categories:
    default_attrs[cat] = 0
    
all_attrs = {}
for i in range(len(trans_numbers)):
    node_params = default_attrs.copy()
    all_attrs[i] = {}
    for cat in set(network_nodes[i-1]['Transaction_Type']):
        node_params[cat] = np.array(network_nodes[i-1][network_nodes[i-1]['Transaction_Type']==cat]['Weight'])[0]
        #node_params[cat] = np.array(network_nodes[i-1][[network_nodes[i-1]['Transaction_Type']==cat]]['Weight'])[0]
    all_attrs[i] = node_params