import argparse
import datetime
import copy
import os
import sys
import thesis_utilities
import numpy as np
import copy
import random

patch_days = [30,7,3,2,1]

class Settings:
    
    def __init__(self, case_name, sample_type, overlap, bin_suffix, add_time_info, add_input_bin, input_bin_suffix, dif_output_name, random_config, landscape_file):
        input_template1 = r"D:\Users\Lydia\results_freqs"
        input_template2 = r"\daily_freqs"
        output_template = r"D:\Users\Lydia\results_freqs\nn_data"
        
        self.case_name = case_name
        self.sample_type = sample_type
        self.overlap = overlap
        self.bin_suffix = bin_suffix
        self.add_time_info = add_time_info
        self.add_input_bin = add_input_bin
        self.input_bin_suffix = input_bin_suffix
        self.input_folder = input_template1+"\\"+ case_name+ input_template2
                
        if dif_output_name!="":
            self.output_folder = output_template+"\\"+dif_output_name
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)	
        output_file_name = self.output_folder+"\\data.txt"
        self.output_file = open(output_file_name,"w")
        
        
        self.random_config=random_config
        self.landscape = None
        if random_config:
            self.add_landscape(landscape_file)
                
        self.settings_to_file()

    def settings_to_file(self):
        f = open(self.output_folder+"\\param_info.txt","w")
        f.write("case name "+str(self.case_name)+"\n")
        f.write("sample type "+str(self.sample_type)+"\n")
        f.write("overlap "+str(self.overlap)+"\n")
        f.write("bin suffix "+str(self.bin_suffix)+"\n")
        f.write("add time info "+str(self.add_time_info)+"\n")
        f.write("add input bin "+str(self.add_input_bin)+"\n")
        f.write("input bin suffix "+str(self.input_bin_suffix)+"\n")
        f.write("input folder "+str(self.input_folder)+"\n")
        f.write("output_folder "+str(self.output_folder)+"\n")
        f.write("random_config "+str(self.random_config)+"\n")
        f.close()
        
    def add_landscape(self, landscape_file):
        # Read in landscape
        full_path = r"D:\Users\Lydia\results puzzle" + "\\" + landscape_file + r"\grid_final.txt"
        self.landscape = thesis_utilities.grid_from_file_list(full_path)

    def get_word(self, i):
        if self.landscape == None:
            print("Trying to get word index from non loaded landscape")
        else:
            return self.landscape[i]
    
    def get_word_index(self, w):
        if self.landscape == None:
            print("Trying to get word index from non loaded landscape")
        else:
            return self.landscape.index(w)
        
    def to_output_file(self, s):
        self.output_file.write(s)
        
    def close_output_file(self):
        self.output_file.close()

def get_bins(file_name):
    f = open(file_name)
    bins = []
    for line in f:
        line = line.split(" ")
        bins.append(float(line[0]))
    bins.append(float(line[1]))    
    f.close()
    return bins
    
# def get_sample(f_in):
    # if sample_type == "simple_samples" or sample_type== "simple_samples_large":
        # return get_sample_simple(f_in)
    # elif sample_type=="freq_bins_classes" or sample_type=="freq_bins_classes_hub":
        # return get_sample_complex(f_in)
    # else:
        # print("sample type not found in get_sample")
        # sys.exit()
    
def get_sample_complex(f_in):
    all_elems = []
    splitter = ","
    first = True
    # count = 0
    for line in f_in:
        if first and ";" in line:
            splitter = ";"
            first = False
        line = line.split(splitter)
        elems = list(map(float, line))
        all_elems.append(elems)
        # print(count, len(all_elems), len(elems), elems[0])
        # count+=1
    result = np.array(all_elems)
    return result
    
        
def get_output_perc_bins(value, bins):
    output = list(np.zeros(len(bins)))
    if value == 0.0:
        output[0]=1
        return output, 0
    else:
        for i in range(len(bins)-1):
            # print(i)
            if value >= bins[i] and value < bins[i+1]:
                output[i+1]=1
                return (output, i+1)
    print("SOMETHING WENT WRONG IN GETTING BIN OUTPUT", value, "\n", bins)
    sys.exit()
    
