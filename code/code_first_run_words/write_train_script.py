import math
import datetime

def write_files(nn_data_case_name, result_freqs_case_name, nr_patches, nr_days, dif, window_size, nr_hidden = 50, learnrate=0.05, momentum = 0.3):
    template_bat = r"D:\Users\Lydia\van_Ed\svl\DeepLearn.exe D:\Users\Lydia\results_freqs\nn_data"
    template_result_freq = r"D:\Users\Lydia\results_freqs"

    nr_classes=3
    nr_inputs_network = window_size*window_size*nr_days
    tft1 = "[DeepNet]\nNrOfSvl = 1\nNrOfClasses = "+str(nr_classes)+"\n\n[Build]\nInputMap = \""
    tft2 = "\"\nOutputMap = \""
    tft3 = "\"\nTrain=0.85\nSeed=123456\nHistory="+str(nr_days)+"\nNrOfInput="
    tft4 = "\nNrOfOut="
    tft5 = "\nDiff="
    tft6 = "\nWs="+ str(window_size)
    
    tft7 = "\n\n[BuildSkip]\nLoadSvl = false\n\n[Svl_0]\nNrOfIteration=100\nSeed=123456\nNrOfLayers=3\nNrOfInput="+str(nr_inputs_network)+"\nNrOfHidden1="+str(nr_hidden)+"\nNrOfOutput=3\nLearnrate=0.05\nMomentum=0.3"

    trainFileName = r"\Train.ini"

    bat_file = open(template_result_freq+r"\nn_data"+"\\"+nn_data_case_name+r"\train.bat", "w")

    for i in range(nr_patches):
        for j in range(nr_patches):
            print("patch",i,j)
            bat_file.write(template_bat+"\\"+nn_data_case_name+r"\patch_"+str(i)+"_"+str(j)+trainFileName+"\n")
            
            input_map = template_result_freq+r"\nn_data"+"\\"+nn_data_case_name+r"\patch_"+str(i)+"_"+str(j)+r"\input"
            output_map = template_result_freq+r"\nn_data"+"\\"+nn_data_case_name+r"\patch_"+str(i)+"_"+str(j)+r"\output"
                        
            info_file = open(template_result_freq+"\\"+result_freqs_case_name+r"\daily_freqs\patches\patch_"+str(i)+"_"+str(j)+"_info.txt","r")
            line = info_file.readline()
            line = line.split(" ")            
            x = int(math.floor( float(line[-1])))
            line = info_file.readline()
            line = line.split(" ")            
            y = int(math.floor( float(line[-1])))
            print("Input nr rows=",x,"nr cols",y)
            inputs = x*y
            line = info_file.readline()
            line = line.split(" ")            
            x = int(math.floor( float(line[-1])))
            line = info_file.readline()
            line = line.split(" ")            
            y = int(math.floor( float(line[-1])))            
            print("output nr cols=",x,"nr cols",y)
            outputs = x*y

            trainFileContent = tft1+input_map+tft2+output_map+tft3+str(inputs)+tft4+str(outputs)+tft5+str(dif)+tft6+tft7

            trainFile = open(template_result_freq+r"\nn_data"+"\\"+nn_data_case_name+r"\patch_"+str(i)+"_"+str(j)+trainFileName, "w")
            trainFile.write(trainFileContent)
 
def write_files_whole_landscape(nn_data_case_name, nr_days, dif, window_size, landscape_size, overlap, nr_hidden = 50, learnrate=0.05, momentum = 0.3, train_extension="", seed = 123456):
    template_bat = r"D:\Users\Lydia\van_Ed\svl\DeepLearn.exe "
    template_result_freq = r"D:\Users\Lydia\results_freqs"

    nr_classes=3
    nr_inputs_network = window_size*window_size*nr_days
    tft1 = "[DeepNet]\nNrOfSvl = 1\nNrOfClasses = "+str(nr_classes)+"\n\n[Build]\nInputMap = \""
    tft2 = "\"\nOutputMap = \""
    tft3 = "\"\nTrain=0.85\nSeed="+str(seed)+"\nHistory="+str(nr_days)+"\nNrOfInput="
    tft4 = "\nNrOfOut="
    tft5 = "\nDiff="
    tft6 = "\nWs="+ str(window_size)
    
    tft7 = "\n\n[BuildSkip]\nLoadSvl = false\n\n[Svl_0]\nNrOfIteration=100\nSeed=123456\nNrOfLayers=3\nNrOfInput="+str(nr_inputs_network)+"\nNrOfHidden1="+str(nr_hidden)+"\nNrOfOutput=3\nLearnrate=0.05\nMomentum=0.3"

    trainFileName = r"\Train"+train_extension+".ini"
    trainFileLoc = template_result_freq+r"\nn_data"+"\\"+nn_data_case_name+r"\whole"+trainFileName
        
    bat_file_name = template_result_freq+r"\nn_data"+"\\"+nn_data_case_name+r"\train"+train_extension+".bat"
    bat_file = open(bat_file_name, "w")
    bat_file.write(template_bat+trainFileLoc+"\n")
    
    input_map = template_result_freq+r"\nn_data"+"\\"+nn_data_case_name+r"\whole\input"
    output_map = template_result_freq+r"\nn_data"+"\\"+nn_data_case_name+r"\whole\output"
                
    inputs = int(math.pow(landscape_size+(overlap*2), 2))
    outputs = int(math.pow(landscape_size, 2)) 

    trainFileContent = tft1+input_map+tft2+output_map+tft3+str(inputs)+tft4+str(outputs)+tft5+str(dif)+tft6+tft7
    trainFile = open(trainFileLoc, "w")
    trainFile.write(trainFileContent) 
    
    return bat_file_name
    

