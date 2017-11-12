# Pagerank for Information Retrieval in Python3
Rank the pages in the corpus by considering the inlinks and outlinks.
<br>Handling dead ends and spider traps.
<br>Topic Specific Page Rank and visualization of page links using igraph.

**Installing igraph in ubuntu:**
```
1. Install aptitude: sudo apt install aptitude
2. Installing the igraph C library: aptitude install build-essential libxml2-dev libglpk-dev libgmp3-dev libblas-dev liblapack-dev libarpack2-dev python-dev
3. pip3 install python-igraph
```

**Instructions on running the code**
```
1.Open main.py:
	A. Specify the data_file value.
	B. If page numbers in dataset are 0-indexed then set is_page_no_zero_indexed = True otherwise set it to False
	C. Set the value of epsilon for convergence
	D. Set max_iterations for calculating pageranks
	E. Set beta value which will be used to avoid spider traps and dead ends.
	F. set the value of display_network_after_each_iteration to True if you want to show the network structure after each iteration.
	G. Set the value of max_nodes_to_show which will specify how many of the top pages to show in the network structure/
	H. If you have a teleport_set then set the value of this list otherwise let it be the way it is.
	
2. Open terminal and change to the directory containing the main.py file

3. Type: python3 main.py
```
