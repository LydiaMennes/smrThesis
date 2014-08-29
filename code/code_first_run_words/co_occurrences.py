from __future__ import division
import oursql
import string
from collections import defaultdict
import re
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import unicodedata
from thesis_utilities import *
import argparse
lib_path = r"K:\Lydia\smrThesis\code\snowballstemmer-1.1.0\src"
print( lib_path)
sys.path.append(lib_path)
import snowballstemmer
import datetime
import bisect

	

window_size = 8
query = "SELECT itemText FROM newsitems WHERE sourceType = "
remove_low_freq = True
freq_cut_off = 0
data_directory = "default"
result_path = "default"
resultfolder = r"D:\Users\Lydia\results word cooc"
silly_words = []

def coocs_to_file_complete(cooc, tf_idf, top_freq_cutoff):
	print("complete coocs to distributed files")
	cooc_path = result_path + r"\complete_cooc"
	if not os.path.exists(cooc_path):
		os.makedirs(cooc_path)	
		print("directory made")
	words = list(tf_idf.keys())
	words.sort() 
	
	f_top = open(result_path+r"\removed_top_freq_words.txt","w")
	nr_removed_top_freq_words = 0
	if remove_low_freq:
		for i in reversed(range(len(words))):
			word_freq = tf_idf[words[i]][3]
			if word_freq <= freq_cut_off or word_freq >= top_freq_cutoff:
				if word_freq >= top_freq_cutoff:
					f_top.write(words[i] + " "+ str(word_freq)+ "\n")
				del words[i]
	f_top.close()
	
	filename_out = cooc_path + r"\wordlist.txt" 
	f = open(filename_out, 'w')
	for w in words:
		f.write(w + "\n")
	f.close()
	nr_words = len(words)
	print( "remaining nr words: ", len(words), "words to file at", datetime.datetime.now()	)
		
	print("normalize coocs",datetime.datetime.now())
	# calculate row sums 
	row_sums = defaultdict(int)
	for w in words:
		for w2 in words:
			if w < w2:
				if cooc[w][w2] == 0:					
					del cooc[w][w2]
					if len(cooc[w])==0:
						del cooc[w]
				else:
					row_sums[w] += cooc[w][w2]
			else:
				if cooc[w2][w] == 0:
					del cooc[w2][w]
					if len(cooc[w])==0:
						del cooc[w]
				else:
					row_sums[w] += cooc[w2][w]
	
	print("coocs to file", datetime.datetime.now())
	current_letter = "a"
	filename_out = cooc_path + r"\_"+current_letter+".txt" 
	f = open(filename_out, 'w')
	for w in words:
		if w[0] > current_letter and w[0] <= "z":			
			f.close()
			current_letter = w[0]
			print( "letter", current_letter, "size cooc", sys.getsizeof(cooc))
			filename_out = cooc_path + r"\_"+current_letter+".txt" 
			f = open(filename_out, 'w')
			
		f.write(w + ";")
		for w2 in words:
			if w < w2:
				if cooc[w][w2] == 0:					
					del cooc[w][w2]
					if len(cooc[w])==0:
						del cooc[w]
				else:
					# norm_freq = np.log(cooc[w][w2]) - np.log(row_sums[w]) # use log prob
					norm_freq = cooc[w][w2] / row_sums[w] # dont use log prob
					f.write(w2 + " " + str(norm_freq)+";")
			else:
				if cooc[w2][w] == 0:
					del cooc[w2][w]
					if len(cooc[w])==0:
						del cooc[w]
				else:
					# norm_freq = np.log(cooc[w2][w]) - np.log(row_sums[w]) # use log prob
					norm_freq = cooc[w2][w] / row_sums[w] # dont use log prob
					f.write(w2 + " " + str(norm_freq)+";")
		f.write("\n")
	f.close()
	del cooc
	
	return nr_words

	
def cooc_stats_to_file(cooc, tf_idf):
	non_zeros = defaultdict(lambda: [0,0] )
	for word1, dict in cooc.items():
		for word2, freq in dict.items():
			if freq == 0:
				print("zero entry gevonden!")
			if tf_idf[word1][3] > freq_cut_off:
				non_zeros[word1][0] += 1
			if tf_idf[word2][3] > freq_cut_off:
				non_zeros[word2][0] += 1
	filename_out = result_path + r"\cooc_stats.txt" 
	f = open(filename_out, 'w')
	for word in non_zeros.keys():
		non_zeros[word][1] = tf_idf[word][3]
		f.write(word + " " + str(non_zeros[word][0]) + " " + str(non_zeros[word][1]) + "\n")
	f.close()
	
	values = list(zip(*non_zeros.values()))
	fig = plt.figure()
	plt.scatter(np.log(values)[0,:], np.log(values)[1,:], c='r', marker='o')
	plt.xlabel("number of non-zero cooccurrence entries (log)")
	plt.ylabel("total word frequency (log)")
	image_name = result_path + r"\cooc_stats_log.pdf"
	fig.savefig(image_name, bbox_inches='tight')
	plt.close()
	fig = plt.figure()
	plt.scatter(values[0], values[1], c='r', marker='o')
	plt.xlabel("number of non-zero cooccurrence entries")
	plt.ylabel("total word frequency")
	image_name = result_path + r"\cooc_stats_nolog.pdf"
	fig.savefig(image_name, bbox_inches='tight')
	plt.close()

