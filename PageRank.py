import time
from igraph import *

class PageRank():
    ##Constructor
    def __init__(self, data_file, is_page_no_zero_indexed, max_iterations, beta, epsilon, display_network_after_each_iteration):
        assert beta>0 and beta<1
        self.is_page_no_zero_indexed = is_page_no_zero_indexed
        self.max_iterations = max_iterations
        self.beta = beta
        self.epsilon = epsilon
        self.display_network_after_each_iteration = display_network_after_each_iteration
        
        t = time.time()
        print("\nReading file and creating adjacency list")
        f = open(data_file)

        adjacency_list={} ## dictionary of list
        edges = [] ## list of tuples of the form (a,b) i.e. edge from a to b
        no_of_pages = 0
        while True:
            edge=f.readline()
            if(edge==''): #EOF
                break
            x = edge.split()
            if(len(x)==0):
                continue
            a = int(x[0])
            b = int(x[1])
            edges.append((a,b)) 
            if(not is_page_no_zero_indexed):
                a-=1
                b-=1
            if(a not in adjacency_list):
                adjacency_list[a] = []
            adjacency_list[a].append(b)   
            no_of_pages = max(a,b,no_of_pages)
        f.close()
        no_of_pages+=1 #0-indexed values
        self.no_of_pages = no_of_pages
        self.adjacency_list = adjacency_list
        self.edges = edges
        print("Total No of Pages",self.no_of_pages)
        t = time.time()-t
        print("File read and Adjacency List creation time:",t,"secs")

        t = time.time()
        print("\nConstructing sparse matrix of in and out links")
        matrix = {} ## Sparse Matrix Representation because NxN matrix for large number of pages cannot be fitted in RAM
        for i in range(no_of_pages):
            matrix[i] = {} #index from 0 to no_of_pages-1
        for i in adjacency_list:
            out_degree = len(adjacency_list[i])
            rank_given = 1/out_degree
            for j in adjacency_list[i]:
                #multiple outlinks to same pages possible
                matrix[j][i] = matrix[j].get(i,0)+rank_given
        self.matrix = matrix
        t = time.time()-t
        print("Matrix creation time:",t,"secs")
        
        self.rank_vector = self.page_rank()
        
    ###################### END OF CONSTRUCTOR #################################
    
    ## Returns rank_vector of the form [[4,0.45],[2,0.23],[0,0.19],[1,0.09],[3,0.04]] i.e. in decresing order of page ranks along with page numbers
    def page_rank(self):
        t = time.time()
        print("\nCalculating Page Rank")
        no_of_pages = self.no_of_pages
        initial_rank = 1/no_of_pages
        rank_vector = [initial_rank for i in range(no_of_pages)] # [1/N]Nx1

        for iteration in range(self.max_iterations):
            print("Iteration",iteration+1)
            # r = M x r
            next_rank_vector = [0 for i in range(no_of_pages)]
            for i in range(no_of_pages):
                for j in self.matrix[i]:
                    next_rank_vector[i] += self.matrix[i][j]*rank_vector[j]
                next_rank_vector[i] = self.beta*next_rank_vector[i]

            leaked_rank = 1 - sum(next_rank_vector)
            teleport_rank = leaked_rank/no_of_pages
            for i in range(no_of_pages):
                next_rank_vector[i] += teleport_rank
            
            done = True
            for i in range(no_of_pages):
                if(abs(rank_vector[i] - next_rank_vector[i])>self.epsilon):
                    done = False
                    break
            rank_vector = next_rank_vector
            
            if(self.display_network_after_each_iteration):
                if(self.is_page_no_zero_indexed):
                    temp = [[i,rank_vector[i]] for i in range(len(rank_vector))]
                else:
                    temp = [[i+1,rank_vector[i]] for i in range(len(rank_vector))]
                temp = sorted(temp, key = lambda x:x[1], reverse=True)
                self.display_network(temp, 20)            
            
            if(done):
                break

        rank_sum = sum(rank_vector)
        print("Sum of all ranks =",rank_sum)
        
        if(self.is_page_no_zero_indexed):
            rank_vector = [[i,rank_vector[i]] for i in range(len(rank_vector))]
        else:
            rank_vector = [[i+1,rank_vector[i]] for i in range(len(rank_vector))]
        rank_vector = sorted(rank_vector, key = lambda x:x[1], reverse=True)
        t = time.time()-t
        print("Page rank calculation time:",t,"secs")
        
        return rank_vector
    ######################### END OF PAGE RANK ################################

    #using topic specific page rank with teleport set = all pages
    def page_rank_2(self):
        if(self.is_page_no_zero_indexed):
            teleport_set = [i for i in range(self.no_of_pages)]
        else:
            teleport_set = [i+1 for i in range(self.no_of_pages)] #original page numbers were reduced by 1 so add 1 to bring to original page no
        return self.topic_specific_page_rank(teleport_set)    
    ######################## END OF PAGE RANK 2 ###############################

    #Takes care of dead ends
	#Teleport set contains original page numbers
    def topic_specific_page_rank(self,teleport_set):
        t = time.time()
        print("\nCalculating Topic Specific Page Rank:")
        print("Teleport Set",teleport_set)
        if(not self.is_page_no_zero_indexed):
            teleport_set = [i-1 for i in teleport_set] # bring to zero indexed pages

        no_of_pages = self.no_of_pages
        initial_rank = 1/no_of_pages
        rank_vector = [initial_rank for i in range(no_of_pages)]

        for iteration in range(self.max_iterations):
            print("Iteration",iteration+1)
            # r = M x r
            next_rank_vector = [0 for i in range(no_of_pages)]
            for i in range(no_of_pages):
                for j in self.matrix[i]:
                    next_rank_vector[i] += self.matrix[i][j]*rank_vector[j]
                next_rank_vector[i] = self.beta*next_rank_vector[i]

            leaked_rank = 1 - sum(next_rank_vector)
            teleport_rank = leaked_rank/len(teleport_set)
            for i in teleport_set:
                next_rank_vector[i] += teleport_rank
            
            done = True
            for i in range(no_of_pages):
                if(abs(rank_vector[i] - next_rank_vector[i])>self.epsilon):
                    done = False
                    break
            rank_vector = next_rank_vector
            
            if(done):
                break

        rank_sum = sum(rank_vector)
        print("Sum of all ranks =",rank_sum)

        if(self.is_page_no_zero_indexed):
            rank_vector = [[i,rank_vector[i]] for i in range(len(rank_vector))]
        else:
            rank_vector = [[i+1,rank_vector[i]] for i in range(len(rank_vector))]
        rank_vector = sorted(rank_vector, key = lambda x:x[1], reverse=True)
        return rank_vector        
    ################### END OF TOPIC SPECIFIC PAGE RANK #######################
    
    #Show network only of pages with top k=max_nodes_to_show page_ranks
	#PageRanks of the form [[4,0.45],[2,0.23],[0,0.19],[1,0.09],[3,0.04]] i.e. in decresing order of page ranks along with page numbers
    def display_network(self, page_ranks, max_nodes_to_show):
        print("\nDisplaying top", max_nodes_to_show, "webpages in the form of a network")
        g = Graph(directed = True)
        
        page_ranks = page_ranks[:max_nodes_to_show]
        new_labels = [] #labels of pages to be shown in graph
        edges_dict = {} #page number mapped to new edge number from 0 to max_nodes_to_show-1
        i = 0
        for p in page_ranks:
            edges_dict[p[0]] = i
            new_labels.append(p[0])
            #new_labels.append(str(p[0])+":"+str(p[1])[:6])
            i+=1
        
        new_edges = [(edges_dict[i[0]],edges_dict[i[1]]) for i in self.edges if i[0] in edges_dict and i[1] in edges_dict]
        
        g.add_vertices(len(page_ranks)) #vertices numbered 0 to len(page_ranks)-1
        g.add_edges(new_edges)
        page_ranks = [i[1] for i in page_ranks]
        
        visual_style = {}
        visual_style["vertex_size"] = [15000*i for i in page_ranks] # radius of nodes in proportion of their page ranks
        visual_style["vertex_label"] = new_labels
        visual_style["vertex_color"] = ["yellow","red","green","blue","purple","orange","pink"]
        out = plot(g, **visual_style)
        #out.save("Page Rank Network Structure.png")
    ################### END OF DISPLAY NETWORK ################################.

########################### END OF CLASS ######################################
