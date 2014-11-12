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

sample_type = ""
overlap = None
case_name = ""
bin_suffix = ""
zeros_portion = None
add_time_info = None
add_input_bin = False
input_bin_suffix = None

def get_bins(file_name):
    f = open(file_name)
    bins = []
    for line in f:
        line = line.split(" ")
        bins.append(float(line[0]))
    bins.append(float(line[1]))    
    f.close()
    return bins
    
def get_sample(f_in):
    if sample_type == "simple_samples" or sample_type== "simple_samples_large":
        return get_sample_simple(f_in)
    elif sample_type=="freq_bins_classes" or sample_type=="freq_bins_classes_hub":
        return get_sample_complex(f_in)
    else:
        print("sample type not found in get_sample")
        sys.exit()
    
def get_sample_simple(f_in):
    all_elems = []
    splitter = ","
    first = True
    for line in f_in:
        if first and ";" in line:
            splitter = ";"
            first = False
        line = line.split(splitter)
        elems = map(float, line)
        all_elems.extend(elems)
    return all_elems
    
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
    
def get_all_samples(samples, nr_samples, max_dif_eq=0.02, print_length=False, target_date = None):

    if sample_type == "simple_samples":
        return get_all_samples_simple(samples, nr_samples, print_length)
    elif sample_type=="simple_samples_large":
        return get_all_samples_large(samples, nr_samples,max_dif_eq, print_length)
    elif sample_type=="freq_bins_classes" or sample_type=="freq_bins_classes_hub":
        return get_all_samples_window(samples, print_length, target_date)
        
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
    


def get_all_samples_window(samples, print_length, target_date):

    # add_input_bin = False
# input_bin_suffix = None

    # print("overlap", overlap)
    all_samples = []
    if sample_type == "freq_bins_classes" or sample_type == "freq_bins_classes_hub":   
        binfile_name = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\info_whole_landscape\binvalues_perc"+bin_suffix+".txt"
        bins = get_bins(binfile_name)
    if add_input_bin:
        binfile_name = r"D:\Users\Lydia\results_freqs"+"\\"+case_name+r"\info_whole_landscape\binvalues_perc"+input_bin_suffix+".txt"
        input_bins = get_bins(binfile_name)
    landscape_size = samples[0].shape[0]
    for i in range(overlap, landscape_size-overlap):
        for j in range(overlap, landscape_size-overlap):
            input = []
            nr_days = len(samples)
            input_consistency = []
            for d in range(nr_days-1):
                day = samples[d][i-overlap:i+overlap+1,j-overlap:j+overlap+1]
                input.extend(list(day.flatten()))
                input_consistency.append(("values", len(list(day.flatten()))))
                if add_input_bin:
                    input_value = day[overlap,overlap]
                    input_bin, inp_bin_nr=get_output_perc_bins(input_value ,input_bins)
                    input.extend(input_bin)
                    input_consistency.append(("target coding", len(input_bin)))
                    
            if add_time_info == "weekday_month":
                time_inf = list(np.zeros(12+7))
                time_inf[target_date.month]=1.0
                time_inf[target_date.weekday()+12]=1.0
                input.extend(time_inf)
                input_consistency.append(("time inf", len(time_inftime_inf)))
            elif add_time_info == "weekday":
                time_inf = list(np.zeros(7))
                time_inf[target_date.weekday()]=1.0
                input.extend(time_inf)
                input_consistency.append(("time inf", len(time_inftime_inf)))
            
            if sample_type == "freq_bins_classes":     
                value = samples[-1][i,j]
                output, bin_nr=get_output_perc_bins(value ,bins)
                all_samples.append([input,output,[value, bin_nr]])
            elif sample_type == "freq_bins_classes_hub":     
                value = samples[-1][i,j]
                output, bin_nr=get_output_perc_bins_hub(value ,bins)
                all_samples.append([input,output,[value, bin_nr]])
            else:
                print("sample type not implemented get all samples window")
                sys.exit() 
    if print_length:
        print("nr samples per batch", len(all_samples))
        print("nr inputs", len(all_samples[0][0]))
        print("nr outputs", len(all_samples[0][1]))
        if add_input_bin:
             print("len additional input target encoding: ", len(input_bin))
        print("input consistency")
        for x in input_consistency:
            print(x)
    return all_samples
        
