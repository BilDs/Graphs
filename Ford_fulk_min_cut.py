class Graph:

    def __init__(self, graph, source, target):
        """Instantiate a Graph object based on a provided adjacency matrix,
        and two vertex labels designated as source and target. The adjacency
        matrix contains the capacities for each edge."""
        self.graph = graph  # Adjacency matrix
        self.s = source     # Source vertex
        self.t = target     # Target vertex
        self.processed = [] # Tracks processed vertices
        self.parent = []    # Reconstructs s-t path
        # A (deep) copy of the input graph's adjacency matrix. This becomes
        # the adjacency matrix for the residual graph (Gf).
        self.residual_graph = [row[:] for row in self.graph]


    def breadth_first_search(self):
        """A slightly modified BFS. The function returns a True/False indicating
        the presence or absence of an s-t path. It also updates the parent[]
        list with the information necessary to reconstruct the path."""
        # Reset list showing every vertex as not processed yet.
        self.processed = [ False ] * len(self.residual_graph)
        # Reset parent[] using -1 as surrogate for null.
        self.parent =  [ -1 ] * len(self.residual_graph) 
        # Setup the FIFO for bfs
        queue = []  
        # Initialize the queue
        queue.append(self.s)  
        # Mark source as processed
        self.processed[self.s] = True  
        # Explore the graph while queue is not empty.
        while queue:  
            # Obtain next-in-line vertex from q
            u = queue.pop(0)  
            # Look for adjacent vertices
            for v in range(len(self.residual_graph)):  
                # Consider only edges with capacity > 0 with endpoints that
                # have not been processed yet.
                if self.residual_graph[u][v] > 0 and not self.processed[v]:
                    # Queue up the endpoint for subsequent iteration
                    queue.append(v)
                    # Mark endpoint as processed
                    self.processed[v] = True
                    # Store the endpoint's parent ( u --> v)
                    self.parent[v] = u
                    # If endpoint is target vertex, we found an s-t path
                    if v == self.t:
                        return True
        return False


    def ford_fulkerson(self):
        """Implementation of the Ford-Fulkerson algorithm."""
        # Initialize max flow to 0
        max_flow = 0
        # Explore the residual graph as long as there is an s-t path in it.
        while self.breadth_first_search():
            # We are in the loop here because an s-t path exists in the residual 
            # graph; let's find how much fow we can push through this path. 
            # Look for the edge with the smallest (residual) capacity in the
            # path. That's the path's bottleneck and it determines how much
            # flow we can send through the path.

            # Minimum residual capacity of path
            mrc = float('inf')  
            # Start from the end of the s-t path
            y = self.t  
            # Walk back towards the source
            while y != self.s:
                x = self.parent[y] 
                # Compare mrc with capacity of edge x-->y
                mrc = min(mrc, self.residual_graph[x][y])
                y = x  # move to the previous vertex in the path
            # Count the min residual capacity towards the graph's max flow.
            max_flow += mrc
            # Update residual capacities in the residual graph.
            # Start from the end of the s-t path
            v = self.t
            # Loop until we reach the source of the s-t path.
            while v != self.s:
                # Parent of current vertex, so we now have edge u --> v
                u = self.parent[v]
                # Forward edge residual capacity
                self.residual_graph[u][v] -= mrc
                # Backward eddge residual capacity
                self.residual_graph[v][u] += mrc
                # Continue to the previous edge
                v = u
        # Here's the max flow of the input graph
        return max_flow
        

    def show_cut(self):
        
        #initialize as there is no s-t path and max flow=0 for our while loop   
        self.parent =  [ -1 ] * len(self.residual_graph)
        max_flow=0
        
        #as soon as there is a path s-t we will find the min capacity of the edges and increment our max flow with it 
        while self.breadth_first_search():
            path_flow= float("inf")
            self.s= self.t
            while(self.s!= self.t):
                path_flow= min(path_flow, self.graph[parent[self.t]][self.t])
                self.t=parent[self.t]
               
                #increment our max flow 
                max_flow+= path_flow 
                
                # update residual capacities of the edges and process u as last along our path
            
            v = self.t 
            while(v!= self.s): 
                u = parent[v] 
                self.graph[u][v] -= path_flow 
                self.graph[v][u] += path_flow 
                v = parent[v] 
  
        # compare the capacity of the edges, so find which are 0 in the residual graph and not null in the initiall graph  
        for i in range(len(self.graph)): 
            for j in range(len(self.graph)): 
                if self.residual_graph[i][j] == 0 and self.graph[i][j] > 0 and i!= self.s: 
                    print((i,j))