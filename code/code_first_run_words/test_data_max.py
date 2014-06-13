import psutil
folder = r"D:\Users\Lydia\results word cooc\cutoff_3\complete_cooc"

letters = "abcdefghijklmnopqrstuvwxyz"

lst = []
i=0
for l in letters:
	f = open(folder + r"\_" + l + ".txt", "r")
	for l in f:
		l = l.replace(";\n", "")
		l = l.split(";")
		lst.append([l[0]])
		del l[0]
		for elem in l:
			elem = elem.split(" ")
			lst[i].append((elem[0], float(elem[1])))
			
		i+=1
		if i%10000 == 0:
			print i, "\nmemory:\n", psutil.virtual_memory()
	f.close()
	
print "final usage:",  psutil.virtual_memory()