import sys
import matplotlib.pyplot as plt
import math
from thesis_utilities import *

nr_stats = 12
labels = []
folder = r"D:\Users\Lydia\results puzzle"

def get_values(dir):
	stats = []
	lbs = []
	for i in range(nr_stats):
		stats.append([])
	f = open(dir + r"\stats.txt", "r")
	line_nr = 0
	for line in f:
		elem_nr= 0
		line = line.replace("\n", "")
		line = line.split(";")
		if line_nr==0:
			lbs = line
		else:
			for elem in line:
				if elem_nr <2:
					stats[elem_nr].append(int(elem))
				else:
					stats[elem_nr].append(float(elem))					
				elem_nr+=1		
		line_nr+=1
	f.close()
	if labels == []:
		print("add labels")
		for label in lbs:
			labels.append(label)
	return stats
	
def make_comparison(case_list, name):
	# get data
	all_stats = []
	for case in case_list:
		print(case)
		all_stats.append(get_values(folder+"\\"+case))		
		if len(all_stats[-1][0])== 0:
			print(case, "NO DATA", "\n=====")
		
		# if case == "limit1000_R_normEnc_withF":
			# print(len(all_stats[-1]), len(all_stats[-2]))
			# print(all_stats[-1])
			# print(all_stats[-2])
			
	
	# make figures
	colors = get_colors()
	figs = []
	stat_nrs = [1,2,4,6,8,10]
	for stat_nr in stat_nrs:
		fig, ax = plt.subplots(1)
		for case_nr in range(len(case_list)):
			ax.plot(all_stats[case_nr][0], all_stats[case_nr][stat_nr], color=colors[case_nr], linestyle='-', label=case_list[case_nr])	
		box = ax.get_position()
		ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
		col_len = int(math.ceil(len(case_list)/2))
		ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=col_len)
		ax.set_xlabel(labels[0])
		ax.set_ylabel(labels[stat_nr])
		ax.set_title(labels[stat_nr] + " comparison for different settings")
		image_name = folder + r"\_" + name + " " + labels[stat_nr] + ".pdf"
		fig.savefig(image_name, bbox_inches='tight')
		plt.close()
	
		
if __name__ == "__main__":
	# cases = ["limit1000_R_deepEnc_noF", "limit1000_R_deepEnc_withF", "limit1000_R_normEnc_noF", "limit1000_R_normEnc_withF","limit1000_GOLD_deepEnc_noF", "limit1000_GOLD_deepEnc_withF", "limit1000_GOLD_normEnc_noF", "limit1000_GOLD_normEnc_withF"]
	# make_comparison(cases, "all")
	
	# cases = ["limit1000_R_deepEnc_noF", "limit1000_R_deepEnc_withF", "limit1000_R_normEnc_noF", "limit1000_R_normEnc_withF"]
	# make_comparison(cases, "settings_test")
	
	# cases = ["limit1000_GOLD_deepEnc_noF", "limit1000_GOLD_deepEnc_withF", "limit1000_GOLD_normEnc_noF", "limit1000_GOLD_normEnc_withF"]
	# make_comparison(cases, "settings_gold")
	
	# cases = ["limit1000_R_deepEnc_noF","limit1000_GOLD_deepEnc_noF"]
	# make_comparison(cases, "Gold vs Test")
	
	cases = ["puzzle_on_random","limit1000_R_deepEnc_noF"]
	make_comparison(cases, "Preprocessing vs puzzle on random")
	
	
	
	
	
	
	