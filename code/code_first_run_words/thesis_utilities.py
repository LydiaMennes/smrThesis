from collections import defaultdict
import numpy as np
import string
import re
from bisect import bisect_left
import random
import os
import datetime
from matplotlib import pyplot as plt
import pylab as P
from collections import defaultdict
import math
import time
import sys

empty = "-EMPTY-"

def check_word_freq(word):
    pol_folder = r"D:\Users\Lydia\results_freqs\freqs_per_day\politics_merged"
    mindate = datetime.date(2007,10,1)
    maxdate = datetime.date(2014,7,5)
    delta = datetime.timedelta(1)
    total_freq = 0
    freqs = []
    year = mindate.year
    while mindate <= maxdate:
        # print(mindate)
        if year != mindate.year:
            year=mindate.year
            print("year", year)
        good = True
        try:
            f = open(pol_folder+"\\words"+str(mindate)+".txt")
        except IOError:
            good = False
        if good:
            for line in f:
                line = line.split(";")
                if line[0] == word:
                    freq = float(line[1].replace("\n",""))
                    total_freq+=freq
                    freqs.append([mindate,freq])
                if line[0][0] > word[0]:
                    break
        mindate+=delta            
    print(freqs)
    print("total freq", total_freq)

def replace_silly_words_sequal(case_name, landscape_size, word_file="sillywords_sequal.txt"):
    landscape_file= r"D:\Users\Lydia\results puzzle"+"\\"+case_name+r"\grid_final.txt"
    landscape = grid_from_file(landscape_file)
    silly_words = get_silly_words_raw(word_file)
    new_landscape = []
    
    for i in range(landscape_size):
        new_landscape.append([])
        for j in range(landscape_size):
            if landscape[i][j] in silly_words:
                new_landscape[i].append(empty)
            else:
                new_landscape[i].append(landscape[i][j])
    
    output_folder = r"D:\Users\Lydia\results puzzle"+"\\"+case_name + "_swrem"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    grid_to_file_basic(output_folder, landscape_size, "final", new_landscape)    
    