def get_all_samples_simple(samples, nr_samples, print_length=False):
    all_samples = []
    for i in range(len(samples[0])):
        sample_input = []
        for j in range(len(samples)-1):
            sample_input.append(samples[j][i])        
        all_samples.append([sample_input, [samples[-1][i]]])
        
    if print_length:
        print("nr samples",len(all_samples))
        print("sample example",all_samples[0])
        
    return all_samples
    
def get_all_samples_large(samples, nr_samples, max_dif_eq, print_length=False):
    all_samples = []
    for i in range(len(samples[0])):
        sample_input = []
        
        sample_output = []
        for j in range(len(samples)-1):
            sample_input.append(samples[j][i])       
            if sample_input[j]>samples[-1][i]+max_dif_eq:
                sample_output.extend([0,0,1])
            elif sample_input[j]<samples[-1][i]-max_dif_eq:
                sample_output.extend([1,0,0])
            else:
                sample_output.extend([0,1,0])                                
        
        day_five =  sample_input[len(patch_days)-1]
        target = samples[-1][i] 
        if day_five < target - max_dif_eq:
            sample_value = ["up"]
        elif day_five > target+max_dif_eq:
            sample_value = ["down"]
        else:
            sample_value = ["equal"]
            
        sample_value.append(samples[-1][i])
        
        all_samples.append([sample_input, sample_output, sample_value])
        # if nr_samples == 0 and i < 10:
            # print(samples[0][i], samples[1][i], samples[2][i], samples[3][i], samples[4][i], samples[5][i])                
        
    if print_length:
        length = 0
        prev_length = len(all_samples[0][0])
        for sample in all_samples:
            length = len(sample[0])
            if length != prev_length:
                print("FALSE LENGTH", length, prev_length)
            prev_length = length
        print("length", length)
        print("nr days in samples", len(samples))
        print("length input", len(sample_input))
        print("length output", len(sample_output))
        print("length value", len(sample_value))
        
        
        
    return all_samples

def not_all_zeros(sample):
    return not(all([x==0.0 for x in sample[0]]) and sample[1][0]==0.0)

def not_final_target_zero(sample):
    return sample[1][0] == 0
    
def not_all_target_values_zero(sample):
    all_zero = True
    row_size = 2*overlap + 1
    for i in range(len(patch_days)):       
        if sample[0][i*row_size*row_size + (overlap*row_size+overlap)] != 0.0:
            all_zero = False
            break
    
    if sample[1][0]!=1:
        all_zero = False
    
    # if all_zero:
        # item = 0
        # for i in range(len(patch_days)):
            # for j in range(row_size): 
                # for k in range(row_size):
                    # print(sample[0][item], end=" ")
                    # item+=1
                # print("|")
            # print("|")        
        # for k in sample[1]:
            # print(k, end=" ")
        # print("\n=========")
                
    return all_zero
    