def stats_to_file(doc_nr, total_nr_words, nr_words, nr_entries, nr_words_single_freq, nr_included_words, use_stemmer):
	filename_out = result_path+r"\stats.txt" 
	f = open(filename_out, 'w')
	f.write("window size: " + str(window_size) + "\n")
	f.write("number of documents: " + str(doc_nr-1) + "\n")
	f.write("total number of words: " + str(total_nr_words) + "\n")
	f.write("number of registered words: " + str(nr_words) + "\n")
	f.write("number of included words: " + str(nr_included_words) + "\n")
	f.write("number cooc entries: " + str(nr_entries) + "\n")
	f.write("number of words with freq "+str(freq_cut_off)+": " + str(nr_words_single_freq) + "\n")
	if remove_low_freq:
		f.write("words with a freq smaller or equal to " + str(freq_cut_off) +" are removed\n")
	else:
		f.write("words with all frequencies are included\n")
	if use_stemmer:
		f.write("Stemmer used\n")
	else:
		f.write("No stemmer used\n")
	f.write("words containing numbers, stopwords and punctuation are removed\n")
	f.close()	
	
def word_stats_to_file(tf_idf):
	nr_words = 0
	nr_words_low_freq = 0	
	nr_included_words = 0
	filename_out = result_path + r"\tf_idf.txt" 
	f = open(filename_out, 'w')
	# Content file: word - total frequency - nr documents in which it appears - freq per document
	top_fifty = []
	for word, lst in tf_idf.items():
		nr_words+=1
		total_freq = sum(lst[1])
		tf_idf[word].append(total_freq)
		if len(top_fifty)<50:
			top_fifty.append(total_freq)
			top_fifty.sort()
		elif top_fifty[0]<total_freq and total_freq not in top_fifty:
			del top_fifty[0]
			i = bisect.bisect(top_fifty, total_freq)
			top_fifty.insert(i,total_freq)
		if total_freq <= freq_cut_off:
			nr_words_low_freq += 1
		if remove_low_freq and tf_idf[word][3] > freq_cut_off:
			nr_included_words += 1
			f.write(word + " "+ str(total_freq) + " " + str(lst[0]) )
			for i in lst[1]:
				f.write(" " + str(i))
			f.write("\n")
		elif not remove_low_freq:
			f.write(word + " "+ str(total_freq) + " " + str(lst[0]) )
			for i in lst[1]:
				f.write(" " + str(i))
			
			f.write("\n")
	f.close()
	print( "number of words:", nr_words)
	return nr_words, nr_words_low_freq, nr_included_words, top_fifty[0]

def coocs_to_file(cooc, tf_idf):
	filename_out = result_path + r"\coocs.txt" 
	f = open(filename_out, 'w')	
	nr_entries = 0
	# Normalize frequencies and write to file	
	for word1, dict in cooc.items():
		for word2, freq in dict.items():
			if not remove_low_freq:
				f.write(word1 + " " + word2 + " " + str(freq) + "\n")
				nr_entries += 1
			elif remove_low_freq and (tf_idf[word1][3] > freq_cut_off and tf_idf[word2][3] > freq_cut_off):
				f.write(word1 + " " + word2 + " " + str(freq) + "\n")
				nr_entries += 1
	print("nr cooc entries:", nr_entries)
	f.close()
	return nr_entries

def isStupid(word):
	if len(word) >= 3:
		return word[0]==word[1] and word[1]==word[2]
	return False
	