def patches_run():
    nr_patches = 5
    nr_days = 5
    # dif = 0.001
    window_size = 5    
    dif = 0.01    
    
    nr_patches=5 
    result_freqs_case_name = "pol_ed_norm" 
    nn_data_case_name = "patches_pol_ed_norm_ndp5_nrp5"
    write_files(nn_data_case_name, result_freqs_case_name, nr_patches, nr_days, dif, window_size)
    
    
    result_freqs_case_name = "pol_ed_rand" 
    nn_data_case_name = "patches_pol_ed_rand_ndp5_nrp5"
    write_files(nn_data_case_name, result_freqs_case_name, nr_patches, nr_days, dif, window_size)
    
    
    # nn_data_case_name = "patches_politics_ad_lim_ns_strict_o2_ndp5_nrp5"
    # result_freqs_case_name = "politics_ad_lim_ns_strict_o2"
    # write_files(nn_data_case_name, result_freqs_case_name, nr_patches, nr_days, dif, window_size)
    
    # nn_data_case_name = "patches_politics_ad_lim_ns_random_strict_o2_ndp5_nrp5"
    # result_freqs_case_name = "politics_ad_lim_ns_random_strict_o2"
    # write_files(nn_data_case_name, result_freqs_case_name, nr_patches, nr_days, dif, window_size)
    
    # nn_data_case_name = "patches_politics_ad_lim_ns_small_ndp5_nrp18"
    # result_freqs_case_name = "politics_ad_lim_ns_small"
    # write_files(nn_data_case_name, result_freqs_case_name, nr_patches, nr_days)
    
    # nn_data_case_name = "patches_perfect_easy_data_ndp5_nrp5"
    # result_freqs_case_name = "perfect_easy_data"
    # write_files(nn_data_case_name, result_freqs_case_name, nr_patches, nr_days)    
    
def whole_landscape_make():
    # write_files_whole_landscape(nn_data_case_name, result_freqs_case_name, nr_days, dif, window_size, landscape_size, overlap, nr_hidden = 50, learnrate=0.05, momentum = 0.3, train_extension="", seed = 123456)
    nr_days = 5
    dif = 0.01
    window_size = 5 
    landscape_size = 90
    overlap = 2 
    bats = []
    
    
       
    # nn_data_case_name = "politics_lim_ns_swrem_whole_o2_logns"
    # bat = write_files_whole_landscape(nn_data_case_name, nr_days, dif, window_size, landscape_size, overlap)
    # bats.append(bat)
    
    # nn_data_case_name = "football_lim_ns_swrem_whole_o2_logns"
    # bat = write_files_whole_landscape(nn_data_case_name, nr_days, dif, window_size, landscape_size, overlap)
    # bats.append(bat)
    
    # nn_data_case_name = "politics_lim_ns_swrem_whole_o2"
    # bat = write_files_whole_landscape(nn_data_case_name, nr_days, dif, window_size, landscape_size, overlap)
    # bats.append(bat)
    
    # nn_data_case_name = "football_lim_ns_swrem_whole_o2"
    # bat = write_files_whole_landscape(nn_data_case_name, nr_days, dif, window_size, landscape_size, overlap)
    # bats.append(bat)
    
    
    
    train_loads = open(r"D:\Users\Lydia\results_freqs\nn_data\train_a_lot.bat", "w")
    for x in bats:
        train_loads.write(x+"\n")
    train_loads.close()
    
    
if __name__ == "__main__":

    patches_run()
    
    
    # whole_landscape_make()




    