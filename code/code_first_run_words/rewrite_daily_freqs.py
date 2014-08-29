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
patch_days = [30,7,3,2,1]

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
        if line[-1] != ";":
            line += ";"
        line_str+=line
    return line_str  

def rewrite_patches(min_date, max_date):    
    input_folder_patch = input_folder+r"\patches"
    nr_exceptions = 0
    for p1 in range(nr_patches):
        for p2 in range(nr_patches):
            nr_samples = 0
            date = copy.copy(min_date)
            output_folder_patch = output_folder + r"\patches_"+case_name+"\\patch_"+str(p1)+"_"+str(p2)
            if not os.path.exists(output_folder_patch):
                os.makedirs(output_folder_patch)
            while date <= max_date:
                good = True
                current_date = copy.copy(date)
                total_str = ""
                output_str = ""
                for pd in patch_days:                  
                    try:
                        f_name= input_folder_patch+"\\day"+str(current_date)+"\patch_"+str(p1)+"_"+str(p2)+".txt"
                        f_in = open(f_name,"r")
                    except IOError:
                        nr_exceptions+=1
                        good = False                                               
                        break
                    total_str+=to_line(f_in)                    
                    f_in.close()
                    current_date = date-datetime.timedelta(pd)
                if good:
                    try:
                        f_in = open(input_folder_patch+"\\day"+str(date)+"\patch_"+str(p1)+"_"+str(p2)+".txt")
                    except IOError:
                        nr_exceptions+=1
                        good = False
                        break
                    output_str = to_line(f_in)
                    f_in.close()
                if good:                
                    # print("day"+str(date)+".txt")
                    if total_str[-1] == ";":
                        total_str = total_str[:-1]
                    if output_str[-1] == ";":
                        output_str = output_str[:-1]
                    f = open(output_folder_patch+r"\input"+str(nr_samples)+".txt", "w")
                    f.write(total_str)
                    f.close()
                    f = open(output_folder_patch+r"\output"+str(nr_samples)+".txt", "w")
                    f.write(output_str+"\n")
                    f.close()
                    nr_samples+=1
                date += datetime.timedelta(1)
    print("nr samples", nr_samples,"nr exceptions", nr_exceptions)
    f = open(output_folder + r"\patches_"+case_name+r"\info_"+case_name+".txt","w")
    f.write("nr samples = " + str(nr_samples) + "\n")
    f.write("number of days per sample = " + str(patch_days) + "\n")
    if resize_output:
        f.write("resizing with size = " + str(reduction_size) + "\n resulting size =" + str(res_size) + "\n")
    else:
        f.write("no resizing\n")
    f.close()
    
def rewrite(nr_days, date, max_date):
    nr_samples = 0
    nr_exceptions = 0
    f = open(output_folder+"\\"+case_name+".csv", "w")
    delta = datetime.timedelta(1)
    while date + nr_days + datetime.timedelta(1) <= max_date:
        good = True
        current_date = copy.copy(date)
        total_str = ""
        for i in range(nr_days.days+1):
            try:
                f_in = open(input_folder+r"\day"+str(current_date)+".txt")
            except IOError:
                nr_exceptions+=1
                good = False
                break
            if i == nr_days.days:
                # print(",",i)
                if total_str[-1]==";":
                    total_str=total_str[0:-1]
                total_str+=","
                if resize_output:
                    line_str, res_size = to_line_reduce(f_in)
                    total_str+= line_str
                else:
                    total_str+= to_line(f_in)
            else:
                total_str+= to_line(f_in)
            f_in.close()
            current_date = current_date+delta
        if good:
            # print("day"+str(date)+".txt")
            nr_samples+=1
            f.write(total_str+"\n")
        else:
            print("FAIL day"+str(date)+".txt")            
        date = date+delta
    f.close()
    print("nr samples", nr_samples,"nr exceptions", nr_exceptions)
    f = open(output_folder+r"\info_"+case_name+".txt","w")
    f.write("nr samples = " + str(nr_samples) + "\n")
    f.write("number of days per sample = " + str(nr_days.days) + "\n")
    if resize_output:
        f.write("resizing with size = " + str(reduction_size) + "\n resulting size =" + str(res_size) + "\n")
    else:
        f.write("no resizing\n")
    f.close()
  
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Run puzzle algorithm')
    # '''parser.add_argument(<naam>, type=<type>, default=<default>, help=<help message>)'''
    parser.add_argument("case_name", help="Name of the data case that you want to process")
    parser.add_argument("nr_days", help="nr of days taken into account for a sample")
    parser.add_argument("begin_date_day", type=int)
    parser.add_argument("begin_date_month", type=int)
    parser.add_argument("begin_date_year", type=int)
    parser.add_argument("end_date_day", type=int)
    parser.add_argument("end_date_month", type=int)
    parser.add_argument("end_date_year", type=int)
    parser.add_argument("patches", help="yes or no")    
    parser.add_argument("--resize_output", default = "no")
    parser.add_argument("--reduction_size", type=int, default=3)
    parser.add_argument("--dif_output_name", default = "")
    parser.add_argument("--nr_patches", type=int, default = None)
    

    args = parser.parse_args()
    kwargs = vars(args)	
    
    
    nr_days = kwargs["nr_days"]
    min_date = datetime.date(kwargs["begin_date_year"], kwargs["begin_date_month"], kwargs["begin_date_day"])
    max_date = datetime.date(kwargs["end_date_year"], kwargs["end_date_month"], kwargs["end_date_day"])

    input_folder = input_folder+"\\"+kwargs["case_name"] + r"\daily_freqs"
    reduction_size = kwargs["reduction_size"]
    
    case_name = kwargs["case_name"]
    if kwargs["dif_output_name"]!="":
        case_name = kwargs["dif_output_name"]
    case_name+="_nd"+str(nr_days)

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
        if kwargs["nr_patches"]==None:
            print("required argument nr patches not defined")
            sys.exit()
        nr_patches = kwargs["nr_patches"]
    else:
        print("invalid value for patches")
        sys.exit()
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)	
    print( "directory made"	)

    if patches:
        print("PATCHES")
        rewrite_patches(min_date, max_date)
    else:
        rewrite(datetime.timedelta(nr_days), min_date, max_date)

    f = open(output_folder + r"\patches_"+case_name+r"\info_"+case_name+".txt","a")
    f.write("\n\n")
    for k in kwargs.keys():
        f.write(str(k)+" "+str(kwargs[k])+"\n")
    f.close()
    print("==============\nDONE\n==============")
	