def get_landscape_patch(case_name, i, j):
    f = open(r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\daily_freqs\patches\landscape_patch_"+str(i)+"_"+str(j)+".txt")
    result = []
    for line in f:            
        line = line.split(",")
        result.append(line[:-1])        
    return result 
    
def not_in_overlap(overlap, line_nr, elem_nr, bps):
    if line_nr > overlap and line_nr < bps-overlap:
        if elem_nr > overlap and elem_nr < bps-overlap:
            return True
    return False    

def translate(value, nr, overlap):
    if nr == 0:
        return value - overlap
    else:
        return value
    
def check_max_vals():
    # case_name = "politics_ad_lim_ns_strict_o2"
    case_name = r"Old\football_ad_lim_ns_strict"
    date = datetime.date(2007, 10, 1)
    max_date = datetime.date(2014, 7, 5)
    nr_patches = 5
    delta = datetime.timedelta(1)
    max_val = 0.8
    overlap = 2
    basic_patch_size = 18
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:[-1])))
    
    while date <= max_date:
        for i in range(nr_patches):
            for j in range(nr_patches):
                try:
                    f = open(r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\daily_freqs\patches\day"+str(date)+"\patch_"+str(i)+"_"+str(j)+".txt")
                    line_nr = 0
                    for line in f:
                        elem_nr=0
                        line = line.split(",")
                        for elem in line:
                            if float(elem) >= max_val and not_in_overlap(overlap, line_nr, elem_nr, basic_patch_size):
                                results[i][j][date]=[translate(line_nr,i,overlap), translate(elem_nr,j,overlap),float(elem)]                            
                            elem_nr+=1
                        line_nr+=1
                except FileNotFoundError:
                    pass
        date+=delta
    
    out_file = open(r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\result_max_val_inspection.csv","w")
    word_count = defaultdict(int)
    for i in range(nr_patches):
        for j in range(nr_patches):
            landscape_patch = get_landscape_patch(case_name, i, j)
            for key, value in results[i][j].items():
                if value[0] != -1:
                    out_file.write("patch, " + str(i) + ", " + str(j) + ", " + str(key) + ", " + str(value[2]) + " patchLoc, "+ str(value[0]) + ", " + str(value[1]) + ", " + landscape_patch[value[0]][value[1]]+"\n")
                    word_count[landscape_patch[value[0]][value[1]]]+=1
    out_file.close()
         
    out_file = open(r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\result_max_val_inspection_counts.csv","w")
    # out_file.write("\n\n===========================\n")
    for word, freq in word_count.items():
        out_file.write(word+","+str(freq)+"\n")
    out_file.close()
                    
def distribution_daily_docs(case_name):
    file_name = r"D:\Users\Lydia\results_freqs\freqs_per_day"+"\\"+case_name+r"\info.txt"
    f = open(file_name,"r")
    f.readline()
    dates = []
    nr_docs = []
    for l in f:
        l = l.split(";")
        d = l[0].split("-")
        d = [int(x) for x in d]
        dates.append(datetime.date(d[0],d[1],d[2]))
        nr_docs.append(int(l[1]))
    f.close()
    
    file_name = r"D:\Users\Lydia\results_freqs\freqs_per_day"+"\\"+case_name+r"\\"
    fig = plt.figure()
    ax = plt.subplot(111)
    plt.plot(list(range(len(dates))), nr_docs, 'r.')
    # plt.show()
    fig.savefig(file_name+"scatterplot_nr_docs_over_days.png")
    fig.savefig(file_name+"scatterplot_nr_docs_over_days.pdf")
        
    fig=plt.figure()
    plt.hist(nr_docs, bins=150)
    plt.title("Nr documents over days")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    # plt.show()
    fig.savefig(file_name+"histogram_nr_docs_over_days.png")
    fig.savefig(file_name+"histogram_nr_docs_over_days.pdf")

def process_dist_freqs(folder, values, nr_values, nr_zero_values, log_fig = True, nr_bins=150, suff = "", btf=False, btf_folder=None):
    figsize = (8,5)
    fig=plt.figure(figsize=figsize)
    [bin_values, bins, blaat] = plt.hist(values, bins=nr_bins)
    plt.title("Distribution over normalized word frequencies")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    # plt.show()
    fig.savefig(folder+"\\histogram_values_"+suff+".png")
    fig.savefig(folder+"\\histogram_values_"+suff+".pdf")
    plt.close()
    
    if btf:
        print(btf_folder)
        f = open(btf_folder+r"\bins.txt", "w")
        for i in range(len(bin_values)):
            f.write(str(bins[i])+" "+str(bins[i+1])+" "+str(bin_values[i])+"\n")        
        f.close()
    
    if log_fig:
        fig=plt.figure(figsize=figsize)
        plt.hist(np.log(np.array(values)), bins=nr_bins)
        plt.title("Distribution values")
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        # plt.show()
        fig.savefig(folder+"\\histogram_values_log_"+suff+".png")
        plt.close()
    
    print("nr values", nr_values)
    print("nr zero values", nr_zero_values)    
    print("percentage", nr_zero_values/nr_values)    

def distribution_values_normalized_by_max_freqs(case_name, fromdate, todate):
    folder = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\daily_freqs"
    delta = datetime.timedelta(1) 
    nr_values = 0
    nr_zero_values = 0
    values = []
    nr_good_docs = 0
    exceptions = 0
    while fromdate<=todate:
        good = True
        try:
            f = open(folder+"\\day"+str(fromdate)+".txt")
        except FileNotFoundError:
            exceptions+=1
            good = False                
            # print(folder+"\\day"+str(fromdate)+".txt")
            # sys.exit()
        if good:
            nr_good_docs+=1
            for line in f:
                line = line.split(",")
                for elem in line:
                    value = float(elem)
                    nr_values+=1
                    if value==0.0:
                        nr_zero_values+=1
                    else:
                        values.append(value)
        
        fromdate+= delta
        
    print("all collected\n", nr_values, nr_zero_values, len(values) , "nr docs", nr_good_docs)
    
    folder = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\daily_freqs"
    process_dist_freqs(folder, values, nr_values, nr_zero_values)
    
def distribution_values_normalized_by_max_freqs_patch(case_name, fromdate, todate, nr_patches):
    folder = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\daily_freqs\patches"
    delta = datetime.timedelta(1) 
    nr_values = 0
    nr_zero_values = 0
    values = []
    while fromdate<=todate:
        for i in range(nr_patches):
            for j in range(nr_patches):
                good = True
                try:
                    f = open(folder+"\\day"+str(fromdate)+"\\patch_"+str(i)+"_"+str(j)+".txt")
                except FileNotFoundError:
                    good = False                
                if good:
                    for line in f:
                        line = line.split(",")
                        for elem in line:
                            value = float(elem)
                            nr_values+=1
                            if value==0.0:
                                nr_zero_values+=1
                            else:
                                values.append(value)
        
        fromdate+= delta
    
    folder = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\daily_freqs"
    process_dist_freqs(folder, values, nr_values, nr_zero_values)

def get_normalized_values_whole_landscape(fromdate, todate, folder):
    delta = datetime.timedelta(1) 
    nr_values = 0
    nr_zero_values = 0
    values = []
    # print(fromdate, todate)
    while fromdate<=todate:        
        good = True
        try:
            # print(folder+"\\day"+str(fromdate)+".txt")
            f = open(folder+"\\day"+str(fromdate)+".txt")
        except FileNotFoundError:
            good = False                
        if good:
            # print("file found")
            for line in f:
                line = line.split(",")
                for elem in line:
                    value = float(elem)
                    nr_values+=1
                    if value==0.0:
                        nr_zero_values+=1
                    else:
                        values.append(value)
        fromdate+= delta
        # sys.exit()
                        
    return (values, nr_values, nr_zero_values)

def make_perc_bins(case_name, fromdate=None, todate=None, nr_bins = 50, suff=""):
    folder = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\daily_freqs"    
    if fromdate==None:
        fromdate = datetime.date(2007, 10,1)
    if todate==None:
        todate = datetime.date(2014,7,5)
        
    values, nr_v, nr_zv = get_normalized_values_whole_landscape(fromdate, todate, folder)
    print(nr_v, nr_zv)
    values.sort()
    boundary = math.floor((nr_v-nr_zv)/nr_bins)
    # print("boundary", boundary, nr_v, nr_zv, nr_bins)
    left_over = (nr_v-nr_zv)%boundary
    index = 0
    perc_bins = [0.0]
    for i in range(nr_bins-1):
        index+=boundary
        if left_over > 0:
            index+=1
            left_over-=1
        perc_bins.append(values[index])
        
    perc_bins.append(values[-1]*1.1)
    
    # for p in perc_bins:
        # print(p)
    
    out_folder = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\info_whole_landscape"
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    
    fig=plt.figure(figsize=(12,12))
    [bin_values, bins, blaat] = plt.hist(values, bins=perc_bins)
    plt.title("Distribution values")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    # plt.show()
    fig.savefig(out_folder+"\\histogram_perc_values"+suff+".png")
    fig.savefig(out_folder+"\\histogram_perc_values"+suff+".pdf")
    plt.close()
    
    f = open(out_folder+r"\binvalues_perc"+suff+".txt", "w")
    for i in range(len(bin_values)):
        f.write(str(bins[i])+" "+str(bins[i+1])+" "+str(bin_values[i])+"\n")        
    f.close()
    
def distribution_values_normalized_by_max_freqs_whole_landscape(case_name, fromdate=None, todate=None, make_log_fig = True, nr_of_bins = 200, suffix="", bins_to_file=False, bins_folder=None, make_perc_bins=False):
    folder = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\daily_freqs"
    
    if fromdate==None:
        fromdate = datetime.date(2007, 10,1)
    if todate==None:
        todate = datetime.date(2014,7,5)
    
    (values, nr_values, nr_zero_values) = get_normalized_values_whole_landscape(fromdate, todate, folder)
    
    folder = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\info_whole_landscape"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    if not bins_to_file:
        process_dist_freqs(folder, values, nr_values, nr_zero_values, log_fig=make_log_fig, nr_bins = nr_of_bins)    
    else:
        if bins_folder == None:
            print("no bins to file folder specified!")
        process_dist_freqs(folder, values, nr_values, nr_zero_values, log_fig=make_log_fig, nr_bins = nr_of_bins, suff = suffix, btf=bins_to_file, btf_folder=bins_folder)    

def has_digits (word):
    hd = re.compile('\d')
    return bool(hd.search(word))
    
def get_parabots_stopwords():
    filename = r"K:\Lydia\smrThesis\code\code_first_run_words\dutchStopwords.txt"
    return get_word_list(filename)
    
def get_english_stopwords():
    filename = r"K:\Lydia\smrThesis\code\code_first_run_words\english_stop_words.txt"
    return get_word_list(filename)
    

def four_digit_string(i):
    if i == 0:
        return "0000"
    elif i >=10000:
        return "TOO LARGE NUMBER"
    s = ""
    start = 1000
    while i/start < 1:
        s += "0"
        start = start / 10
    return s + str(i)
    
def grid_to_file(output_directory, grid_size, suffix, grid):
    f = open(output_directory + r"\grid_" + suffix +".txt", "w")    
    grid_size = int(grid_size)
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j]!= None:
                f.write(grid[i][j].name + " ; " )
            else:
                f.write(empty+" ; ")
        f.write("\n")
    f.close()
    
def grid_to_file_basic(output_directory, grid_size, suffix, grid):
    f = open(output_directory + r"\grid_" + suffix +".txt", "w")    
    grid_size = int(grid_size)
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j]!= None:
                f.write(grid[i][j] + " ; " )
            else:
                f.write(empty+" ; ")
        f.write("\n")
    f.close()
    
def get_colors():
    r = [[0,0,1], [1,0,0],[0,1,0],[0,1,1],[1,1,0],[0,1,0.5],[1,0,0.5],[0.5,1,0],[0,0.5,1],[1,0,1],[0.5,0,1],[1,0.5,0]]
    q = np.array(r)
    q = q*0.5
    r.extend(map(list,list(q)))
    return r
    
def space_to_file(data, filename):
    f = open(filename, "w")
    for i in range(data.shape[0]):
        f.write(str(data[i,0]) + "," + str(data[i,1])+"\n")
    f.close()

def space_from_file(filename):
    print(filename)
    f = open(filename, "r")
    d = []
    for line in f:
        line = line.replace("\n","")
        line = line.split(",")
        d.append([float(line[0]), float(line[1])])
    f.close()
    print("d", len(d))
    return np.array(d)
    
def grid_from_file(landscape_file):
    grid = defaultdict(lambda: defaultdict(lambda: None) )
    f = open(landscape_file)
    row = 0
    column = 0
    for line in f:
        line = line.replace(" ; \n", "")
        line = line.split(" ; ")
        for w in line:
            if w != empty:
                grid[row][column] = w    
            column += 1
        column = 0
        row+= 1    
    f.close()
    
    return grid
    
def grid_from_file_list(landscape_file, include_empty=True):
    grid = []
    f = open(landscape_file)    
    # i = 0
    for line in f:
        line = line.replace(" ; \n", "")
        line = line.split(" ; ")
        for w in line:
            if w != empty:
                grid.append(w)                    
                # if i < 10:
                    # print("-"+w+"-")
                # i+=1
            elif include_empty:
                grid.append(None)
    f.close()
    
    return grid
    
def esc_chars(s):
    s = s.replace(r"\a"," ")
    s = s.replace(r"\b"," ")
    s = s.replace(r"\f"," ")
    s = s.replace(r"\n"," ")
    s = s.replace(r"\x"," ")
    s = s.replace(r"\v"," ")
    s = s.replace(r"\r"," ")
    s = s.replace(r"\t"," ") 
    return s
    
def get_silly_words():
    return get_silly_words_raw("silly_words.txt")
    
def get_silly_words_raw(name):
    f = open(name,"r")
    words = []
    for line in f:
        line = line.replace("\n", "")
        words.append(line)
    f.close()
    return words
    
def get_word_list(file):
    f = open(file,"r")
    words = []
    for l in f:
        l = l.replace("\n","")
        words.append(l)
    f.close()
    return words

def build_random_grid(words, output_dir):
    print("nr words:", len(words))
    grid_size = int(np.ceil(np.sqrt(len(words))))
    print("grid_size", grid_size)
    nr_items = grid_size*grid_size
        
    if not os.path.exists(output_dir+r"\grids"):
        os.makedirs(output_dir+r"\grids")
    f = open(output_dir+r"\grids\random_grid.txt", "w")
    f2 = open(output_dir+r"\grid_final.txt", "w")    
    f3 = open(output_dir+r"\grid_initial.txt", "w")    
    for i in range(grid_size):
        for j in range(grid_size):
            ind = random.randrange(nr_items)
            if ind<len(words):
                f.write(words[ind]+" ; ")
                f2.write(words[ind]+" ; ")
                f3.write(words[ind]+" ; ")
                del words[ind]
            else:
                f.write(empty + " ; ")
                f2.write(empty + " ; ")
                f3.write(empty + " ; ")
            nr_items-=1
        f.write("\n")
        f2.write("\n")
        f3.write("\n")
    f.close()
    f2.close()
    f3.close()

def get_nr_words_from_stats(file_folder):
    f = open(file_folder+r"\stats.txt","r")
    for line in f:
        if "number of included words: " in line:
            line = line.replace("number of included words: ", "")
            line = line.replace("\n", "")
            included_words = int(line)
            break
    f.close()
    return included_words
    
def build_random_puzzle_result(landscape_file, out_folder):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    landscape = grid_from_file(landscape_file)
    grid_size = len(landscape)
    blob_size = grid_size//2
    blob_nr = 0
    freq = 0
    first = True
    word_list = []
    f = open(out_folder+r"\blob_file.txt","w")
    for i in range(grid_size):
        for j in range(grid_size):
            elem = landscape[i][j]
            if elem != None:
                # if elem == "strontrace":
                    # print("ENCOUNTERED")
                word_list.append(elem)
                if freq==blob_size or first:
                    if not first:
                        f.write("\n")
                    first = False
                    f.write(str(blob_nr) + " " + elem + " " + str(000) )
                    freq = 0
                    blob_nr+=1
                else:
                    f.write(" " + elem)
                    freq+=1
    f.close()
    build_random_grid(word_list, out_folder)
    
def get_related_colors(c, n):
    colors = np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1]])
    
    dif = 0.6/c
    if n > 6:
        print("too many colors")
    result = []
    for i in range(n):
        result.append([])
        for j in range(c):            
            result[i].append( list(colors[i,:]*(0.4+dif*j)))
     
                
    return result
    
