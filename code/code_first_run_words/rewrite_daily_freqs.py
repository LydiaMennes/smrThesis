import datetime
import os
import copy
import argparse
import sys
import numpy as np

input_folder = r"D:\Users\Lydia\results_freqs"
output_folder  = r"D:\Users\Lydia\results_freqs\nn_data"
case_name = ""
resize_output = ""
reduction_size = 0
patches = None
nr_patches = None
sample_days = [30,7,3,2,1]
# sample_days = [14,7,3,2,1]
# sample_days = [5,4,3,2,1]
overlap = None
from thesis_utilities import *

strict = True
   

def to_line_reduce(f_in):
    data = []
    for line in f_in:
        line = line.replace("\n","")
        x = line.split(";")
        data.append([float(y) for y in x])
        
    line_str = ""
    data = np.array(data)
    row = 0
    column = 0
    resulting_size = [0,0]
    while row < data.shape[0]:
        while column < data.shape[1]:
            row_end = min(row+reduction_size, data.shape[0])
            column_end = min(column+reduction_size, data.shape[1])
            line_str += str( np.sum(  data[row:row_end, column:column_end]) ) + ";"
            column += reduction_size
            if row==0:
                resulting_size[1] += 1
        column = 0
        row += reduction_size
        resulting_size[0]+=1
    return line_str[0:-1], resulting_size

def to_line(f_in):
    line_str = ""
    for line in f_in:
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        if line[-1] != ",":
            line += ","
        line_str+=line
    return line_str  
    
def to_line_patch(f_in):
    line_str = ""
    for line in f_in:
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        if line[-1] != ",":
            line += ","
        line_str+=line
    if ";" in line_str:
        print("; in to line patch")
        sys.exit()
    return line_str  
    
def to_line_output_patch(f_in, patchrow, patchcolumn):
    if nr_patches == None:
        nr_patches_x = float("inf")
    else:
        nr_patches_x = nr_patches
    lines = []
    line_nr = 0
    lt = 0
    for line in f_in:        
        line = line.replace("\n", "")
        line = line.replace(" ", "")        
        if line[-1] == ",":
            line = line[:-1]
        temp = line.split(",")
        if (patchcolumn!=0 and overlap>0) or strict:
            temp = temp[overlap:]
        if (patchcolumn < nr_patches_x-1 and overlap>0) or strict:
            temp = temp[:-overlap]
        lt = len(temp)
        lines.append(",".join(temp))
        line_nr+=1
    if (patchrow != 0 and overlap>0) or strict:
        lines = lines[overlap:]
    if (patchrow < nr_patches_x-1 and overlap>0) or strict:
        lines = lines[:-overlap]
    # print("patch", patchrow, patchcolumn, "size", len(lines), lt)
    result = ",".join(lines)  
    if ";" in result:
        print("output patch contains ;")
        sys.exit()
    return result

