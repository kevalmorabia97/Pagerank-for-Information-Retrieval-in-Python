import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_nodes_from([1, 2, 3,4])
G.add_edges_from([(1,2),(3,1)])
nx.draw_networkx(G,with_labels=True, nodelist=[1,2], node_color='b', node_size=500)
nx.draw_networkx(G,with_labels=True, nodelist=[3,4], node_color='g', node_size=800)

#nx.draw(G,with_labels=True)
plt.show()


##import matplotlib.pyplot as plt
##
##import networkx as nx
##
##G=nx.cubical_graph()
##pos=nx.spring_layout(G) # positions for all nodes
##
### nodes
##nx.draw_networkx_nodes(G,pos,
##                       nodelist=[0,1,2,3],
##                       node_color='r',
##                       node_size=5000,
##                   alpha=0.8)
##nx.draw_networkx_nodes(G,pos,
##                       nodelist=[4,5,6,7],
##                       node_color='b',
##                       node_size=500,
##                   alpha=0.8)
##
### edges
##nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
##nx.draw_networkx_edges(G,pos,
##                       edgelist=[(0,1),(1,2),(2,3),(3,0)],
##                       width=8,alpha=0.5,edge_color='r')
##nx.draw_networkx_edges(G,pos,
##                       edgelist=[(4,5),(5,6),(6,7),(7,4)],
##                       width=8,alpha=0.5,edge_color='b')
##
##
### some math labels
##labels={}
##labels[0]=r'$a$'
##labels[1]=r'$b$'
##labels[2]=r'$c$'
##labels[3]=r'$d$'
##labels[4]=r'$\alpha$'
##labels[5]=r'$\beta$'
##labels[6]=r'$\gamma$'
##labels[7]=r'$\delta$'
##nx.draw_networkx_labels(G,pos,labels,font_size=16)
##
##plt.axis('off')
##plt.show()



##import matplotlib.pyplot as plt
##import networkx as nx
##
##G = nx.DiGraph()
##G.add_nodes_from([1,2,3,4,5])
##G.add_edges_from([(1,3),(1,4),(3,2)])
##G.add_edge(1, 2, weight=4.7 )
##G.add_edges_from([(3,4),(4,5)], color='red')
##G.add_edges_from([(1,2,{'color':'blue'}), (2,3,{'weight':8})])
##
##nx.draw(G)
##plt.draw()
##plt.show()



##import networkx as nx
##import numpy as np
##import matplotlib.pyplot as plt
##import pylab
##
##G = nx.DiGraph()
##
##G.add_edges_from([('A', 'B'),('C','D'),('G','D')], weight=1)
##G.add_edges_from([('D','A'),('D','E'),('B','D'),('D','E')], weight=2)
##G.add_edges_from([('B','C'),('E','F')], weight=3)
##G.add_edges_from([('C','F')], weight=4)
##
##
##val_map = {'A': 1.0,
##                   'D': 0.5714285714285714,
##                              'H': 0.0}
##
##values = [val_map.get(node, 0.45) for node in G.nodes()]
##edge_labels=dict([((u,v,),d['weight'])
##                 for u,v,d in G.edges(data=True)])
##red_edges = [('C','D'),('D','A')]
##edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]
##
##pos=nx.spring_layout(G)
##nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
##nx.draw(G,pos, node_color = values, node_size=1500,edge_color=edge_colors,edge_cmap=plt.cm.Reds)
##pylab.show()