def rewrite_from_whole_landscape(min_date, max_date, input_folder, output_file, max_samples, include_zeros):
    print("")
    input_folder_patch = input_folder+r"\patches"
    nr_exceptions = 0    
   
    f_data_link = open(output_folder + "\\data_nr_info.txt","w")
    f_out = open(output_folder+"\\simple_data.txt","w")
    print_nr_link = True
    first = True
    first_final = True
    
    nr_samples = 0
    nr_encountered_samples = 0
    nr_naz_samples = 0
    nr_az_samples = 0
    nr_included_az_samples = 0
    current_year = 0
    
    date = copy.copy(min_date) 
    continue_while = True
    print_length_bool=True
    while continue_while:
        samples = []
        good = True        
        if date.year!=current_year:
            print("year",date.year, datetime.datetime.now())
            current_year = date.year
            print("nr samples", nr_samples,"nr encountered samples", nr_encountered_samples)
            print("nr not all zero samples", nr_naz_samples,"nr all zero samples", nr_az_samples, "\nnr included all zero samples", nr_included_az_samples, "\n")
    
        for pd in patch_days:                  
            current_date = date-datetime.timedelta(pd)
            try:
                f_name= input_folder+"\\day"+str(current_date)+".txt"
                if first:
                    print("file name",f_name)
                    first = False
                f_in = open(f_name,"r")
            except IOError:
                nr_exceptions+=1
                good = False  
                break                    
            if good:
                samples.append(get_sample(f_in))                   
                f_in.close()
            else:
                break
        if good:
            try:
                f_name = input_folder+"\\day"+str(date)+".txt"
                if first_final:
                    print("first_final good file",f_name)
                    first_final=False
                f_in = open(f_name)
            except IOError:
                nr_exceptions+=1
                good = False                       
        if good: 
            samples.append(get_sample(f_in))
            f_in.close()
            if print_length_bool:
                print("\n===============\nprint length")                
            all_samples = get_all_samples(samples, nr_samples, print_length=print_length_bool, target_date=date)            
            if print_length_bool:
                print("===============\n")
            print_length_bool=False
            sample_index=0
            # print("nr samps", len(all_samples))
            for sample in all_samples:
                
                # naz = not_all_target_values_zero(sample)
                naz = not_final_target_zero(sample)
                
                bool1 = include_zeros!="no"  or naz
                bool2 = max_samples==None or max_samples>nr_samples
                r = random.uniform(0, 1)
                bool3 = include_zeros != "part" or (naz or r < zeros_portion)
                
                nr_encountered_samples +=1
                if naz:
                    nr_naz_samples += 1
                else:
                    nr_az_samples += 1
                    # if nr_az_samples == 5:
                        # sys.exit()
                    if r < zeros_portion:
                        nr_included_az_samples += 1
                        if not bool3:
                            print("something wrong here")
                        # print("RRRRRRR", r)
                    # else:
                        # print("r", r)
                        
                # if not bool3:
                    # print(include_zeros, not not_all_zeros(sample), zeros_portion, r)
                # bullshizzle_check = len(sample[0])!=14
                # if not bullshizzle_check:
                    # print("blaat gevonden", nr_samples)
                # if bool1 and bool2 and bool3 and bullshizzle_check:
                if bool1 and bool2 and bool3:
                    if print_nr_link:
                        f_data_link.write(str(nr_samples)+";"+str(date)+";"+str(sample_index)+"\n")
                    sample_index+=1
                    
                    for info_type in range(len(sample)):
                        for elem_nr in range(len(sample[info_type])):
                            f_out.write(str(sample[info_type][elem_nr]))
                            if elem_nr < len(sample[info_type])-1:
                                f_out.write(",")
                        if info_type < len(sample)-1:
                            f_out.write(";")
                    f_out.write("\n")
                    nr_samples+=1
                    if nr_samples % 100000==0 and (sample_type == "simple_samples" or sample_type== "simple_samples_large"):
                        print("samples",nr_samples)
        date += datetime.timedelta(1)  
        continue_while=(date <= max_date) and (max_samples==None or max_samples>nr_samples)
        
    f_data_link.close()
    f_out.close()
    
    print("date", date, "max_date", max_date)
    
    print("nr samples", nr_samples,"nr exceptions", nr_exceptions, "nr encountered samples", nr_encountered_samples)
    print("nr not all zero samples", nr_naz_samples,"nr all zero samples", nr_az_samples, "\nnr included all zero samples", nr_included_az_samples)
    
