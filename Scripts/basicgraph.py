import numpy as np
import shutil
import math
import webbrowser
from graphviz import Source
import os

class basicgraph:

   def __init__(self):
      self.set_nodes = 0
      self.set_conn = 0 

   def setNodes(self,nodelist,labels):
      self.nodes = nodelist
      self.labels=labels
      self.set_nodes = 1

   def setConnections(self,connections):
      if self.set_nodes == 0 :
         sys.error("nodes should be set before connections are set")
      if connections.shape[0]!=len(self.nodes) | connections.shape[1]!=len(self.nodes) :
         sys.error("mismatch for shape of connections array")  
      self.graph = connections 
      self.set_conn = 1

   def printNodeGraph(self,node):
      label = self.labels[self.nodes.index(node)]
      graphstr = "digraph { \n" 
      graphstr += "bgcolor=transparent \n" 
      graphstr += "node [style=rounded shape=box]\n" 
# Write this node
      graphstr += node + ' [style="bold,rounded" color=blue label=<' + label + '> URL="' + node + '.html" target="_top"];\n' 
# Write nodes with forward and backwards connections
      i = self.nodes.index(node)
      forwardnodes = []
      backnodes = []
      for j in range(0,len(self.nodes)):
          if self.graph[ i, j ] == 1 :
             graphstr += self.nodes[j] + ' [label=<' + self.labels[j] + '> URL="' + self.nodes[j] + '.html" target="_top"];\n' 
             graphstr += "edge[style=solid]; \n"
             graphstr += node + " -> " + self.nodes[j] + '\n'
             if (len(forwardnodes)>0) & (len(forwardnodes)%2==0) :
                 graphstr += "edge[style=invis];\n"
                 graphstr += forwardnodes[len(forwardnodes)-2] + " -> " + self.nodes[j] + '\n'
             forwardnodes.append(self.nodes[j])
          if self.graph[ j, i ] == 1 :
             graphstr += self.nodes[j] + ' [label=<' + self.labels[j] + '> URL="' + self.nodes[j] + '.html" target="_top"];\n' 
             graphstr += "edge[style=solid]; \n"
             graphstr += self.nodes[j] + " -> " + node + '\n'
             if (len(backnodes)>0) & (len(backnodes)%2==0) :
                 graphstr += "edge[style=invis];\n"
                 graphstr += backnodes[len(backnodes)-2] + " -> " + self.nodes[j] + '\n'
             backnodes.append(self.nodes[j])
      for i in range(0,math.floor(len(forwardnodes)/2)+1) :
          if len(forwardnodes)>2*i+2 :  
             graphstr += "{ rank=same; " + forwardnodes[2*i] + ";" + forwardnodes[2*i+1] + "; } \n" 
      for i in range(0,math.floor(len(backnodes)/2)+1) :
          if len(backnodes)>2*i+2 : 
             graphstr += "{ rank=same; " + backnodes[2*i] + ";" + backnodes[2*i+1] + "; } \n"
      graphstr += "}" 
      src = Source( graphstr, format='svg' )
      src.render("html/" + node) 
      # Delete the dot file
      os.remove("html/" + node)

   def printFullGraph(self,filename):
      if self.set_conn == 0 : 
         sys.error("graph must be set before print")  

      graphstr = "digraph { \n" 
      graphstr += "bgcolor=transparent \n" 
      graphstr += "node [style=rounded shape=box]\n" 
      for name in self.nodes :
          label = self.labels[ self.nodes.index(name) ]
          # Label here should be label from node file
          graphstr += name + ' [label=<' + label + '> URL="' + name + '.html" target="_top"];\n'  
      # And the connections
      for i in range(0,len(self.nodes)):
          for j in range(0,len(self.nodes)):
              if self.graph[i,j] == 1 :
                 graphstr += self.nodes[i] + " -> " + self.nodes[j] + '\n'
      # And finish printing the dot file
      graphstr += "}"   
      src = Source( graphstr, format='svg' )
      src.render("html/" + filename)
      # Delete the dot file
      os.remove("html/" + filename)

   def printGraphWithPath(self,topicpath,modulename):
    graphstr = "digraph { \n" 
    graphstr += "bgcolor=transparent \n" 
    graphstr += "node [style=rounded shape=box]\n" 
    for node_name in self.nodes :
        node_label = self.labels[self.nodes.index(node_name)]
        if node_name in topicpath :
            graphstr += node_name + ' [label=<' + node_label + '> URL="' + node_name + '.html" target="_top" penwidth=3 color=blue];\n' 
        else :
            graphstr += node_name + ' [label=<' + node_label + '> URL="' + node_name + '.html" target="_top"];\n' 
# And the connections
    for j in range(0,len(self.nodes)):
        for k in range(0,len(self.nodes)):
            if self.graph[j,k] == 1 :
               if (self.nodes[j] in topicpath) & (self.nodes[k] in topicpath) :
                  graphstr += self.nodes[j] + " -> " + self.nodes[k] + ' [penwidth=3 color=blue];\n'
               else :
                  graphstr += self.nodes[j] + " -> " + self.nodes[k] + '\n'

    graphstr += "}" 
    src = Source( graphstr, format='svg' )
    src.render("html/" + modulename)
    # Delete the dot file
    os.remove("html/" + modulename)


