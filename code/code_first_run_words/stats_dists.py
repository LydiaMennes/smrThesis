folder = r"D:\Users\Lydia\results puzzle"
import matplotlib.pyplot as plt
figure_size = 8
import numpy as np

def stats(dest_folder):
	f_in = open(dest_folder+r"\complete_pairwise_dists.txt", "r")
	values = []
	nr_ones = 0

	nr_entries = 0
	
	for line in f_in:
		line = line.replace("\n","")
		line = line.split(";")
		values.append(float(line[2]))
		nr_entries+=1
		if values[-1] == 1:
			nr_ones +=1
	f_in.close
	fig = plt.figure(figsize=(figure_size, figure_size))
	n, bins, patches = plt.hist(values, 50, log=True)
	fig.savefig(dest_folder+r"\dists_distribution.pdf", bbox_inches='tight')
	plt.close()
	values = np.array(values)	
	f_out = open(dest_folder+r"\dist_stats.txt","w")
	f_out.write("nr entries with distance 1:"+str(nr_ones))
	f_out.write("average:"+str(np.mean(values)))
	f_out.write("standard deviation:"+str(np.std(values)))
	print("Nr elems with distance 1:"+str(nr_ones))
	
if __name__ == "__main__":
	case_name = r"\limit1000_nolog"
	stats(folder+case_name)