def rewrite_patches(min_date, max_date, input_folder, output_folder,max_samples, nr_patches, include_zeros): 
    print("max_date",max_date)
    input_folder_patch = input_folder+r"\patches"
    nr_exceptions = 0
     
    
    f_data_link = open(output_folder + "\\data_nr_info.txt","w")
    f_out = open(output_folder+"\\simple_data.txt","w")
    print_nr_link = True
    first = True
    max_samples_not_reached = True
    for p1 in range(nr_patches):
        for p2 in range(nr_patches):
            nr_samples = 0
            date = copy.copy(min_date)            
            print("patch", p1, p2)
            while date <= max_date and max_samples_not_reached:
                samples = []
                good = True
                
                for pd in patch_days:                  
                    current_date = date-datetime.timedelta(pd)
                    try:
                        f_name= input_folder_patch+"\\day"+str(current_date)+"\patch_"+str(p1)+"_"+str(p2)+".txt"
                        if first:
                            print("file name",f_name)
                            first=False
                        f_in = open(f_name,"r")
                    except IOError:
                        nr_exceptions+=1
                        good = False  
                        break                    
                    if good:
                        samples.append(get_sample(f_in))                   
                        f_in.close()
                if good:
                    try:
                        f_in = open(input_folder_patch+"\\day"+str(date)+"\patch_"+str(p1)+"_"+str(p2)+".txt")
                    except IOError:
                        nr_exceptions+=1
                        good = False                       
                if good: 
                    samples.append(get_sample(f_in))
                    f_in.close()
                    # VERWERK
                    all_samples = get_all_samples(samples, nr_samples)
                    sample_index=0
                    for sample in all_samples:
                        if max_samples_not_reached and (include_zeros=="yes" or not_all_zeros(sample)):
                            if print_nr_link:
                                f_data_link.write(str(nr_samples)+";"+str(date)+";"+str(sample_index)+"\n")
                            sample_index+=1
                            for info_type in range(len(sample)):
                                for elem_nr in range(len(sample[info_type])):
                                    f_out.write(str(sample[info_type][elem_nr]))
                                    if elem_nr < len(sample[info_type])-1:
                                        f_out.write(",")
                                if info_type < len(sample)-1:
                                    f_out.write(";")
                            f_out.write("\n")
                            nr_samples+=1
                        max_samples_not_reached = (max_samples == None) or (nr_samples < max_samples)
                date += datetime.timedelta(1)  
    f_out.close()
    f_data_link.close()
    
    print("date", date, "max_date", max_date)
    
    print("nr samples", nr_samples,"nr exceptions", nr_exceptions)
    
 
  
