from semantic_distance import cosine_distance
import datetime
import os
from collections import defaultdict

def all_differences_to_csv(dir_out, dir_in):
	dists = defaultdict(lambda:defaultdict(int))
	representations = []
	
	letters = "abcdefghijklmnopqrstuvwxyz"
	template = dir_in + r"\_"
	for l in letters:
		print("letter", l,datetime.datetime.now())
		try:
			inf = open(template+l+".txt", "r")
			# print("at file", l)
			#for each word
			for line in inf:
				line = line.replace(";\n", "")
				line = line.split(";")
				# print( line)
				word = line[0]
				del line[0]
				# build semantic representation
				if len(line)>0:
					# print("do word", word)
					rep = []
					for elem in line:
						# print( line)
						elem=elem.split(" ")
						# print(elem)
						rep.append([elem[0],float(elem[1])])
					# calc semantic difference with all other words in dict
					for [word2,rep2] in representations:
						d = cosine_distance(rep, rep2)
						# write to file
						if word<word2:
							dists[word][word2]=d
						else:
							dists[word2][word]=d
					representations.append([word,rep])
				else:
					print("word with no elements", word)
			inf.close()
		except IOError:
			pass
	print("stuff to file" ,datetime.datetime.now())
	if not os.path.exists(dir_out):
		os.makedirs(dir_out)	
	representations.sort()
	outf = open(dir_out+r"\complete_pairwise_dists_mat.txt","w")
	outf2 = open(dir_out+r"\wordlist.txt","w")
	i = 0
	j=0
	for [w1,x1] in representations:
		if j%100 == 0:
			print(j,"rows processed")
		j+=1
		outf2.write(w1+"\n")
		for [w2, x2] in representations:
			if i !=0:
				outf.write(",")
			if w1<w2:
				outf.write(str(dists[word][word2]))
			elif w2<w1:
				outf.write(str(dists[word2][word]))				
			else:
				outf.write("0.0")							
			i+=1
		outf.write("\n")
		i=0				
	outf2.close()		
	outf.close()	

def calc_all_differences(dir_out, dir_in):
	outf = open(dir_out+r"\complete_pairwise_dists.txt","w")
	representations = []
	
	letters = "abcdefghijklmnopqrstuvwxyz"
	template = dir_in + r"\_"
	for l in letters:
		try:
			inf = open(template+l+".txt", "r")
			# print("at file", l)
			#for each word
			for line in inf:
				line = line.replace(";\n", "")
				line = line.split(";")
				# print( line)
				word = line[0]
				del line[0]
				# build semantic representation
				if len(line)>0:
					# print("do word", word)
					rep = []
					for elem in line:
						# print( line)
						elem=elem.split(" ")
						# print(elem)
						rep.append([elem[0],float(elem[1])])
					# calc semantic difference with all other words in dict
					for rep2 in representations:
						d = cosine_distance(rep, rep2[1])
						# write to file
						outf.write(word +";"+ rep2[0]+";"+str(d)+"\n")
					representations.append([word,rep])
				else:
					print("word with no elements", word)
			inf.close()
		except IOError:
			None
			
	outf.close()	
		
	
if __name__ == "__main__":
	# input = r"\limit1000_nolog"
	# output = r"\limit1000_nolog"
	
	inputs = ["football_limit1000_no_stem","football_limit1000_stem","politics_limit1000_no_stem","politics_limit1000_stem"]
	outputs = ["football_limit1000_no_stem","football_limit1000_stem","politics_limit1000_no_stem","politics_limit1000_stem"]
	
	
	for i in range(len(inputs)):
		input = inputs[i]
		output = outputs[i]
		print("all pairwise distances for", input, datetime.datetime.now())
		input_dir = r"D:\Users\Lydia\results word cooc" + "\\" + input + r"\complete_cooc"
		output_dir = r"D:\Users\Lydia\results puzzle" + "\\" + output
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)	
			print("directory made", output_dir)
		calc_all_differences(output_dir, input_dir)
	print("DONE")