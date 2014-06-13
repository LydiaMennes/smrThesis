from __future__ import division
import MySQLdb
import nltk
import string
from nltk.corpus import stopwords
from collections import defaultdict
import re
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import unicodedata
from thesis_utilities import *

window_size = 8
query = "SELECT itemText FROM newsitems WHERE sourceType = 2"
remove_low_freq = True
stopwords_type = "parabots"
freq_cut_off = 0
data_directory = "default"
result_path = "default"
resultfolder = r"D:\Users\Lydia\results word cooc"
silly_words = ["image", "afbeelding", "reageer"]

def coocs_to_file_complete(cooc, tf_idf):
	print "complete coocs to distributed files"
	cooc_path = result_path + r"\complete_cooc"
	if not os.path.exists(cooc_path):
		os.makedirs(cooc_path)	
		print "directory made"
	words = tf_idf.keys()
	words.sort() 
	
	if remove_low_freq:
		for i in range(len(words))[::-1]:
			if tf_idf[words[i]][3] <= freq_cut_off:
				del words[i]
	print "remaining nr words: ", len(words)	
	filename_out = cooc_path + r"\wordlist.txt" 
	f = open(filename_out, 'w')
	for w in words:
		f.write(w + "\n")
	f.close()
	
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
	
	current_letter = "a"
	filename_out = cooc_path + r"\_"+current_letter+".txt" 
	f = open(filename_out, 'w')
	for w in words:
		if w[0] > current_letter and w[0] <= "z":			
			f.close()
			current_letter = w[0]
			print "letter", current_letter, "size cooc", sys.getsizeof(cooc)
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

	
def cooc_stats_to_file(cooc, tf_idf):
	non_zeros = defaultdict(lambda: [0,0] )
	for word1, dict in cooc.iteritems():
		for word2, freq in dict.iteritems():
			if freq == 0:
				print "zero entry gevonden!"
			if tf_idf[word1][3] > freq_cut_off:
				non_zeros[word1][0] += 1
			if tf_idf[word2][3] > freq_cut_off:
				non_zeros[word2][0] += 1
	filename_out = result_path + r"\cooc_stats.txt" 
	f = open(filename_out, 'w')
	for word in non_zeros.iterkeys():
		non_zeros[word][1] = tf_idf[word][3]
		f.write(word + " " + str(non_zeros[word][0]) + " " + str(non_zeros[word][1]) + "\n")
	f.close()
	
	values = zip(*non_zeros.values())
	fig = plt.figure(1)
	plt.scatter(np.log(values)[0,:], np.log(values)[1,:], c='r', marker='o')
	plt.xlabel("number of non-zero cooccurrence entries (log)")
	plt.ylabel("total word frequency (log)")
	image_name = result_path + r"\cooc_stats_log.pdf"
	fig.savefig(image_name, bbox_inches='tight')
	# plt.show()
	fig = plt.figure(1)
	plt.scatter(values[0], values[1], c='r', marker='o')
	plt.xlabel("number of non-zero cooccurrence entries")
	plt.ylabel("total word frequency")
	image_name = result_path + r"\cooc_stats_nolog.pdf"
	fig.savefig(image_name, bbox_inches='tight')
	# plt.show()

def stats_to_file(doc_nr, total_nr_words, nr_words, nr_entries, nr_words_single_freq, nr_included_words):
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
	f.write("stopwords type: " + stopwords_type + "\n")
	f.write("words containing numbers, stopwords and punctuation are removed\n")
	f.close()	
	
def word_stats_to_file(tf_idf):
	nr_words = 0
	nr_words_low_freq = 0	
	nr_included_words = 0
	filename_out = result_path + r"\tf_idf.txt" 
	f = open(filename_out, 'w')
	# Content file: word - total frequency - nr documents in which it appears - freq per document
	for word, lst in tf_idf.iteritems():
		nr_words+=1
		total_freq = sum(lst[1])
		tf_idf[word].append(total_freq)
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
	print "number of words:", nr_words
	return nr_words, nr_words_low_freq, nr_included_words

def coocs_to_file(cooc, tf_idf):
	filename_out = result_path + r"\coocs.txt" 
	f = open(filename_out, 'w')	
	nr_entries = 0
	# Normalize frequencies and write to file	
	for word1, dict in cooc.iteritems():
		for word2, freq in dict.iteritems():
			if not remove_low_freq:
				f.write(word1 + " " + word2 + " " + str(freq) + "\n")
				nr_entries += 1
			elif remove_low_freq and (tf_idf[word1][3] > freq_cut_off and tf_idf[word2][3] > freq_cut_off):
				f.write(word1 + " " + word2 + " " + str(freq) + "\n")
				nr_entries += 1
	print "nr cooc entries:", nr_entries
	f.close()
	return nr_entries
	
