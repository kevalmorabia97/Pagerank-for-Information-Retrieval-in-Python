import time

class PageRank():
    
    def __init__(self, data_file, is_page_no_zero_indexed, max_iterations, beta, epsilon):
        assert beta>0 and beta<1
        self.is_page_no_zero_indexed = is_page_no_zero_indexed
        self.max_iterations = max_iterations
        self.beta = beta
        self.epsilon = epsilon
        
        t = time.time()
        print("\nReading file and creating adjacency list")
        f = open(data_file)

        adjacency_list={}
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
        print("Total No of Pages",self.no_of_pages)
        t = time.time()-t
        print("File read and Adjacency List creation time:",t,"secs")

        t = time.time()
        print("\nConstructing sparse matrix of in and out links")
        matrix = {}
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
    
    def page_rank(self):
        t = time.time()
        print("\nCalculating Page Rank")
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
            teleport_rank = leaked_rank/no_of_pages
            for i in range(no_of_pages):
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
        t = time.time()-t
        print("Page rank calculation time:",t,"secs")
        
        return rank_vector
    ######################### END OF PAGE RANK ################################

    #using topic specific page rank with teleport set = all pages
    def page_rank_2(self):
        if(self.is_page_no_zero_indexed):
            teleport_set = [i for i in range(self.no_of_pages)]
        else:
            teleport_set = [i+1 for i in range(self.no_of_pages)]
        return self.topic_specific_page_rank(teleport_set)    
    ######################## END OF PAGE RANK 2 ###############################

    #Takes care of dead ends
    def topic_specific_page_rank(self,teleport_set):
        t = time.time()
        print("\nCalculating Topic Specific Page Rank:")
        #print("Teleport Set",teleport_set)
        if(not self.is_page_no_zero_indexed):
            teleport_set = [i-1 for i in teleport_set]

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
            rank_vector = [[i,rank_vector[i]] for i in range(no_of_pages)]
        else:
            rank_vector = [[i+1,rank_vector[i]] for i in range(no_of_pages)]
        rank_vector = sorted(rank_vector, key = lambda x:x[1], reverse=True)
        t = time.time()-t
        print("Topic Specific Page rank calculation time:",t,"secs")

        return rank_vector        
    ################### END OF TOPIC SPECIFIC PAGE RANK #######################
    
    def display_network(self,rank_vector, max_nodes_to_show):
        print("Displaying webpages in the form of a network")
        #############
        ##REMAINING##
        #############
    ################### END OF DISPLAY NETWORK ################################
    
########################### END OF CLASS ######################################
