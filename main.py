from PageRank import *
import time

start_time = time.time()
##data_file = "Datasets/sx-mathoverflow.txt"
data_file = "Datasets/Wiki-Vote.txt"
##data_file = "Datasets/test.txt"
is_page_no_zero_indexed = False
epsilon = 0.00001
max_iterations = 10
beta = 0.85
display_network_after_each_iteration = True

PgRank = PageRank(data_file, is_page_no_zero_indexed, max_iterations, beta, epsilon, display_network_after_each_iteration)
print("Rank Vector:")
for i in PgRank.rank_vector[:10]:
    print(i)
    
max_no_of_nodes_to_show = 20
PgRank.display_network(PgRank.rank_vector, max_no_of_nodes_to_show)    
    
if(is_page_no_zero_indexed):
    teleport_set = [i for i in PgRank.matrix if i%500==0]
else:
    teleport_set = [i+1 for i in PgRank.matrix if i%500==0]
topic_specific_rank_vector = PgRank.topic_specific_page_rank(teleport_set)
print("Topic Specific Rank Vector:")
for i in topic_specific_rank_vector[:10]:
    print(i)

end_time = time.time()
time_taken = float(end_time-start_time)
print("\nTotal Running time:",time_taken, "secs")