if __name__ == "__main__":
    print("\nstart", datetime.datetime.now())
    input_template1 = r"D:\Users\Lydia\results_freqs"
    input_template2 = r"\daily_freqs"
    output_template = r"D:\Users\Lydia\results_freqs\nn_data"
    
    parser = argparse.ArgumentParser(description='Run puzzle algorithm')
    # '''parser.add_argument(<naam>, type=<type>, default=<default>, help=<help message>)'''
    parser.add_argument("case_name", help="Name of the data case that you want to process")
    parser.add_argument("sample_type", help="options: simple_samples, simple_samples_large, freq_bins_classes, freq_bins_classes_hub")
    sample_type_options = ["simple_samples", "simple_samples_large", "freq_bins_classes", "freq_bins_classes_hub"]
    parser.add_argument("--beg_d", type=int, default = 1)
    parser.add_argument("--beg_m", type=int, default = 10)
    parser.add_argument("--beg_y", type=int, default = 2007)
    parser.add_argument("--end_d", type=int, default = 5)
    parser.add_argument("--end_m", type=int, default = 7)
    parser.add_argument("--end_y", type=int, default = 2014)
    parser.add_argument("--dif_output_name", default = "")
    parser.add_argument("--max_samples", type=int, default = None)
    parser.add_argument("--nr_patches", type=int, default = 5)
    parser.add_argument("--whole_landscape", default = None)
    parser.add_argument("--include_zeros", default = "yes")
    parser.add_argument("--overlap", type=int, default = None)
    parser.add_argument("--bin_suffix", default = None)
    parser.add_argument("--zeros_portion", type = float, default = None)
    parser.add_argument("--add_time_info", default = None, help="weekday_month, weekday")
    parser.add_argument("--add_input_bin", default = "no")
    parser.add_argument("--input_bin_suffix", default = None)  

    args = parser.parse_args()
    kwargs = vars(args)	
    
    min_date = datetime.date(kwargs["beg_y"], kwargs["beg_m"], kwargs["beg_d"])
    max_date = datetime.date(kwargs["end_y"], kwargs["end_m"], kwargs["end_d"])

    case_name = kwargs["case_name"]
    input_folder = input_template1+"\\"+ case_name+ input_template2
    zeros_portion = kwargs["zeros_portion"]
    overlap = kwargs["overlap"]
    
    sample_type = kwargs["sample_type"]
    if sample_type not in sample_type_options:
        print("invalid sample type")
        sys.exit()
    if (sample_type == "freq_bins_classes" or sample_type=="freq_bins_classes_hub") and overlap==None:
        print("for sampletype", sample_type, "you need to specify the overlap (>window_size) ")
        sys.exit()
    print("sample_type", sample_type)
    
    if kwargs["add_input_bin"]=="yes":
        add_input_bin = True
        if kwargs["input_bin_suffix"]==None:
            print("input bin suffix needs to be specified if you want to add a input bin")
            sys.exit()
    elif kwargs["add_input_bin"]!="no":
        print("invalid value add_input_bin")
        sys.exit()
    
    if kwargs["input_bin_suffix"]!=None:
        input_bin_suffix = kwargs["input_bin_suffix"]
    
    if kwargs["dif_output_name"]!="":
        output_folder = output_template+"\\"+kwargs["dif_output_name"]+"_simpleSamples"
    else:
        output_folder = output_template+"\\"+case_name+"_simpleSamples" 

    if kwargs["include_zeros"]!="no" and kwargs["include_zeros"]!="yes" and kwargs["include_zeros"]!="part":
        print("invalid value include_zeros")
        sys.exit()    
    if kwargs["include_zeros"]=="no" and not sample_type == "simple_samples":
        print("wrong combination of inputs include_only_non_zeros and use simple samples")
        sys.exit()
    if kwargs["include_zeros"]=="part" and kwargs["zeros_portion"] == None:
        print("You have to specify zeros_portion if you want to include part of the zeros")
        sys.exit()
      
    if kwargs["add_time_info"] != None:
        if not(kwargs["add_time_info"] == "weekday" or kwargs["add_time_info"] == "weekday_month"):
            print("wrong value add time info")
            sys.exit()
        add_time_info = kwargs["add_time_info"] 
      
    if kwargs["bin_suffix"] != None:
        bin_suffix = kwargs["bin_suffix"]
        
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    f = open(output_folder+"\\arguments_info.txt", "w")
    for key, elem in kwargs.items():
        f.write(str(key)+" " + str(elem)+"\n")
    f.close()
        
    if kwargs["whole_landscape"]=="yes":
        rewrite_from_whole_landscape(min_date, max_date, input_folder, output_folder,kwargs["max_samples"], kwargs["include_zeros"])
        # thesis_utilities.print_n_lines_file(output_folder+r"\simple_data.txt", 3)
    elif kwargs["whole_landscape"] == None or kwargs["whole_landscape"]=="no":    
        rewrite_patches(min_date, max_date, input_folder, output_folder,kwargs["max_samples"], kwargs["nr_patches"], kwargs["include_zeros"])
        thesis_utilities.print_n_lines_file(output_folder+r"\simple_data.txt", 3)
    else:
        print("invalid whole landscape argument")
	
    