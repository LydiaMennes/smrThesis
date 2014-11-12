import os

def remove_files_patch(folder):
    
    try:
        print(os.listdir(folder))
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:                
                os.unlink(file_path)
            except:
                print("exception clearing folder")
    except FileNotFoundError:
        print(folder, "\t NOT FOUND")
            
def remove_files_output_ed(nr_patches, location):
     for i in range(nr_patches):
        for j in range(nr_patches):
            remove_files_patch(location+"\\patch_"+str(i)+"_"+str(j)+"\\data")
                
if __name__ == "__main__":
    
    # nr_patches = 5
    # location = r"D:\Users\Lydia\results_freqs\nn_data\patches_politics_ad_lim_ns_strict_ndp5_nrp5"
    # remove_files_output_ed(nr_patches, location)
    
    # location=r"D:\Users\Lydia\results_freqs\nn_data\patches_politics_ad_lim_ns_random_strict_ndp5_nrp5"
    # remove_files_output_ed(nr_patches, location)
   
   
   
    # x = r"D:\Users\Lydia\results_freqs\nn_data\patches_politics_ad_lim_ns_random_strict_ndp5_nrp5\patch_4_0\data"
    # y = r"D:\Users\Lydia\results_freqs\nn_data\patches_politics_ad_lim_ns_random_strict_ndp5_nrp5\patch_4_0\data"
    
    # if x==y:
        # print("it is the fucking same")