from thesis_utilities import *
import numpy
import os

def from_log(case_name, line_nr, p1, p2):
    folder = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\patch_"+str(p1)+"_"+str(p2)+"\\log"
    try:    
        interesting_files = [ f for f in os.listdir(folder) if f.startswith('Train')]
        logfiles = sorted(interesting_files)
        # print(folder)
        # print(os.listdir(folder))
        # print(interesting_files)
        if len(logfiles)!=0:
            most_recent = logfiles[-1]
            # print("Most recent file",most_recent)
            
            f = open(folder+"\\"+most_recent)
            i = 1
            for l in f:
                if i == line_nr:
                    l = l.split(" ")
                    return(float(l[1]))
                i+=1        
    except FileNotFoundError:
        # print("no logs found", case_name, p1, p2)
        pass
        
    return None

            
def from_logs(nr_patches, case_name, line_nr):
    acc = []
    for i in range(nr_patches):
        for j in range(nr_patches):
            acc_r = from_log(case_name, line_nr, i,j)
            if acc_r!=None:
                acc.append(acc_r)
    acc=np.array(acc)
    print("average accuracy", case_name, "\n", np.mean(acc))    
    return acc, np.mean(acc)

def check_results(location, prefix, max_dif_eq, stop, start=0):
    n = 0
    up_down_correct = 0
    # interval_correct = 0
    # interval_good_correct = 0
    # good_interval_size = 0
    
    n_nz=0
    up_down_correct_nz = 0
    # interval_correct_nz = 0
    # interval_good_correct_nz = 0
    # good_interval_size_nz = 0
    
    for i in range(start, stop):
        found = False
        try:
            f_in = open(location+"\\"+prefix+four_digit_string(i)+".csv", "r")
            found = True
        except IOError:
            pass
        if found:
            for line in f_in:
                n+=1
                line = line.split(",")
                day_five = float(line[0])
                target = float(line[1])
                up_down = int(line[2])
                # print(day_five, target, max_dif_eq)
                
                lb = day_five-max_dif_eq
                ub = day_five+max_dif_eq
                
                higher_right = target <= lb and up_down ==0
                equal_right = target > lb and target < ub and up_down == 1
                lower_rigt = target >= ub and up_down ==2
                
                if lower_rigt or higher_right or equal_right:
                    up_down_correct+=1
                    
                if not(target==0 and day_five==0):   
                    n_nz +=1
                    if lower_rigt or higher_right or equal_right:
                        up_down_correct_nz+=1
    perc_corr_n = -100
    perc_corr_nz = -100    
    if n>0:
        print("n", n)  
        perc_corr_n = up_down_correct/n        
        print("percentage up down correct", perc_corr_n)
        
        print("n non zero", n_nz)
        perc_corr_nz = up_down_correct_nz/n_nz
        print("percentage up down correct only non zeros", perc_corr_nz)        
    else:
        print("No results")
        perc_corr_n = None
        perc_corr_nz = None
        
    return (perc_corr_n,perc_corr_nz)

def check_results_simple_Version(location, max_dif_eq):
    n = 0
    up_down_correct = 0 
    n_nz=0
    up_down_correct_nz=0
    found = False
    try:
        f_in = open(location, "r")
        found = True
    except IOError:
        pass
        
    if found:
        for line in f_in:
            good = True
            n+=1
            line = line.split(",")
            try:
                day_five = float(line[0])
                target = float(line[1])
                up_down = int(line[2])  
            except ValueError:
                print("value error\n",line)
                good = False
            
            if good:
                lb = day_five-max_dif_eq
                ub = day_five+max_dif_eq
                
                higher_right = target <= lb and up_down ==0
                equal_right = target > lb and target < ub and up_down == 1
                lower_rigt = target >= ub and up_down ==2
                
                if lower_rigt or higher_right or equal_right:
                    up_down_correct+=1
                    
                if not(target==0 and day_five==0):   
                    n_nz +=1
                    if lower_rigt or higher_right or equal_right:
                        up_down_correct_nz+=1    
    if n>0:
        print("n", n)                
        print("percentage up down correct", up_down_correct/n)   
        print("n non zero", n_nz)
        print("percentage up down correct only non zeros", up_down_correct_nz/n_nz)        
    else:
        print("No results")

     
