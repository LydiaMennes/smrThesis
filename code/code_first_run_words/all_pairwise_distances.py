from semantic_distance import cosine_distance


def calc_all_differences(dir_out, dir_in):
	outf = open(dir_out+r"\complete_pairwise_dists.txt","w")
	representations = []
	
	letters = "abcdefghijklmnopqrstuvwxyz"
	template = dir_in + r"\_"
	for l in letters:
		try:
			inf = open(template+l+".txt", "r")
			print("at file", l)
			#for each word
			for line in inf:
				line = line.replace(";\n", "")
				line = line.split(";")
				print( line)
				word = line[0]
				del line[0]
				# build semantic representation
				if len(line)>0:
					print("do word", word)
					rep = []
					for elem in line:
						print( line)
						elem=elem.split(" ")
						print(elem)
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
	input = r"\limit1000_nolog"
	output = r"\limit1000_nolog"
	
	input_dir = r"D:\Users\Lydia\results word cooc" + input + r"\complete_cooc"
	output_dir = r"D:\Users\Lydia\results puzzle" + output
	calc_all_differences(output_dir, input_dir)