def rewrite_patches(min_date, max_date, file_for_each_sample = False): 
    print("max_date",max_date)
    input_folder_patch = input_folder+r"\patches"
    nr_exceptions = 0
    if not os.path.exists(output_folder + r"\patches_"+case_name):
        os.makedirs(output_folder + r"\patches_"+case_name)
    f_data_link = open(output_folder + r"\patches_"+case_name+"\\data_nr_info.txt","w")
    print_nr_link = True
    print("link in", output_folder + r"\patches_"+case_name+"\\data_nr_info.txt")    
    
    for p1 in range(nr_patches):
        for p2 in range(nr_patches):
            nr_samples = 0
            date = copy.copy(min_date)
            
            print("patch", p1, p2)
            
            output_folder_patch = output_folder + r"\patches_"+case_name+"\\patch_"+str(p1)+"_"+str(p2)
            if not os.path.exists(output_folder_patch):
                os.makedirs(output_folder_patch)
            if file_for_each_sample:
                if not os.path.exists(output_folder_patch+"\\output"):
                    os.makedirs(output_folder_patch+"\\output")
                if not os.path.exists(output_folder_patch+"\\input"):
                    os.makedirs(output_folder_patch+"\\input")
            f_out = open(output_folder_patch+r"\data.txt", "w")
            
            while date <= max_date:
                
                good = True
                total_str = ""
                output_str = ""
                for pd in sample_days:                  
                    current_date = date-datetime.timedelta(pd)
                    try:
                        f_name= input_folder_patch+"\\day"+str(current_date)+"\patch_"+str(p1)+"_"+str(p2)+".txt"
                        f_in = open(f_name,"r")
                    except IOError:
                        nr_exceptions+=1
                        good = False  
                        break                    
                    if good:
                        total_str+=to_line_patch(f_in)                    
                        f_in.close()
                if good:
                    try:
                        f_in = open(input_folder_patch+"\\day"+str(date)+"\patch_"+str(p1)+"_"+str(p2)+".txt")
                    except IOError:
                        nr_exceptions+=1
                        good = False                       
                if good: 
                    output_str = to_line_output_patch(f_in, p1, p2)
                    f_in.close()
                    if total_str[-1] == ",":
                        total_str = total_str[:-1]
                    if output_str[-1] == ",":
                        output_str = output_str[:-1]
                    if not file_for_each_sample:
                        f_out.write(total_str+";"+output_str+"\n")    
                        if print_nr_link:
                            f_data_link.write(four_digit_string(nr_samples)+";"+str(date)+"\n")
                    else:
                        f_out_output = open(output_folder_patch+"\\output\sample_out"+four_digit_string(nr_samples)+".txt","w")
                        f_out_output.write(output_str)
                        f_out_output.close()
                        f_out_input = open(output_folder_patch+"\\input\sample_in"+four_digit_string(nr_samples)+".txt","w")
                        f_out_input.write(total_str)
                        f_out_input.close()
                        if print_nr_link:
                            f_data_link.write(four_digit_string(nr_samples)+";"+str(date)+"\n")
                    nr_samples+=1
                date += datetime.timedelta(1)
            f_out.close()
            print_nr_link =False
            f_data_link.close()
    
    print("date", date, "max_date", max_date)
    
    print("nr samples", nr_samples,"nr exceptions", nr_exceptions)
    f = open(output_folder + r"\patches_"+case_name+r"\info_"+case_name+".txt","w")
    f.write("nr samples = " + str(nr_samples) + "\n")
    f.write("number of days per sample = " + str(sample_days) + "\n")
    if resize_output:
        f.write("resizing with size = " + str(reduction_size) + "\n resulting size =" + str(res_size) + "\n")
    else:
        f.write("no resizing\n")
    f.close()
    
