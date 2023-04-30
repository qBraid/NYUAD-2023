# Smart Current: Blackouts are not just an inconvenience
<p align="center">
  <img src="images/logo.jpg"
  width=40%/>
</p>
https://smartcurrents.webflow.io/


## Project Description

In this project, we leverage quantum computing to solve the problem of power outages. Quantum-enhanced GNNs and quantum extracted topological features are used to regulate power flows and prevent blackouts.

## The Team
<p align="center">
  <img src="images/team.jpg"
  width=50%/>
</p>


## Our Approach

We have developed an algorithm to analyze power grids and monitor their stability in real-time. This algorithm identifies the topology of a power grid and analyzes node parameters such as power output and consumption to determine how stable the grid is. The goal of this algorithm is to prevent power grid failure by detecting any issues in real-time.

The classical algorithm works by finding the topological values associated with every node's two-hop neighborhood (all the nodes and connections within two steps of every node). We do this by running a topological data analysis (TDA) algorithm on every node's neighborhood, which identifies topological features such as holes and manifolds. This is added as a parameter to every node, so that we have information about every node's neighborhood. Then, we run a GNN (graph neural network) to identify how stable a power grid is. A graph neural network takes in a graph as input, so it is very practical for our use case of power grid analysis. 

The classical algorithm runs in super-polynomial time, meaning it is very slow for large power grids. We want the power grid analysis to run in real-time, and every check of the power-grid requires a topological analysis, so we need an improvement to our topological analysis. In other words, we need to speed-up our analysis and remain accurate. 