def get_output_perc_bins_hub(value, bins):
    output = list(np.zeros(len(bins)))
    if value == 0.0:
        output[0]=1
        output[1]=0.5
        return output, 0
    else:
        for i in range(len(bins)-1):
            # print(i)
            if value >= bins[i] and value < bins[i+1]:
                output[i+1]=1
                output[i] = 0.5
                output[min(i+2,len(bins)-2)] = 0.5
                return (output, i+1)
    print("SOMETHING WENT WRONG IN GETTING BIN OUTPUT", value, "\n", bins)
    sys.exit()

def get_output_only_class(value, bins):
    if value == 0.0:
        return 0
    for i in range(len(bins)-1):
        # print(i)
        if value >= bins[i] and value < bins[i+1]:            
            return i+1
    print("SOMETHING WENT WRONG IN GETTING BIN OUTPUT", value, "\n", bins)
    sys.exit()

def get_all_samples_window(samples, print_length, target_date, cur_set):
    all_samples = []
    binfile_name = r"D:\Users\Lydia\results_freqs"+"\\"+cur_set.case_name+r"\info_whole_landscape\binvalues_perc"+cur_set.bin_suffix+".txt"
    bins = get_bins(binfile_name)
    if cur_set.add_input_bin:
        binfile_name = r"D:\Users\Lydia\results_freqs"+"\\"+cur_set.case_name+r"\info_whole_landscape\binvalues_perc"+cur_set.input_bin_suffix+".txt"
        input_bins = get_bins(binfile_name)
    landscape_size = samples[0].shape[0]
    overlap = cur_set.overlap
    for i in range(overlap, landscape_size-overlap):
        for j in range(overlap, landscape_size-overlap):
            input = []
            nr_days = len(samples)
            input_consistency = []
            for d in range(nr_days-1):
                day = samples[d][i-overlap:i+overlap+1,j-overlap:j+overlap+1]
                input.extend(list(day.flatten()))
                input_consistency.append(("values", len(list(day.flatten()))))
                if cur_set.add_input_bin:
                    input_value = day[overlap,overlap]
                    input_bin, inp_bin_nr=get_output_perc_bins(input_value ,input_bins)
                    input.extend(input_bin)
                    input_consistency.append(("target coding", len(input_bin)))
                    
            if cur_set.add_time_info == "weekday_month":
                time_inf = list(np.zeros(12+7))
                time_inf[target_date.month]=1.0
                time_inf[target_date.weekday()+12]=1.0
                input.extend(time_inf)
                input_consistency.append(("time inf", len(time_inf)))
            elif cur_set.add_time_info == "weekday":
                time_inf = list(np.zeros(7))
                time_inf[target_date.weekday()]=1.0
                input.extend(time_inf)
                input_consistency.append(("time inf", len(time_inf)))
            
            if cur_set.sample_type == "freq_bins_classes":     
                value = samples[-1][i,j]
                output, bin_nr=get_output_perc_bins(value ,bins)
                all_samples.append([input,output,[value, bin_nr]])
            elif cur_set.sample_type == "freq_bins_classes_hub":     
                value = samples[-1][i,j]
                output, bin_nr=get_output_perc_bins_hub(value ,bins)
                all_samples.append([input,output,[value, bin_nr]])
            elif cur_set.sample_type == "only_class":     
                value = samples[-1][i,j]
                output=get_output_only_class(value ,bins)
                all_samples.append([input,[output],[value]])
            else:
                print("sample type not implemented get all samples window")
                sys.exit() 
    if print_length:
        print("nr samples per batch", len(all_samples))
        print("nr inputs", len(all_samples[0][0]))
        print("nr outputs", len(all_samples[0][1]))
        if cur_set.add_input_bin:
             print("len additional input target encoding: ", len(input_bin))
        print("input consistency")
        for x in input_consistency:
            print(x)
    return all_samples
        