def get_cooccurrences(folder):
	db = MySQLdb.connect(host="10.0.0.125", # your host, usually localhost
						 user="Lydia", # your username
						  passwd="voxpop", # your password
						  db="voxpop") # name of the data base       
						  
	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cur = db.cursor()

	# Columns: 5 = itemText
	# Use all the SQL you like
	# Sourcetypes: 1 = algemeen, 2 = politiek, 3 = business

	print "Get items from database"	
	cur.execute(query)
	print "selection made"
	
	if stopwords_type == "nltk":
		stop_words = stopwords.words('dutch')
	elif stopwords_type == "parabots":
		stop_words = get_parabots_stopwords()
	
	# init dictionary
	cooc = defaultdict(lambda: defaultdict(int))
	# 1st element: nr of documents in which word appears, 2nd element: list of word frequencies in those documents, 3rd element: doc_nr of last doc in which it appeared
	tf_idf =  defaultdict(lambda: [0, [], -1])
	doc_nr = 1
	total_nr_words = 0
	
	for row in enumerate(cur.fetchall()):
		window = []
		current_word = -1;
		s = row[1][0]
		s = unicodedata.normalize('NFKD', s.decode('unicode-escape')).encode('ascii', 'ignore')
		s = s.replace("\n", "")
		s = s.translate(None, string.punctuation)
		text = s.split(" ")
				
		for word in text:			
			word = word.lower()
			if len(word)!=1 and word != "" and word not in stop_words and not has_digits(word) and word not in silly_words:				
				window.append(word)	
				total_nr_words+=1
		
				# Update current word position
				if len(window) < 2*window_size + 1 and len(window) >= window_size:
					current_word+=1
					#print "current word =", current_word
				
			
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
			print doc_nr, "files processed"
		doc_nr +=1	
	# Counts and list of words to file
	
	print "number of documents: " , doc_nr-1
	
	print "data processed, write to file"
	
	
	(nr_words, nr_words_single_freq, nr_included_words) = word_stats_to_file(tf_idf)
	
	nr_entries = coocs_to_file(cooc, tf_idf)
	
	stats_to_file(doc_nr, total_nr_words, nr_words, nr_entries, nr_words_single_freq, nr_included_words)	
	
	cooc_stats_to_file(cooc, tf_idf)	
	
	coocs_to_file_complete(cooc, tf_idf)
	
	del cooc
			
if __name__ == "__main__":
	
	# print "limited"
	# query = "SELECT itemText FROM newsitems WHERE sourceType = 2 LIMIT 1000"
	# data_directory = r"\limit1000_nolog"
	# result_path = resultfolder + data_directory
	# if not os.path.exists(result_path):
		# os.makedirs(result_path)	
		# print "directory made"	
	# freq_cut_off = 1
	# get_cooccurrences(data_directory)
	
	
	# query = "SELECT itemText FROM newsitems WHERE sourceType = 2"
	# print "cut off 3"
	# data_directory = r"\cutoff_3_nolog"	
	# result_path = resultfolder + data_directory
	# if not os.path.exists(result_path):
		# os.makedirs(result_path)	
		# print "directory made"	
	# freq_cut_off = 3
	# get_cooccurrences(data_directory)
	
	
	
	query = "SELECT itemText FROM newsitems WHERE sourceType = 2"
	print "cut off 10"
	data_directory = r"\cutoff_10_nolog"	
	result_path = resultfolder + data_directory
	if not os.path.exists(result_path):
		os.makedirs(result_path)	
		print "directory made"	
	freq_cut_off = 10
	get_cooccurrences(data_directory)
	
	
	# query = "SELECT itemText FROM newsitems WHERE sourceType = 2"
	# print "cut off 2"
	# data_directory = r"\cutoff_2"	
	# result_path = resultfolder + data_directory
	# if not os.path.exists(result_path):
		# os.makedirs(result_path)	
		# print "directory made"	
	# freq_cut_off = 2
	# get_cooccurrences(data_directory)

	
	# query = "SELECT itemText FROM newsitems WHERE sourceType = 2"
	# print "cut off 1"
	# data_directory = r"\cutoff_1"	
	# result_path = resultfolder + data_directory
	# if not os.path.exists(result_path):
		# os.makedirs(result_path)	
		# print "directory made"	
	# freq_cut_off = 1
	# get_cooccurrences(data_directory)
	
	
	# data_directory = r"\test"	
	# result_path = resultfolder + data_directory
	# c = defaultdict(lambda: defaultdict(int))
	# c["blaat"]["blub"] = 4
	# c["blaat"]["hoi"] = 2
	# c["hoi"]["jam"] = 3
	# c["blub"]["jam"] = 6
	# t = {}
	# t["blaat"] = (0,0,0,4)
	# t["blub"] = (0,0,0,4)
	# t["hoi"] = (0,0,0,4)
	# t["jam"] = (0,0,0,4)
	# coocs_to_file_complete(c, t)
	

	
	
	
	
	
	
	
	
	
	
	
	