def get_related_colors_new(n):
   
    result = []
    # politics = ["Aqua","DeepSkyBlue","DarkBlue"]
    if n == 2:
        politics = ["Aqua","Blue"]
        football = ["Gold","FireBrick"]        
    if n == 3:
        politics = ["Aqua","RoyalBlue","MidNightBlue"]
        football = ["Yellow","Orange","Red"]
    result.append(football)
    result.append(politics)                
    return result
    
def count_elems_on_first_line(file_name, separator, print_info = True, doubleSplit = False, sec_sep=""):
    f = open(file_name,"r")
    line = f.readline()
    line = line.split(separator)
    if doubleSplit:
        sum = 0
        for elem in line:
            elem = elem.split(sec_sep)
            print(len(elem))
            sum+=len(elem)
        print("sum", sum)
    else:
        if print_info:
            print("nr elems on first line:", len(line))
        else:
            return len(line)
        
def print_n_lines_file(file_name, n):
    f = open(file_name, "r")
    for i in range(n):
        l = f.readline()
        print(l)

def count_lines_file(file_name):
    f = open(file_name)
    i = 0
    for line in f:
        i+=1
    f.close()
    print("nr lines", i)

def check_lengths(filename, inputs, outputs):
    f = open(filename)
    index = 0
    for line in f:
        line = line.split(";")
        inps = line[0].split(",")
        otps = line[1].split(",")
        if len(inps)!=inputs:
            print("elem", index, "sucks inputs", len(inps))
        if len(otps)!=outputs:
            print("elem", index, "sucks outputs", len(otps))
            
        index+=1
        
    print("nr elems:", index)
    