# def not_all_zeros(sample):
    # return not(all([x==0.0 for x in sample[0]]) and sample[1][0]==0.0)

def not_final_target_zero(sample, sample_type=None):
    if sample_type=="only_class":
        return sample[1][0]!=0
    else:
        return sample[1][0] == 0
    
    
def check_lengths(all_samples):
    for i in range(1,len(all_samples)):
        if len(all_samples[i])!= len(all_samples[0]):
            print("something wrong with lengths")
            for x in all_samples:
                print(len(x))
            sys.exit()

def write_samples_to_file(sample_nr, all_samples, all_settings, include_z):
    # nr_naz_samples += counts[0]
    # nr_az_samples += counts[1]
    # nr_included_az_samples += counts[2]
    # nr_samples+=counts[3]
    counts=[0,0,0,0,0]
    ntz = not_final_target_zero(all_samples[0][sample_nr], all_settings[0].sample_type)
    if not ntz:
        counts[1]=1
        if include_z:
            counts[2]=1
            counts[3]=1
    else:
        counts[0]=1
        counts[3]=1
    word = all_settings[0].get_word(sample_nr)
    if word == None:
        counts[4]=1
            
    if (ntz or include_z) and word!=None:
        for setting_nr in range(len(all_settings)):
            s = all_settings[setting_nr]
            if s.random_config:
                sample = all_samples[setting_nr][s.get_word_index(word)]
            else:
                sample = all_samples[setting_nr][sample_nr]
                
            for info_type in range(len(sample)):
                for elem_nr in range(len(sample[info_type])):
                    s.to_output_file(str(sample[info_type][elem_nr]))
                    if elem_nr < len(sample[info_type])-1:
                        s.to_output_file(",")
                if info_type < len(sample)-1:
                    if s.sample_type == "only_class":                   
                        s.to_output_file(",")
                    else:
                        s.to_output_file(";")
            s.to_output_file("\n")
            
    return counts
            
def rewrite(min_date, max_date, max_samples, zeros_portion, all_settings):
    
    nr_exceptions = 0 
    first = True
    nr_samples = 0
    nr_encountered_samples = 0
    nr_naz_samples = 0
    nr_az_samples = 0
    nr_included_az_samples = 0
    nr_nones=0
    current_month = -1    
    date = copy.copy(min_date) 
    continue_while = True
    print_length_bool=True
    
    while continue_while:
        good = True        
        
        all_samples = []
        for setting in all_settings:
            samples = []            
            if good:
                for pd in patch_days:                  
                    current_date = date-datetime.timedelta(pd)
                    try:
                        f_name= setting.input_folder+"\\day"+str(current_date)+".txt"
                        if first:
                            print("file name",f_name)
                            first = False
                        f_in = open(f_name,"r")
                    except IOError:
                        nr_exceptions+=1
                        good = False  
                        break                    
                    if good:
                        samples.append(get_sample_complex(f_in))                   
                        f_in.close()
                    else:
                        break
            if good:
                try:
                    f_name = setting.input_folder+"\\day"+str(date)+".txt"                    
                    f_in = open(f_name)
                except IOError:
                    nr_exceptions+=1
                    good = False                       
            if good: 
                samples.append(get_sample_complex(f_in))
                f_in.close()
                if print_length_bool:
                    print("\n===============\nprint length")                
                # all_samples = get_all_samples_window(samples, print_length, target_date, cur_set)
                extracted_samples = get_all_samples_window(samples, print_length_bool, date, setting)            
                if print_length_bool:
                    print("===============\n")
                print_length_bool=False
                # print("nr extracted samples", len(extracted_samples))
                all_samples.append(extracted_samples)
        
        if date.month!=current_month:
            print("current:", date, "now", datetime.datetime.now())
            current_month = date.month
            if nr_samples !=0:
                portion = nr_included_az_samples/nr_samples
            else:
                portion = "na"
            print("nr samples", nr_samples,"nr encountered samples", nr_encountered_samples, "zeros_portion", portion)
            print("nr not all zero samples", nr_naz_samples,"nr all zero samples", nr_az_samples, "\nnr included all zero samples", nr_included_az_samples, "nr nones", nr_nones, "\n")

        
        
        if good:
            check_lengths(all_samples)
            for sample_nr in range(len(all_samples[0])):
                if max_samples==None or max_samples>nr_samples:  
                    r = random.uniform(0, 1)                
                    counts = write_samples_to_file(sample_nr, all_samples, all_settings, r<zeros_portion)
                    
                    nr_encountered_samples += 1
                    nr_naz_samples += counts[0]
                    nr_az_samples += counts[1]
                    nr_included_az_samples += counts[2]
                    nr_samples+=counts[3] 
                    nr_nones+=counts[4]
        date += datetime.timedelta(1)  
        continue_while=(date <= max_date) and (max_samples==None or max_samples>nr_samples)
    
    # close output files
    for s in all_settings:
        s.close_output_file()
    
    print("date", date, "max_date", max_date)
    
    print("nr samples", nr_samples,"nr exceptions", nr_exceptions, "nr encountered samples", nr_encountered_samples)
    print("nr not all zero samples", nr_naz_samples,"nr all zero samples", nr_az_samples, "\nnr included all zero samples", nr_included_az_samples)
    print("portion zeros = ", nr_included_az_samples/nr_samples)

