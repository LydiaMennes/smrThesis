import sys
lib_path = r"K:\Lydia\code\tsne_python"
print lib_path
sys.path.append(lib_path)

import tsne
import space_to_grid as stg
import numpy as np
from collections import defaultdict
import eigennamen_visualizeGrid as viz

def data_2d_to_file(data, suffix, indexes):
	size = data.shape
	file = open(r"results\tsne_result_2d_"+ suffix+ ".txt",'w')
	for i in range(size[0]):
		file.write(indexes[i] + " ")
		for j in range(size[1]):
			file.write(str(data[i,j]) + " ")
		file.write("\n")
	file.close()
			

def grid_to_file(assignment, grid_size, suffix, indexes):
	empty_string = "-EMPTY-"
	print "gridsize = ", grid_size
	grid_w = []
	print "nr_grid_elems =", len(assignment)
	for i in range(grid_size):
		grid_w.append([])		
		for j in range(grid_size):
			grid_w[i].append(empty_string)
			
	for elem in assignment:
		if grid_w[grid_size-elem[1]-1][elem[0]] != empty_string:
			print "element gets overwritten in grid to file"
		grid_w[grid_size-elem[1]-1][elem[0]] = indexes[elem[2]]
	
	file = open(r"results\semantic_landscape_"+ suffix+ ".txt",'w')
	for i in range(grid_size):		
		for j in range(grid_size):
			file.write(grid_w[i][j] + "; ")
		file.write("\n")
	file.close()
	
def grid_to_file_latex(assignment, grid_size, suffix, indexes):
	empty_string = "-EMPTY-"
	print "gridsize = ", grid_size
	grid_w = []
	print "nr_grid_elems =", len(assignment)
	for i in range(grid_size):
		grid_w.append([])		
		for j in range(grid_size):
			grid_w[i].append(empty_string)
			
	for elem in assignment:
		if grid_w[grid_size-elem[1]-1][elem[0]] != empty_string:
			print "element gets overwritten in grid to file latex"
		grid_w[grid_size-elem[1]-1][elem[0]] = indexes[elem[2]]
	
	file = open(r"results\semantic_landscape_latex_"+ suffix+ ".txt",'w')
	file.write("{|")
	for i in range(grid_size):		
		file.write("c|")
	file.write("} \n")
	file.write(r"\hline")
	file.write("\n")
	for i in range(grid_size):
		second_line = []
		for j in range(grid_size):
			if grid_w[i][j]!= empty_string:
				a = grid_w[i][j].split("**")
				file.write(a[1])
				second_line.append(a[0])
			if j < grid_size-1:
				second_line.append(" & ")
				file.write(" & ")
		file.write(r"\\")
		file.write("\n")
		for st in second_line:
			file.write(st)
		file.write(r"\\")
		file.write("\n")		
		file.write(r"\hline ")
	file.close()
		

def get_data(data_file, word_file, nr_words, suffix):
	
	co_occ_file = open(data_file, 'r')
	indexes = {}
	reverse_index = {}
	indexes = defaultdict(lambda: -1, indexes)
	current_index = 0
	matrix = np.zeros( (nr_words, nr_words) )
	count = 0
	
	for line in co_occ_file:
		
		line = line.replace("\n", "")
		instance = line.split(",")
		if indexes[instance[0]] == -1:
			indexes[instance[0]] = current_index
			reverse_index[current_index] = instance[0]
			current_index+=1
		if indexes[instance[1]] == -1:
			indexes[instance[1]] = current_index
			reverse_index[current_index] = instance[1]
			current_index+=1
		matrix[ indexes[instance[0]], indexes[instance[1]] ] = float(instance[2])
		matrix[ indexes[instance[1]], indexes[instance[0]] ] = float(instance[2])
	
	print "nr words encoutnered in coocs:", current_index	
	co_occ_file.close()
	
	words = open(word_file, 'r')
	line_nr = 1
	for line in words:
		line_nr+=1
		instance = line.split(",")
		if indexes[instance[0]] == -1:
			indexes[instance[0]] = current_index
			reverse_index[current_index] = instance[0]
			current_index+=1
	
	print "nr_indexes naderhand: ", current_index
	
	sum_log = np.array([np.sum(matrix,1)]).T
	# iterate because there are a lot of zeros resulting in log(0) = -inf
	for i in range(nr_words):
		for j in range(nr_words):
			if matrix[i,j] != 0:
				matrix[i,j] = np.log(matrix[i,j])
		if sum_log[i,0] != 0:
			sum_log[i,0] = np.log(sum_log[i,0])			
	normalized = matrix - np.tile(sum_log, (1,nr_words))
	
	return matrix, reverse_index

'''	
def PCA(data, dims_rescaled_data=2):
    
    # returns: data transformed in 2 dims/columns + regenerated original data
    # pass in: data as 2D NumPy array
       
    mn = np.mean(data, axis=0)
    # mean center the data
    data -= mn
    # calculate the covariance matrix
    C = np.cov(data.T)
    # calculate eigenvectors & eigenvalues of the covariance matrix
    evals, evecs = LA.eig(C)
    # sorted them by eigenvalue in decreasing order
    idx = np.argsort(evals)[::-1]
    evecs = evecs[:,idx]
    evals = evals[idx]
    # select the first n eigenvectors (n is desired dimension
    # of rescaled data array, or dims_rescaled_data)
    evecs = evecs[:,:dims_rescaled_data]
    # carry out the transformation on the data using eigenvectors
    data_rescaled = np.dot(evecs.T, data.T).T
'''
	
	
def nse(data, nr_words):
	return tsne.tsne(data, 2, nr_words)
	
def space_to_grid(reduced_2):
	return stg.space_to_grid_iterative(reduced_2)

def get_semantic_landscape(nr_words, data_file, suffix, word_file):
	print "get data"
	(data, indexes) = get_data(data_file, word_file, nr_words, suffix)
	print "run nse"
	reduced_2 = nse(data, nr_words)
	print "data 2 file"
	data_2d_to_file(reduced_2, suffix, indexes)
	print "make grid from space"
	(assignment, grid_size) = space_to_grid(reduced_2)
	grid_to_file(assignment, grid_size, suffix, indexes)
	grid_to_file_latex(assignment, grid_size, suffix, indexes)
	viz.visualize_grid(suffix, grid_size)
	print "+++++++++ DONE +++++++++++"
	
if __name__ == "__main__":
	nr_words = 150
	data_file = r"results\person_coocs_all.txt"
	word_file = r"results\person_frequencies_all.txt"
	suffix = "eigennamen_all"
	
	# data_file = r"results\person_coocs_6000docs.txt"
	# word_file = r"results\person_frequencies_6000docs.txt"
	# suffix = "eigennamen_6000docs"
	
	get_semantic_landscape(nr_words, data_file, suffix, word_file)
	
	