def get_name_club_link(file_path):
    f = open(file_path)
    result = {}
    for line in f:
        line = line.replace("\n","")
        line = line.split(",")
        result[line[0]]=line[1]
    f.close()
    return result
    
def run_distr_max_all_case_names():
    # distribution_values_normalized_by_max_freqs_whole_landscape(case_name, fromdate=None, todate=None, make_log_fig = True, nr_of_bins = 200, suffix="", bins_to_file=False, bins_folder=None)
    tmpl1 = r"D:\Users\Lydia\results_freqs"
    tmpl2 = r"\info_whole_landscape"
    
    case_name = r"politics_lim_ns_swrem_whole_o2_logas"
    print("\nprocess", case_name)
    distribution_values_normalized_by_max_freqs_whole_landscape(case_name, make_log_fig = False, nr_of_bins=50, suffix="binz", bins_to_file=True, bins_folder=tmpl1+"\\"+case_name+tmpl2)
    
    case_name = r"politics_lim_ns_swrem_whole_o3_logas"
    print("\nprocess", case_name)
    distribution_values_normalized_by_max_freqs_whole_landscape(case_name, make_log_fig = False, nr_of_bins=50, suffix="binz", bins_to_file=True, bins_folder=tmpl1+"\\"+case_name+tmpl2)
        
    # case_name = r"football_lim_ns_swrem_whole_o2_logns"
    # print("\nprocess", case_name)
    # distribution_values_normalized_by_max_freqs_whole_landscape(case_name, make_log_fig = False, nr_of_bins=50, suffix="binz", bins_to_file=True, bins_folder=tmpl1+"\\"+case_name+tmpl2)
    
    # case_name = r"football_lim_ns_swrem_whole_o2_logas"
    # print("\nprocess", case_name)
    # distribution_values_normalized_by_max_freqs_whole_landscape(case_name, make_log_fig = False, nr_of_bins=50, suffix="binz", bins_to_file=True, bins_folder=tmpl1+"\\"+case_name+tmpl2)
    
    # case_name = r"football_lim_ns_swrem_whole_o2"
    # print("\nprocess", case_name)
    # distribution_values_normalized_by_max_freqs_whole_landscape(case_name, make_log_fig = False, nr_of_bins=50, suffix="binz", bins_to_file=True, bins_folder=tmpl1+"\\"+case_name+tmpl2)
   
