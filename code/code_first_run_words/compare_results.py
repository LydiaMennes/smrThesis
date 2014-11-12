import sys
import matplotlib.pyplot as plt
import math
from thesis_utilities import *
import argparse

nr_stats = 13
labels = []
folder = r"D:\Users\Lydia\results puzzle"
comparison_type = ""

size_h = 4.5
size_w = 3
fontsize = 10

def alternative_labels():
    labels = []
    labels.append("Trial number")
    labels.append("Nr of swaps")
    labels.append("Avg stress value")
    labels.append("Sd stress value")
    labels.append("Avg optimal semantic dist")
    labels.append("Sd optimal semantic dist")
    labels.append("Avg semantic dist to neighbors")
    labels.append("Sd semantic dist to neighbors")
    labels.append("Avg nr of encountered words")
    labels.append("Avg nr of encountered words")
    labels.append("Avg nr best match updates")
    labels.append("Sd nr best match updates")
    labels.append("Noise probability")
    return labels

def set_font(ax):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]+ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(fontsize)
        
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
        print( labels)
    return stats
    
def make_comparison(case_list, name, different_conds=True, max_conds=None):
    # get data
    line_styles = ["-","-","-",":","steps","","-."]
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
            # colors = get_related_colors(len(case_list[0]), len(case_list))
            colors = get_related_colors_new(len(case_list[0]))
        else:
            colors = get_related_colors(max_conds, len(case_list))            
    else:
        colors = get_colors()
    figs = []
    stat_nrs = [1,2,4,6,8,10]
    
    # print("\n=============")
    # print( colors)
    # print()
    # print(case_list)
    # print("=============\n")
    
    for stat_nr in stat_nrs:
        fig, ax = plt.subplots(1)
        fig.set_figheight(4)
        fig.set_figwidth(4)
        
        if different_conds:
            case_nr = 0
            for i in range(len(case_list)):
                for j in range(len(case_list[i])):
                    if comparison_type=="small":
                        current_label = case_list[i][j].replace("_", " ").replace("limit1000","lim").replace(" no stem","").replace(" stem","").replace("noNoise", "no noise")
                    else:
                        current_label = case_list[i][j].replace("_", " ").replace("limit1000","lim")
                    ax.plot(all_stats[case_nr][0], all_stats[case_nr][stat_nr], color=colors[i][j], linestyle=line_styles[j], label=current_label)    
                    case_nr+=1
        else:
            for case_nr in range(len(case_list)):
                current_label = case_list[case_nr].replace("_", " ").replace("limit1000","lim").replace("no stem","").replace("stem","")
                ax.plot(all_stats[case_nr][0], all_stats[case_nr][stat_nr], color=colors[case_nr], linestyle='-', label=current_label)    
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.4, box.width, box.height * 0.6])
        # if different_conds:
            # col_len = int(math.ceil(nr_lines/2))
        # else:
            # col_len = int(math.ceil(len(case_list)/2))
        col_len = 2
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=col_len, prop={'size':fontsize})
        ax.set_xlim([0,all_stats[0][0][-1]])
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[stat_nr])
        ax.set_title(labels[stat_nr] + " in different settings")
        set_font(ax)
        
        image_name = folder + "\\" + name.replace(" ", "_") + "_" + labels[stat_nr].replace(" ", "_") + ".pdf"
        fig.savefig(image_name, bbox_inches='tight')
        image_name = folder + "\\" + name.replace(" ", "_") + "_" + labels[stat_nr].replace(" ", "_") + ".png"
        fig.savefig(image_name, bbox_inches='tight')
        plt.close()
    
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run puzzle algorithm')
    parser.add_argument("comparison", help="options: small, big_noise, big_random, stem")    
    
    args = parser.parse_args()
    kwargs = vars(args)   

    comparison_type=kwargs["comparison"]
    
    labels.extend(alternative_labels())
     
    
    if comparison_type=="stem":
        shapes_stem = ["politics_limit1000_stem","politics_limit1000_no_stem"]
        shapes_nostem = ["football_limit1000_stem","football_limit1000_no_stem"]
        
        cases = []
        cases.append(shapes_stem)        
        cases.append(shapes_nostem)        
        make_comparison(cases, "Stemming vs no stemming")
    
    elif comparison_type=="small":
        shapes_stem = ["football_limit1000_stem","politics_limit1000_stem"]
        shapes_nostem = ["football_limit1000_no_stem","politics_limit1000_no_stem"]
            
        cases = [[],[]]
        for i in range(len(shapes_stem)):
            cases[i].append(shapes_stem[i])
            cases[i].append(shapes_stem[i]+"_stripy")
            cases[i].append(shapes_stem[i]+"_random")        
        make_comparison(cases, "stem different initializations")
        
        cases = [[],[]]
        for i in range(len(shapes_nostem)):
            cases[i].append(shapes_nostem[i])
            cases[i].append(shapes_nostem[i]+"_stripy")
            cases[i].append(shapes_nostem[i]+"_random")
        make_comparison(cases, "no stem different initializations")
        
        cases = [[],[]]
        for i in range(len(shapes_stem)):
            cases[i].append(shapes_stem[i])
            cases[i].append(shapes_stem[i]+"_noNoise")        
        make_comparison(cases, "stem effect of noise on normal")
        
        cases = [[],[]]
        for i in range(len(shapes_nostem)):
            cases[i].append(shapes_nostem[i])
            cases[i].append(shapes_nostem[i]+"_noNoise")   
        make_comparison(cases, "no stem effect of noise on normal")
        
        
        cases = [[],[]]
        for i in range(len(shapes_stem)):
            cases[i].append(shapes_stem[i]+"_gold_noNoise")
            cases[i].append(shapes_stem[i]+"_gold")
        make_comparison(cases, "stem effect of noise on gold")
        
        cases = [[],[]]
        for i in range(len(shapes_nostem)):
            cases[i].append(shapes_nostem[i]+"_gold_noNoise")
            cases[i].append(shapes_nostem[i]+"_gold")
        make_comparison(cases, "no stem effect of noise on gold")
        
        cases = [[],[]]
        for i in range(len(shapes_stem)):
            cases[i].append(shapes_stem[i])
            cases[i].append(shapes_stem[i]+"_gold")
        # cases.append(shapes_stem)
        # cases.append([x+"_gold" for x in shapes_stem])
        make_comparison(cases, "stem gold versus normal")
        
        cases = [[],[]]
        for i in range(len(shapes_nostem)):
            cases[i].append(shapes_nostem[i])
            cases[i].append(shapes_nostem[i]+"_gold")
        make_comparison(cases, "no stem gold versus normal")
        
    elif comparison_type=="big_noise":
        shapes = ["football_big_no_stem","football_big_stem","politics_big_no_stem","politics_big_stem"]
                    
        cases = []
        cases.append(shapes)
        cases.append([x+"_noNoise" for x in shapes])
        make_comparison(cases, "Effect of noise on bigger grid")
    elif comparison_type=="big_random":
        shapes = ["politics_big_stem_puzz","politics_big_stem_random"]
        
        make_comparison(shapes, "Effect of initialisation big grid", different_conds = False)
    else:
        print("invalid option")
        
    print("==============\nDONE\n==============")
    
    
    
    