def rewrite(date, max_date, sample_per_file=False):
    nr_samples = 0
    nr_exceptions = 0
    delta = datetime.timedelta(1)
    
    if not sample_per_file:
        f_all = open(output_folder+"\\"+case_name+"\\"+case_name+".csv", "w")
    
    if sample_per_file:
        all_inputs_folder = output_folder+"\\"+case_name+r"\whole\input"
        all_outputs_folder = output_folder+"\\"+case_name+r"\whole\output"
        if not os.path.exists(all_inputs_folder):
            os.makedirs(all_inputs_folder)
        if not os.path.exists(all_outputs_folder):
            os.makedirs(all_outputs_folder)
    
    current_year = 0
    
    while date <= max_date:
        if date.year > current_year:
            current_year=date.year
            print("year", current_year)
        good = True
        in_str = ""
        out_str = ""
        for pd in sample_days:            
            try:
                f_in = open(input_folder+r"\day"+str(date-datetime.timedelta(pd))+".txt")
                in_str+= to_line(f_in)
            except IOError:
                nr_exceptions+=1
                good = False
                break   
            if good:
                f_in.close()
        if good:                    
            try:
                f_in = open(input_folder+r"\day"+str(date)+".txt")
                out_str+= to_line_output_patch(f_in, 2, 2)
            except IOError:
                nr_exceptions+=1
                good = False
        if good:
            f_in.close()   
            if in_str[-1]==",":
                in_str=in_str[:-1]
            if out_str[-1]==",":
                out_str=out_str[:-1]
            if sample_per_file:
                f = open(all_inputs_folder+r"\sample_in"+four_digit_string(nr_samples)+".txt", "w")
                f.write(in_str)
                f.close()
                f = open(all_outputs_folder+r"\sample_out"+four_digit_string(nr_samples)+".txt", "w")
                f.write(out_str)
                f.close()                
            else:
                f_all.write(in_str+";"+out_str+"\n")
            nr_samples+=1
                   
        date = date+delta
    
    print("date:", date, "max date", max_date)
    
    if not sample_per_file:
        f_all.close()
    
    
    print("nr samples", nr_samples,"nr exceptions", nr_exceptions)
    f = open(output_folder+"\\"+case_name+r"\info_"+case_name+".txt","w")
    f.write("nr samples = " + str(nr_samples) + "\n")
    if resize_output:
        f.write("resizing with size = " + str(reduction_size) + "\n resulting size =" + str(res_size) + "\n")
        f.write("NO LONGER SUPPORTED!!!!!!!!!!!!!")
    else:
        f.write("no resizing\n")
    f.close()
 
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Run puzzle algorithm')
    # '''parser.add_argument(<naam>, type=<type>, default=<default>, help=<help message>)'''
    parser.add_argument("case_name", help="Name of the data case that you want to process")
    parser.add_argument("patches", help="yes or no")    
    parser.add_argument("--begin_date_day", type=int, default = 1)
    parser.add_argument("--begin_date_month", type=int, default = 10)
    parser.add_argument("--begin_date_year", type=int, default = 2007)
    parser.add_argument("--end_date_day", type=int, default = 5)
    parser.add_argument("--end_date_month", type=int, default = 7)
    parser.add_argument("--end_date_year", type=int, default = 2014)
    parser.add_argument("--resize_output", default = "no")
    parser.add_argument("--reduction_size", type=int, default=3)
    parser.add_argument("--dif_output_name", default = "")
    parser.add_argument("--nr_patches", type=int, default = None, help="nr of patches on one row, total nr of patches= nr_patches^2")
    parser.add_argument("--overlap", type=int, default = None)
    parser.add_argument("--sample_per_file", default = None)
    parser.add_argument("--strict", default = None)
    parser.add_argument("--nr_days", help="nr of days taken into account for a sample", default=None)
      

    args = parser.parse_args()
    kwargs = vars(args)	
    
    
    nr_days = kwargs["nr_days"]
    min_date = datetime.date(kwargs["begin_date_year"], kwargs["begin_date_month"], kwargs["begin_date_day"])
    max_date = datetime.date(kwargs["end_date_year"], kwargs["end_date_month"], kwargs["end_date_day"])

    input_folder = input_folder+"\\"+kwargs["case_name"] + r"\daily_freqs"
    print(input_folder)
    
    overlap = kwargs["overlap"]
    case_name = kwargs["case_name"]
    if kwargs["dif_output_name"]!="":
        case_name = kwargs["dif_output_name"]

    if kwargs["strict"] == "no":
        strict = False
    elif not(kwargs["strict"] == "yes" or kwargs["strict"] == None):        
        print("invalid input for strict")
        sys.exit()
        
    if kwargs["resize_output"] == "no":
        resize_output = False
    elif kwargs["resize_output"] == "yes":
        resize_output = True
        case_name += "_red" + str(reduction_size)  
        print("resize output with reduction size", reduction_size)
    else:
        print("invalid input for resize output")
        sys.exit()
    
    if kwargs["patches"]=="no":
        patches = False        
    elif kwargs["patches"]=="yes":
        patches = True
        case_name+="_ndp"+str(len(sample_days))
        if kwargs["nr_patches"]==None or kwargs["overlap"]==None:
            print("required argument nr patches or overlap not defined")
            sys.exit()
        nr_patches = kwargs["nr_patches"]
        case_name+="_nrp"+str(nr_patches)
    else:
        print("invalid value for patches")
        sys.exit()
        
    if not os.path.exists(output_folder+"\\"+case_name):
        os.makedirs(output_folder+"\\"+case_name)	
    print( "directory made"	)

    if patches:
        print("PATCHES")
        if kwargs["sample_per_file"] == None:
            rewrite_patches(min_date, max_date)
        elif kwargs["sample_per_file"]=="yes":
            rewrite_patches(min_date, max_date, file_for_each_sample=True)
    else:
        if kwargs["sample_per_file"]=="yes":
            rewrite(min_date, max_date, sample_per_file=True)
        else:
            rewrite(min_date, max_date)

    print(case_name)
    if patches:
        f = open(output_folder +r"\patches_"+case_name+ r"\info_params_"+case_name+".txt","w")
    else:
        f = open(output_folder +"\\"+case_name+ r"\info_params_"+case_name+".txt","w")
        
    f.write("\n\n")
    for k in kwargs.keys():
        f.write(str(k)+" "+str(kwargs[k])+"\n")
    f.close()
    print("==============\nDONE\n==============")
	