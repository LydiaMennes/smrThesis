import sys
lib_path = "E:/tsne_python"
print lib_path
sys.path.append(lib_path)
import tsne
import numpy as NP
from collections import defaultdict
import mdp

#For politics 1 year 5000 articles: nr_functional_words = 59570
nr_functional_words = 59570
perplexity = 5
co_occ_doc = "freqCooc_ws5_Politics5000.txt"
co_occ_file = open(co_occ_doc, 'r')

indexes = {}
indexes = defaultdict(lambda: -1, indexes)
current_index = 0
matrix = NP.zeros( (nr_functional_words, nr_functional_words) )

count = 0

print "read data"
for line in co_occ_file:
	if count < 100:
		count += 1
		line = line.replace("\n", "")
		instance = line.split(" ")
		if(indexes[instance[0]] == -1):
			indexes[instance[0]] = current_index
			current_index+=1
		if(indexes[instance[1]] == -1):
			indexes[instance[1]] = current_index
			current_index+=1
		matrix[ indexes[instance[0]], indexes[instance[1]] ] = float(instance[2])
	else:
		break
		
	if count%10000 == 0:
		print count, "entries processed"
		
co_occ_file.close()

if current_index != nr_functional_words-1:
	print "not the same", current_index, nr_functional_words

print "perform pca"		
matrix = mdp.pca(matrix, 30)
print "pca done, start tsne"
	
#Y = tsne.tsne(X, no_dims, perplexity)
y = tsne.tsne(matrix, 2, nr_functional_words, perplexity)
