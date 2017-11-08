from PageRank import *
import time

start_time = time.time()
data_file = "G:\\Study\\Programming\\Python\\Pagerank-for-Information-Retrieval-in-Python\\Datasets\\sx-mathoverflow.txt"
##data_file = "G:\\Study\\Programming\\Python\\Pagerank-for-Information-Retrieval-in-Python\\Datasets\\Wiki-Vote.txt"
is_page_no_zero_indexed = False
epsilon = 0.00001
max_iterations = 10
beta = 0.85

PgRank = PageRank(data_file, is_page_no_zero_indexed, max_iterations, beta, epsilon)
print("Rank Vector:")
for i in PgRank.rank_vector[:10]:
    print(i)
    
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
