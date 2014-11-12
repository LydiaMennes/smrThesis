from __future__ import division
import datetime
import string
import sys
import oursql
import unicodedata
from collections import defaultdict
from thesis_utilities import *
from matplotlib import pyplot as plt
import numpy as np
import all_pairwise_distances as pwd

# lib_path = r"K:\Lydia\smrThesis\code\snowballstemmer-1.1.0\src\snowballstemmer"
lib_path = r"K:\Lydia\smrThesis\code\snowballstemmer-1.1.0\src"
sys.path.append(lib_path)
import snowballstemmer

def pairwise_dists():
	input = "football_small"
	output = "football_small"
	
	input_dir = r"D:\Users\Lydia\results word cooc" + "\\" + input + r"\complete_cooc"
	output_dir = r"D:\Users\Lydia\pairwise_dists" + "\\" + output
	
	pwd.all_differences_to_csv(output_dir, input_dir)
	

def test_stemmer():
	stemmer = snowballstemmer.stemmer('dutch');
	print(stemmer.stemWords("aanbevelen aanbeveling aanbevelingen".split()))

def test_wordlists():
	dir = r"D:\Users\Lydia\results word cooc"
	wf = r"\complete_cooc\wordlist.txt"
	f1 = open(dir+r"\limit1000_nolog"+wf)
	f2 = open(dir+r"\limit1000_newsql"+wf)
	lst1 = []
	lst2 = []
	
	for w in f1:
		w = w.replace(r"\n", "")
		lst1.append(w)
		
	for w in f2:
		w = w.replace(r"\n", "")
		lst2.append(w)
		
	f = open(dir+"\wordlist_comparison.txt", "w")
	w1, w2 = 0,0
	for w in lst1:
		if w not in lst2:
			w1+=1
			f.write(w + " in nolog but not newsql \n")
			
	for w in lst2:
		if w not in lst1:
			w2+=1
			f.write(w + " in newsql but not nolog \n")
	f.write("total " + str(w1)+ " in nolog but not newsql and " +str(w2)+" in newsql but not nolog")
	
def new_sql():
	stop_words = get_parabots_stopwords()
	silly_words = ["image", "afbeelding", "reageer"]
	a = defaultdict(int)
	conn = oursql.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop"
						  , use_unicode=False)
	curs = conn.cursor(oursql.DictCursor)
	# result = curs.execute('SELECT * FROM `some_table` WHERE `col1` = ? AND `col2` = ?',(42, -3))
	curs.execute('SELECT itemText, pubDate FROM newsitems WHERE sourceType = 2 LIMIT 1000')
	for row in curs:
		s_b = row['itemText']
		# print(s)
		# s = str(s)
		s_esc = s_b.decode('unicode-escape')
		# print("after decode", type(s_esc), s_esc[1:100], "\n")
		s_norm = unicodedata.normalize('NFKD', s_esc)
		# print("after normalize", type(s_norm), s_norm[1:100], "\n")
		s_asc = s_norm.encode('ascii', 'ignore')
		
		s = str(s_asc)
		# s = s_asc
		
		# print("after all", type(s), s[1:100], "\n")		
		punc_map = str.maketrans("","",string.punctuation)
		# s = s.translate(None, string.punctuation)
		
		s = esc_chars(s)
		# print("after replacement", s[1:100], "\n")
		s = s.translate(punc_map)
		text = s.split(" ")
		for word in text:
			if len(word)!=1 and word != "" and word not in stop_words and not has_digits(word) and word not in silly_words:				
				word = word.lower()
				a[word]+=1
		d = row['pubDate']
		# print(d, type(d), "\n\n\n")
	
	keys = list(a.keys())
	keys.sort()
	f = open("test_coding.txt", "w")
	for k in keys:
		f.write(k+" "+str(a[k])+"\n")
	f.close()
	
def test_related_colors():
	# 6 vars in 5 conditions
	nr_vars = 6
	nr_conds = 3
	colors = get_related_colors(nr_conds, nr_vars)
	fig = plt.figure()
	x = np.array(list(range(100)))
	nr=0
	for i in range(nr_vars):
		nr+=1
		for j in range(nr_conds):
			plt.plot(x, x*nr, c=colors[i][j])
			nr+=1
	plt.show()
      
def print_n_lines(f_in, f_out, n):
    f = open(f_in, 'r')
    f2 = open(f_out,'w')
    for i in range(n):
        line = f.readline()
        f2.write(line)
    f.close()
    f2.close()
 
def file_contains(fname, cont):
    f = open(fname, "r")
    k = 0
    for l in f:
        if cont in l:
            print("contains "+cont+"in line", k)
        k+=1
    f.close()
    print("DONE")

	
if __name__ == "__main__":

    # print_n_lines(r"D:\Users\Lydia\results_freqs\nn_data\politics_limit1000_no_stem.csv",r"D:\Users\Lydia\results_freqs\nn_data\check_politics.txt", 2)
    file_contains(r"D:\Users\Lydia\results_freqs\nn_data\patches_politics_limit_ns_patch_ndp5\patch_0_0\input\sample_in0000.txt", ";")

	# test_stemmer()
	# test_related_colors()
	# print("hoi")
	# pairwise_dists()
	# print("doei")

	# test_wordlists()
	# get_silly_words()
	
	# word_file = r"D:\Users\Lydia\results word cooc\limit1000_nolog\complete_cooc\wordlist.txt"
	# output_dir = r"D:\Users\Lydia\results puzzle\limit1000_nolog_random"
	# build_random_grid(word_file, output_dir)

	# old_stdout = sys.stdout
	# try:
		# mem_file = open("TEST_log.txt","w")
		# sys.stdout = mem_file
		# get_frequencies()
	# finally:
		# sys.stdout = old_stdout
		# mem_file.close()