import sys
import matplotlib.pyplot as plt
import math
from thesis_utilities import *
import argparse

nr_stats = 13
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
	
def make_comparison(case_list, name, different_conds=True, max_conds=None):
	# get data
	all_stats = []
	
	nr_lines = 0
	if different_conds:
		for i in range(len(case_list)):
			for case in case_list[i]:
				print(case)
				all_stats.append(get_values(folder+"\\"+case))
				nr_lines+=1
				if len(all_stats[-1][0])== 0:
					print(case, "NO DATA", "\n=====")
	else:
		for case in case_list:
			print(case)
			all_stats.append(get_values(folder+"\\"+case))		
			if len(all_stats[-1][0])== 0:
				print(case, "NO DATA", "\n=====")
		
	
	# make figures	
	if different_conds:
		if max_conds == None:
			colors = get_related_colors(len(case_list[0]), len(case_list))
		else:
			colors = get_related_colors(max_conds, len(case_list))			
	else:
		colors = get_colors()
	figs = []
	stat_nrs = [1,2,4,6,8,10]
	for stat_nr in stat_nrs:
		fig, ax = plt.subplots(1)
		if different_conds:
			case_nr = 0
			for i in range(len(case_list)):
				for j in range(len(case_list[i])):
					ax.plot(all_stats[case_nr][0], all_stats[case_nr][stat_nr], color=colors[i][j], linestyle='-', label=case_list[i][j])	
					case_nr+=1
		else:
			for case_nr in range(len(case_list)):
				ax.plot(all_stats[case_nr][0], all_stats[case_nr][stat_nr], color=colors[case_nr], linestyle='-', label=case_list[case_nr])	
		box = ax.get_position()
		ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
		if different_conds:
			col_len = int(math.ceil(nr_lines/2))
		else:
			col_len = int(math.ceil(len(case_list)/2))
		ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=col_len)
		ax.set_xlabel(labels[0])
		ax.set_ylabel(labels[stat_nr])
		ax.set_title(labels[stat_nr] + " comparison for different settings")
		image_name = folder + r"\_" + name + " " + labels[stat_nr] + ".pdf"
		fig.savefig(image_name, bbox_inches='tight')
		plt.close()
	
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Run puzzle algorithm')
	parser.add_argument("comparison", help="options: small, big")	
	
	args = parser.parse_args()
	kwargs = vars(args)	
	
	if kwargs["comparison"]=="small":
		shapes_stem = ["football_limit1000_stem","politics_limit1000_stem"]
		shapes_nostem = ["football_limit1000_no_stem","politics_limit1000_no_stem"]
			
		cases = []
		cases.append(shapes_stem)
		cases.append([x+"_stripy" for x in shapes_stem])
		cases.append([x+"_random" for x in shapes_stem])
		make_comparison(cases, "stem Different initializations")
		
		cases = []
		cases.append(shapes_nostem)
		cases.append([x+"_stripy" for x in shapes_nostem])
		cases.append([x+"_random" for x in shapes_nostem])
		make_comparison(cases, "nostem Different initializations")
		
		cases = []
		cases.append(shapes_stem)
		cases.append([x+"_noNoise" for x in shapes_stem])
		make_comparison(cases, "stem Effect of noise on normal")
		
		cases = []
		cases.append(shapes_nostem)
		cases.append([x+"_noNoise" for x in shapes_nostem])
		make_comparison(cases, "nostem Effect of noise on normal")
		
		
		cases = []
		cases.append([x+"_gold_noNoise" for x in shapes_stem])
		cases.append([x+"_gold" for x in shapes_stem])
		make_comparison(cases, "stem Effect of noise on gold")
		
		cases = []
		cases.append([x+"_gold_noNoise" for x in shapes_nostem])
		cases.append([x+"_gold" for x in shapes_nostem])
		make_comparison(cases, "nostem Effect of noise on gold")
		
		cases = []
		cases.append(shapes_stem)
		cases.append([x+"_gold" for x in shapes_stem])
		make_comparison(cases, "stem Gold versus normal")
		
		cases = []
		cases.append(shapes_nostem)
		cases.append([x+"_gold" for x in shapes_nostem])
		make_comparison(cases, "nostem versus normal")
		
	elif kwargs["comparison"]=="big_noise":
		shapes = ["football_big_no_stem","football_big_stem","politics_big_no_stem","politics_big_stem"]
					
		cases = []
		cases.append(shapes)
		cases.append([x+"_noNoise" for x in shapes])
		make_comparison(cases, "Effect of noise on bigger grid")
	elif kwargs["comparison"]=="big_random":
		shapes = ["politics_big_stem_puzz","politics_big_stem_random"]
		
		make_comparison(shapes, "Effect of initialisation", different_conds = False)
	else:
		print("invalid option")
		
	print("==============\nDONE\n==============")
	
	
	
	