def check_shizzle(normal, random, prefix, nr_patches, stop , prefix_location, max_dif_eq):
    perc_n = []
    perc_nz = []
    print("Real landscape")
    for i in range(nr_patches):
        for j in range(nr_patches):
            location = prefix_location+ "\\"+normal+ r"\patch_"+str(i)+"_"+str(j)+r"\data"
            print("\n==========================\nPatch", i, j)
            p1,p2 = check_results(location, prefix, max_dif_eq, stop)
            # print(p1, p2)
            if not (p1==None and p2==None):
                perc_n.append(p1)
                perc_nz.append(p2)                               
    
    perc_n_random = []
    perc_nz_random = []
    print("\n\nRandom landscape")
    for i in range(nr_patches):
        for j in range(nr_patches):
            location = prefix_location+"\\"+random+r"\patch_"+str(i)+"_"+str(j)+r"\data"
            print("\n==========================\nPatch", i, j)
            p1,p2 = check_results(location, prefix, max_dif_eq, stop)
            # print(p1, p2)
            if not( p1==None and p2==None):
                perc_n_random.append(p1)
                perc_nz_random.append(p2)                  
    
    perc_n_random = np.array(perc_n_random)
    perc_nz_random = np.array(perc_nz_random)
    perc_n = np.array(perc_n)
    perc_nz = np.array(perc_nz)
    
    print("\n\n\nnr patches real and random", perc_n.shape[0], perc_n_random.shape[0] )
    print("average performance real landscape:", np.mean(perc_n), "sd:", np.std(perc_n))
    print("average performance on non zeros real landscape:", np.mean(perc_nz), "sd:", np.std(perc_nz))
    print("\naverage performance random landscape:", np.mean(perc_n_random), "sd:", np.std(perc_n_random))
    print("average performance on non zeros random landscape:", np.mean(perc_nz_random), "sd:", np.std(perc_nz_random))
        
if __name__ == "__main__":
    
    # nr_patches = 5
    # line_nr = 1997
    # case_name = "patches_pol_ed_norm_ndp5_nrp5"
    # from_logs(nr_patches, case_name, line_nr)

    # case_name = "patches_pol_ed_rand_ndp5_nrp5"
    # from_logs(nr_patches, case_name, line_nr)

    prefix = "sample_out" 
    nr_patches = 5
    stop = 290 #=nr of samples in set
    prefix_location = r"D:\Users\Lydia\results_freqs\nn_data"
    max_dif_eq = 0.02
    
    print("Real random comparison")
    normal = "patches_pol_ed_norm_ndp5_nrp5"
    random = "patches_pol_ed_rand_ndp5_nrp5"
    check_shizzle(normal, random, prefix, nr_patches, stop , prefix_location, max_dif_eq)
    
    
    # print("No fillup with zeros")
    # normal = "patches_politics_ad_lim_ns_ndp5_nrp5"
    # random = "patches_politics_ad_lim_ns_random_ndp5_nrp5"
    # check_shizzle(normal, random, prefix, nr_patches, stop , prefix_location, max_dif_eq)
    
    # print("diff = ", max_dif_eq)
    # print("\n\nFillup with zeros")
    # normal = "patches_politics_ad_lim_ns_strict_o2_ndp5_nrp5"
    # random = "patches_politics_ad_lim_ns_random_strict_o2_ndp5_nrp5"
    # check_shizzle(normal, random, prefix, nr_patches, stop , prefix_location, max_dif_eq)
    
            
    # stop = 5000 #=nr of samples in set
    # print("\n\nvalidation")
    # location = r"D:\Users\Lydia\results_freqs\nn_data\weird_dif0.001\validationset.csv"
    # check_results_simple_Version(location, max_dif_eq)   
    # stop = 1651692-10000 #=nr of samples in set
    # print("\ntrain")        
    # location = r"D:\Users\Lydia\results_freqs\nn_data\weird_dif0.001\trainset.csv"
    # check_results_simple_Version(location, max_dif_eq)
    
    # print("\n\Perfect data")
    # for i in range(nr_patches):
        # for j in range(nr_patches):
            # location = prefix_location+r"\patches_perfect_easy_data_ndp5_nrp5\patch_"+str(i)+"_"+str(j)+r"\data"
            # print("\n==========================\nPatch", i, j)
            # check_results(location, prefix, stop)
            
            
            
            