def run_politics_words_svm():
    sample_types = ["freq_bins_classes", "freq_bins_classes_hub", "only_class"]
    time_indics = ["weekday", "weekday_month"]
    beg_d = 1
    beg_m = 5
    beg_y = 2010
    end_d = 5
    end_m = 7
    end_y = 2014
    # max_samples = 1000
    max_samples = 500000
    zeros_portion = 0.05
    min_date = datetime.date(beg_y, beg_m, beg_d)
    max_date = datetime.date(end_y,end_m, end_d)
        
    all_settings = []
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o2_logas", sample_types[2], 2, "_5bins", False, False, None, "svm_politics_lim_ns_o2_logas_more", False, None  ))
    all_settings[0].add_landscape("politics_limit1000_no_stem_swrem")
    all_settings.append(Settings("politics_lim_ns_random_swrem_o2_logas", sample_types[2], 2, "_5bins", False, False, None, "svm_politics_lim_ns_random_o2_logas_more", True, "politics_limit1000_no_stem_RANDOM_swrem"  ))    
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o0_logas", sample_types[2], 0, "_5bins", False, False, None, "svm_politics_lim_ns_o0_logas_more", False, None  ))
    rewrite(min_date, max_date, max_samples, zeros_portion, all_settings)


def run_politics_words():
    sample_types = ["freq_bins_classes", "freq_bins_classes_hub", "only_class"]
    time_indics = ["weekday", "weekday_month"]
    beg_d = 1
    beg_m = 5
    beg_y = 2008
    end_d = 5
    end_m = 7
    end_y = 2014
    # max_samples = 1000
    max_samples = 1500000
    zeros_portion = 0.05
    min_date = datetime.date(beg_y, beg_m, beg_d)
    max_date = datetime.date(end_y,end_m, end_d)
        
    all_settings = []
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o2_logas", sample_types[1], 2, "_5bins", False, False, None, "politics_lim_ns_o2_logas_hub", False, None  ))
    all_settings[0].add_landscape("politics_limit1000_no_stem_swrem")
    all_settings.append(Settings("politics_lim_ns_random_swrem_o2_logas", sample_types[1], 2, "_5bins", False, False, None, "politics_lim_ns_random_o2_logas_hub", True, "politics_limit1000_no_stem_RANDOM_swrem"  ))    
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o2_logas", sample_types[0], 2, "_5bins", False, False, None, "politics_lim_ns_o2_logas_no_hub", False, None  ))
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o0_logas", sample_types[1], 0, "_5bins", False, False, None, "politics_lim_ns_o0_logas_hub", False, None  ))
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o3_logas", sample_types[1], 3, "_5bins", False, False, None, "politics_lim_ns_o3_logas_hub", False, None  ))
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o2_logas", sample_types[1], 2, "_5bins", time_indics[1], False, None, "politics_lim_ns_o2_logas_hub_timeind", False, None  ))
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o2_logas", sample_types[1], 2, "_5bins", False, True, "_5bins", "politics_lim_ns_o2_logas_hub_tarind5", False, None  ))
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o2_logas", sample_types[1], 2, "_5bins", False, True, "_10bins", "politics_lim_ns_o2_logas_hub_tarind10", False, None  ))
    all_settings.append(Settings("politics_lim_ns_swrem_whole_o2_logas", sample_types[1], 2, "_5bins", time_indics[1], True, "_5bins", "politics_lim_ns_o2_logas_hub_timeind_tarind5", False, None  ))
    rewrite(min_date, max_date, max_samples, zeros_portion, all_settings)