def run_perc_bins_all_case_names():
    
    
    case_name = r"politics_names_allDocs_o0"
    print("\nprocess", case_name)
    make_perc_bins(case_name, nr_bins=5, suff="_5bins")
    
    case_name = r"politics_names_allDocs_o2"
    print("\nprocess", case_name)
    make_perc_bins(case_name, nr_bins=5, suff="_5bins")

    case_name = r"politics_names_allDocs_o2_random"
    print("\nprocess", case_name)
    make_perc_bins(case_name, nr_bins=5, suff="_5bins")
   
    
    # case_name = r"politics_lim_ns_random_swrem_o2_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=5, suff="_5bins")    
        
    # case_name = r"test"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=5, suff="_5bins") 

    # case_name = r"politics_lim_ns_swrem_whole_o0_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=5, suff="_5bins") 
    
    
    # case_name = r"politics_lim_ns_swrem_whole_o2_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=20, suff="_20bins") 

    # case_name = r"politics_lim_ns_swrem_whole_o2_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=5, suff="_5bins") 
    
    # case_name = r"politics_lim_ns_swrem_whole_o3_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=20, suff="_20bins")
    
    # case_name = r"politics_lim_ns_swrem_whole_o3_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=5, suff="_5bins") 
    
    # case_name = r"politics_lim_ns_random_swrem_whole_o2_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=20, suff="_20bins")
    
    # case_name = r"politics_lim_ns_random_swrem_whole_o2_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=5, suff="_5bins") 
    
    # case_name = r"politics_lim_ns_random_swrem_whole_o3_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=20, suff="_20bins")
    
    # case_name = r"politics_lim_ns_random_swrem_whole_o3_logas"
    # print("\nprocess", case_name)
    # make_perc_bins(case_name, nr_bins=5, suff="_5bins") 