def get_cooccurrences(folder, use_stemmer):
	conn = oursql.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop",
						  use_unicode = False) # name of the data base       
						  
	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	curs = conn.cursor(oursql.DictCursor)

	# Columns: 5 = itemText
	# Use all the SQL you like
	# Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business

	print( "Get items from database")
	curs.execute(query)
	print("selection made")
	
	stop_words = get_parabots_stopwords()
	stop_words.extend(get_english_stopwords())
	
	# init dictionary
	cooc = defaultdict(lambda: defaultdict(int))
	# 1st element: nr of documents in which word appears, 2nd element: list of word frequencies in those documents, 3rd element: doc_nr of last doc in which it appeared
	tf_idf =  defaultdict(lambda: [0, [], -1])
	doc_nr = 1
	total_nr_words = 0
	
	punc_map = str.maketrans("","",string.punctuation)
	exceptions = 0
	stemmer = snowballstemmer.stemmer('dutch');	

	for row in curs:
		window = []
		current_word = -1;
		s = row['itemText']
		try:
			s = unicodedata.normalize('NFKD', s.decode('unicode-escape')).encode('ascii', 'ignore')
			s = str(s)
			s = esc_chars(s)
			s = s.translate(punc_map)
			text = s.split(" ")
					
			for word in text:			
				word = word.lower()
				if len(word)!=1 and word != "" and word not in stop_words and not has_digits(word) and word not in silly_words and not isStupid(word):				
					
					if use_stemmer:
						word = stemmer.stemWord(word)
					window.append(word)	
					total_nr_words+=1
			
					# Update current word position
					if len(window) < 2*window_size + 1 and len(window) >= window_size:
						current_word+=1

					
				
					if current_word != -1:
						if len(window) > 2*window_size + 1:
							# Remove item from window
							window.pop(0)			
																		
						# Update counts
						for index, element in enumerate(window):
							if index != window_size:
								if window[current_word] < element:
									cooc[window[current_word]][element] += 1
								else:
									cooc[element][window[current_word]] += 1
					
					# Process tf-idf statistics
					if tf_idf[word][2] == doc_nr:							
						tf_idf[word][1][-1] += 1						
					else:
						tf_idf[word][0] += 1
						tf_idf[word][1].append(1) 
						tf_idf[word][2] = doc_nr
		except UnicodeDecodeError:
			exceptions+=1
						
		# Process final bits of window		
		while len(window) > window_size+1:
			window.pop(0)
			
			# Update counts
			for index, element in enumerate(window):
				if index != window_size:
					if window[current_word] < element:
						cooc[window[current_word]][element] += 1
					else:
						cooc[element][window[current_word]] += 1
			
			
			
		if doc_nr%10000 == 0:
			print( doc_nr, "files processed at", datetime.datetime.now())
		doc_nr +=1	
	# Counts and list of words to file
	
	print("number of documents: " , doc_nr-1)
	
	print( "data processed, write to file")
	print( "nr of exceptions:", exceptions)
	
	
	(nr_words, nr_words_single_freq, nr_included_words, top_freq_cutoff) = word_stats_to_file(tf_idf)
	
	nr_entries = coocs_to_file(cooc, tf_idf)
	
	nr_included_words = coocs_to_file_complete(cooc, tf_idf, top_freq_cutoff)
	
	stats_to_file(doc_nr, total_nr_words, nr_words, nr_entries, nr_words_single_freq, nr_included_words, use_stemmer)	
	
	cooc_stats_to_file(cooc, tf_idf)	
	
	
	del cooc
			
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Run puzzle algorithm')
	# '''parser.add_argument(<naam>, type=<type>, default=<default>, help=<help message>)'''
	parser.add_argument("case_name", help="Name of the data case that you want to process")
	parser.add_argument("article_type", help="Options: football or politics")
	parser.add_argument("--freq_cutoff", type=int, default=1, help="Name of the data case that you want to process")
	parser.add_argument("--query_limit", default=None)
	parser.add_argument("--use_stemmer", default="")
		
	args = parser.parse_args()
	kwargs = vars(args)	
	
	print( "\n\n\n")
	print( kwargs)
	
	data_directory = "\\" + kwargs["case_name"]
	if kwargs["article_type"]=="football":
		query = query + "1"
	elif kwargs["article_type"]=="politics":
		query = query + "2"
	else:
		print("UNRECOGNIZED ARTICLE TYPE")
		sys.exit()
		
	use_stemmer = True
	if kwargs["use_stemmer"]=="no":
		use_stemmer = False
	
	if kwargs["query_limit"]!=None:
		query = query + " LIMIT " + kwargs["query_limit"]
	freq_cut_off = kwargs["freq_cutoff"]
	silly_words.extend(get_silly_words())
	
	print("final query", "-"+query+"-")
	
	print( data_directory)
	print( "cutoff", freq_cut_off)
	result_path = resultfolder + data_directory
	if not os.path.exists(result_path):
		os.makedirs(result_path)	
		print( "directory made"	)
	get_cooccurrences(data_directory, use_stemmer)
	
	print("==============\nDONE\n==============")
	