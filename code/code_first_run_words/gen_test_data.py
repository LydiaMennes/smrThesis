import random
import os


if __name__ == "__main__":
	
	let1 = "abcde"
	let2 = "abcdefghijklmnopqrstuvwxyz"
	# let1 = "ab"
	# let2 = "abcdefghijklmnopqrst"
	
	result_path = r"D:\Users\Lydia\results word cooc\test2\complete_cooc"
	s = []
	for l1 in let1:
		for l2 in let2:
			s.append(l1+l2)
	
	if not os.path.exists(result_path):
		os.makedirs(result_path)	
		print "directory made"
	
	
	file_li = 0
	file_l = let1[file_li]
	f = open(result_path + r"\_"+let1[file_li]+".txt", "w")
	for l1 in s:
		if l1[0] != file_l:
			f.close()
			file_li+=1
			f = open(result_path + r"\_"+let1[file_li]+".txt", "w")
			file_l = let1[file_li]
		f.write(l1)			
		for l2 in s:
			if random.random() > 0.5:
				f.write(";"+l2+" "+str(random.randrange(1,4)))
				# f.write(";"+l2+" "+str(1))
		f.write(";\n")
	
	
	
	f = open(result_path + r"\wordlist.txt", "w")
	for i in s:
		f.write(i+"\n")
	f.close()