def check_random_landscape():
    gn1 = r"D:\Users\Lydia\results puzzle\politics_limit1000_no_stem_swrem\grid_final.txt"
    gn2 = r"D:\Users\Lydia\results puzzle\politics_limit1000_no_stem_RANDOM_swrem\grid_final.txt"
    print("g1")
    g1 = grid_from_file_list(gn1)
    print("g2")
    g2 = grid_from_file_list(gn2)
    
    print("\n",gn1, "\n", gn2,"\n")
    
    cg1 = 0
    cg2 = 0
    for w in g1:
        if not w in g2:
            # print(w, "in g1 and not in g2")
            cg1+=1
    print("\n")
    for w in g2:
        if not w in g1:
            cg2+=1
            # print(w, "in g2 and not in g1")
    print(cg1, cg2)
    
if __name__ == "__main__":
    print("start", datetime.datetime.now())

    file_name = r"D:\Users\Lydia\results_freqs\nn_data\politics_names_allDocs_o0_hub2\data.txt"
    print(file_name)
    count_lines_file(file_name)    
    print("\n")
       
    # check_word_freq("snelkookpannen") 
    
    # case_name = "politics_nolog_freqs"
    # fromdate = datetime.date(2013,1,1)
    # todate = datetime.date(2014,1,1)
    # distribution_values_normalized_by_max_freqs(case_name, fromdate, todate)



    # filename= "D:\\Users\\Lydia\\results_freqs\\nn_data\\politics_lim_ns_o2_logas_hub_tarind10\\data.txt"
    # inputs= 180
    # outputs = 6
    # check_lengths(filename, inputs, outputs)
    
    # file = r"D:\Users\Lydia\results word cooc\politics_names_allDocs\wordlist.txt"
    # destination = r"D:\Users\Lydia\results puzzle\politics_names_allDocs_RANDOM_temp"
    # words = get_word_list(file)
    # build_random_grid(words, destination)
    # destination2 = r"D:\Users\Lydia\results puzzle\politics_names_allDocs_RANDOM"
    # build_random_puzzle_result(destination+r"\grid_final.txt", destination2)
 
 
    # replace_silly_words_sequal("politics_limit1000_no_stem", 90, "sillywords_sequal.txt")
    # check_max_vals()
    
    # run_perc_bins_all_case_names()
    # run_distr_max_all_case_names()
    
    # case_name = "test_freqs"
    # make_perc_bins(case_name, nr_bins=5, suff="_5bins")
    
    # for i in range(1876):
        # x = count_elems_on_first_line(r"D:\Users\Lydia\results_freqs\nn_data\politics_lim_ns_swrem_whole_o2_logas\whole\input\sample_in"+four_digit_string(i)+".txt",",", print_info = False)
        # y = count_elems_on_first_line(r"D:\Users\Lydia\results_freqs\nn_data\politics_lim_ns_swrem_whole_o2_logas\whole\output\sample_out"+four_digit_string(i)+".txt",",", print_info = False)
        # if x != 44180 or y != 8100:
            # print("not right nr of elems:", x, y)
    
    # print_n_lines_file(r"D:\Users\Lydia\results_freqs\nn_data\politics_lim_ns_swrem_whole_o0_logas_5bins_tz_simpleSamples\simple_data.txt", 10)   
    # count_elems_on_first_line(r"D:\Users\Lydia\results_freqs\nn_data\politics_lim_ns_swrem_whole_o0_logas_5bins_tz_simpleSamples\simple_data.txt", ";", doubleSplit = True, sec_sep = ",")

    # print("\n\ndistribution docs politics")
    # distribution_daily_docs("politics_merged")
    # print("distribution docs football")
    # distribution_daily_docs("football_all")

    # data_cases = ["football_limit1000_no_stem","football_limit1000_stem","politics_limit1000_no_stem","politics_limit1000_stem"]
    # output_naes = ["football_limit1000_no_stem","football_limit1000_stem","politics_limit1000_no_stem","politics_limit1000_stem"]
    # data_cases = ["politics_big_stem"]
    # output_names = ["politics_big_stem_random"]
    
    # for i in range(len(data_cases)):
        # data_case = data_cases[i]
        # output_name = output_names[i]
        # landscape = r"D:\Users\Lydia\results puzzle"+"\\"+data_case+r"\grid_initial.txt"
        # destination = r"D:\Users\Lydia\results puzzle"+"\\"+output_name
        # build_random_puzzle_result(landscape, destination)
        
    # print("==============\nDONE\n==============")
    
    
    # stat_file = r"D:\Users\Lydia\results word cooc\football_limit1000_no_stem"
    # print(get_nr_words_from_stats(stat_file))
    
    