def run_politics_names_svm():
    sample_types = ["freq_bins_classes", "freq_bins_classes_hub", "only_class"]
    time_indics = ["weekday", "weekday_month"]
    beg_d = 1
    beg_m = 1
    beg_y = 2008
    end_d = 5
    end_m = 7
    end_y = 2014
    # max_samples = 1000
    max_samples = 10000
    zeros_portion = 0.01
    min_date = datetime.date(beg_y, beg_m, beg_d)
    max_date = datetime.date(end_y,end_m, end_d)
        
    all_settings = []
    all_settings.append(Settings("politics_names_allDocs_o2", sample_types[2], 2, "_5bins", False, False, None, "svm_politics_names_allDocs_o2_hub", False, None  ))
    all_settings[0].add_landscape("politics_names_allDocs")
    all_settings.append(Settings("politics_names_allDocs_o2_random", sample_types[2], 2, "_5bins", False, False, None, "svm_politics_names_allDocs_o2_hub_random", True, "politics_names_allDocs_RANDOM"  ))    
    all_settings.append(Settings("politics_names_allDocs_o0", sample_types[2], 0, "_5bins", False, False, None, "svm_politics_names_allDocs_o0_hub", False, None  ))
    rewrite(min_date, max_date, max_samples, zeros_portion, all_settings)
    
    
def run_politics_names():
    sample_types = ["freq_bins_classes", "freq_bins_classes_hub", "only_class"]
    time_indics = ["weekday", "weekday_month"]
    beg_d = 1
    beg_m = 1
    beg_y = 2008
    end_d = 5
    end_m = 7
    end_y = 2014
    # max_samples = 1000
    max_samples = 100000
    zeros_portion = 0.01
    min_date = datetime.date(beg_y, beg_m, beg_d)
    max_date = datetime.date(end_y,end_m, end_d)
        
    all_settings = []
    all_settings.append(Settings("politics_names_allDocs_o2", sample_types[1], 2, "_5bins", False, False, None, "politics_names_allDocs_o2_hub2", False, None  ))
    all_settings[0].add_landscape("politics_names_allDocs")
    all_settings.append(Settings("politics_names_allDocs_o2_random", sample_types[1], 2, "_5bins", False, False, None, "politics_names_allDocs_o2_hub_random2", True, "politics_names_allDocs_RANDOM"  ))    
    all_settings.append(Settings("politics_names_allDocs_o0", sample_types[1], 0, "_5bins", False, False, None, "politics_names_allDocs_o0_hub2", False, None  ))
    rewrite(min_date, max_date, max_samples, zeros_portion, all_settings)
    
    
if __name__ == "__main__":

    # run_politics_words()

    run_politics_names()
    
    # run_politics_words_svm()
    
    run_politics_names_svm()
    
    
    
	
    