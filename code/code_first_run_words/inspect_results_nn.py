import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys

folder = r"D:\Users\Lydia\results_nn"
round = [False]

fontsize = 9
line_thickness = 2
nr_columns = 2

def set_font(ax):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]+ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(fontsize)

def get_values(case_names, run_nr=None, folder_suffix=None):
    legend = []
    first = True
    x = []
    y = [[],[],[],[]]
    max_len = 0
    for i in range(len(case_names)):
        y[0].append([])
        y[1].append([])
        y[2].append([])
        y[3].append([])
        x.append([])
        if folder_suffix==None:
            in_folder=folder
        else:   
            in_folder = folder+"\\"+folder_suffix
        if run_nr==None:
            case_name = case_names[i]
        else:
            case_name = case_names[i]+"_run"+str(run_nr)
        f = open(in_folder+"\\"+case_name+r"\log.txt")
        for line in f:
            line = line.replace(" " , "")
            line = line.split(",")
            if first:
                first = False
                if len(line)>8:
                    test_acc_available = True
                    legend = [line[0],line[2],line[4],line[6], line[8]]
                else:
                    test_acc_available = False
                    legend = [line[0],line[2],line[4],line[6]]
                    
            x[i].append(int(line[1]))
            y[0][i].append(float(line[3]))
            y[1][i].append(float(line[5]))
            y[2][i].append(float(line[7]))
            if test_acc_available:
                y[3][i].append(float(line[9]))
        f.close()
    if not test_acc_available:
        del y[3]
    return (x,y,legend)
    
def get_values_averaged(case_names, nr_runs, folder_suffix):
    legend = []
    first = True
    x = []
    y = [[],[],[],[]]
    max_len = 0
    
    best_runs = []
    for i in range(len(case_names)):
        x.append([])
        case_name = case_names[i]
        first_run = True
        y0_avg_vals=[]
        y1_avg_vals=[]
        y2_avg_vals=[]
        y3_avg_vals=[]
        for run_nr in range(nr_runs):
            
            if folder_suffix == None:
                file_name_in = folder+"\\"+case_name+"_run"+str(run_nr)+r"\log.txt"
            else:
                file_name_in=folder+"\\"+folder_suffix+"\\"+case_name+"_run"+str(run_nr)+r"\log.txt"
                
            f = open(file_name_in)
            line_nr = 0
            for line in f:
                line = line.replace(" " , "")
                line = line.split(",")
                  
                if first:
                    first = False
                    legend = [line[0],line[2],line[4],line[6], line[8]]
                if first_run:
                    x[i].append(int(line[1]))
                    y0_avg_vals.append(float(line[3]))
                    y1_avg_vals.append(float(line[5]))
                    y2_avg_vals.append(float(line[7]))
                    y3_avg_vals.append(float(line[9]))
                    # print(line_nr)
                    max_val = float(line[5])
                    best_run = 0
                else:
                    if line_nr >= len(y0_avg_vals):                    
                        print("\n\n",len(y0_avg_vals), line_nr)
                        print(file_name_in)
                        print("run", run_nr)
                        print("line nr", line_nr, "\n\n")
                    y0_avg_vals[line_nr]+=float(line[3])
                    y1_avg_vals[line_nr]+=float(line[5])
                    y2_avg_vals[line_nr]+=float(line[7])
                    y3_avg_vals[line_nr]+=float(line[9])
                    if float(line[5]) > max_val:
                        max_val = float(line[5])
                        best_run = run_nr
                    
                line_nr+=1
            f.close()
            first_run=False
        y[0].append(list(np.array(y0_avg_vals)/nr_runs))
        y[1].append(list(np.array(y1_avg_vals)/nr_runs))
        y[2].append(list(np.array(y2_avg_vals)/nr_runs))
        y[3].append(list(np.array(y3_avg_vals)/nr_runs))
        best_runs.append(best_run)
        
    return (x,y,legend, best_runs)

def accuracies_table_avg(labels, f_out, case_names, nr_runs, folder_suffix, folder):
    
    f_out_all = open(folder+"\\all_values_test.txt", "w")
    
    # result = np.zeros((len(case_names),3))
    result = []    
    avg_best_reached_test = []
    for cn in case_names:
        avg_best_reached_test.append(0)
        result.append([[],[],[]])
        f_out_all.write(cn + "\t\t\t")
    f_out_all.write("\n")
    
        
    for j in range(nr_runs):
        x,y,leg = get_values(case_names, run_nr=j, folder_suffix=folder_suffix)
        x_avg, y_avg, leg2, br = get_values_averaged(case_names, nr_runs, folder_suffix=folder_suffix)
        
        for i in range(len(case_names)):
        
            best_acc_val = np.max(y[1][i])
            # result[i][0] += best_acc_val            
            result[i][0].append(best_acc_val)
            f_out_all.write("val " + string_val(best_acc_val))
            best_acc_val_ind = np.argmax(y[1][i])
            # print(case_names[i], "best: ", best_acc_val_ind)
            
            avg_best_reached_test[i] += np.max(y[3][i])
            best_test_val = y[3][i][best_acc_val_ind]
            # result[i][2] += best_test_val
            result[i][2].append(best_test_val)
            f_out_all.write(" test " + string_val(best_test_val))
            
            best_train_val = y[2][i][best_acc_val_ind] 
            # result[i][1] += best_train_val
            result[i][1].append(best_train_val)
            f_out_all.write(" train " + string_val(best_train_val))            
            
            f_out_all.write(" iternr " + string_val(best_acc_val_ind) + " -- ")
        f_out_all.write("\n")        
    f_out_all.write("\nbest test value averaged over runs " +case_names[0]+ "\t" + string_val(avg_best_reached_test[0]/nr_runs)+"\n"+case_names[1]+ "\t" + string_val(avg_best_reached_test[1]/nr_runs)+"\n" +case_names[2]+ "\t"+ string_val(avg_best_reached_test[2]/nr_runs)+ "\n")        
    f_out_all.close()
    
    # result = result/nr_runs
    
    for i in range(len(case_names)):
        f_out.write(labels[i]+" & "+string_val(np.mean(np.array(result[i][0])))+" & " +string_val(np.std(np.array(result[i][0])))+" & " + string_val(np.mean(np.array(result[i][1])))+" & "+string_val(np.std(np.array(result[i][1])))+" & "+string_val(np.mean(np.array(result[i][2])))+" & "+string_val(np.std(np.array(result[i][2]))) +" \\\\\n")

    
def accuracies_table_no_avg(y, labels, f_out, nr_case_names):
    for i in range(nr_case_names):
        # x1,y1,leg = get_values(case_names, run_nr=best_runs[i], folder_suffix=folder_suffix)
        best_acc_val = np.max(y[1][i])
        best_acc_val_ind = np.argmax(y[1][i])
        print(case_names[i], "best: ", best_acc_val_ind)
        best_acc_train = y[2][i][best_acc_val_ind]
        if len(y) > 3:
            best_acc_test = y[3][i][best_acc_val_ind]
            f_out.write(labels[i]+" & "+string_val(best_acc_train)+" & " + string_val(best_acc_val)+" & "+string_val(best_acc_test)+" \\\\\n")
        else:
            f_out.write(labels[i]+" & "+string_val(best_acc_train)+" & " + string_val(best_acc_val)+" \\\\\n")
            

def comparisons(case_names, colors,labels, suffix="", max_iter=None, round_vals=False, average=False, nr_runs=None, folder_suffix=None):

    if round_vals:
        round[0]=True
    
    if average:
        if nr_runs == None:
            print("nr runs not specified")
            sys.exit()
        x,y,legend, best_runs = get_values_averaged(case_names, nr_runs, folder_suffix)
    else:
        x, y, legend = get_values(case_names)
        
    for i in range(len(y)):
        fig, ax = plt.subplots(1)       
        fig.set_figheight(4)
        fig.set_figwidth(3)        
        print(i)
        for j in range(len(case_names)):
            # print(x[j], y[i][j])
            if max_iter == None:
                ax.plot(x[j], y[i][j], color = colors[j], label=labels[j], linewidth=line_thickness)     
            else:
                ax.plot(x[j][0:max_iter], y[i][j][0:max_iter], color = colors[j], label=labels[j], linewidth=line_thickness)     
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.5, box.width, box.height * 0.5])    
        col_len = nr_columns
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=col_len, prop={'size':fontsize})
        # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True)
        ax.set_xlabel("iteration")
        ax.set_ylabel(legend[i+1])
        ax.set_title("compare "+legend[i+1]+"\n")
        if max_iter != None:
            ax.set_xlim(0, max_iter)
        set_font(ax)
        image_name = folder  + "\\"+ legend[i+1]  +"_comparison"+suffix  + ".pdf"
        fig.savefig(image_name, bbox_inches='tight')
        image_name = folder + "\\"+ legend[i+1]  +"_comparison"+suffix  + ".png"        
        fig.savefig(image_name, bbox_inches='tight')
        plt.close()
    

    f_out = open(folder+"\\comparison_table"+suffix+".txt","w")
    
    f_out.write("\\begin{table}[h] \n \\small \n\\centering\n\\begin{tabular}{|c|")
    for i in range(3):
        f_out.write("cc|")    
    f_out.write("}\n\\hline \n Setting & \multicolumn{2}{c}{Train} & \multicolumn{2}{c}{Validation} & \multicolumn{2}{c}{Test} \\\\\n\\hline\n")    
    f_out.write(" & Acc & Sd & Acc & Sd & Acc & Sd \\\\\n\\hline\n")    
    if average:
        accuracies_table_avg(labels,f_out, case_names, nr_runs, folder_suffix, folder)
    else:
        accuracies_table_no_avg(y, labels, f_out, len(case_names))
    f_out.write("\\hline \n\\end{tabular} \n\\caption{} \n\\label{} \n\\end{table}")            
    f_out.close()
    
    if average:
        return best_runs
    
    
def string_val(x):
    if round[0]:
        return "{0:.4f}".format(x)
    else:
        return str(x)
    
def conf_matrix_to_file(case_name, matrix, nr_cats, suffix="", folder_suffix=None):
    title_case_name = case_name.replace("_","-")
    title_case_name = title_case_name.replace(".","-")
    sep = " & "
    if folder_suffix==None:
        f_out= open(folder+"\\"+case_name+r"\conf_matrix"+suffix+".txt","w")
    else:
        f_out= open(folder+"\\"+folder_suffix+r"\conf_matrix"+suffix+".txt","w")
    # f_out.write(case_name+"\n")
    
    f_out.write("\\begin{table}[h] \n \\small \n \\centering \n \\begin{tabular} {|c|")
    for i in range(nr_cats):
        f_out.write("c")
    f_out.write("|c|} \n \\hline")
    for i in range(nr_cats):
        f_out.write(sep + str(i) )
    f_out.write(" & sum \\\\ \n \\hline \n")
        
    for i in range(nr_cats):
        f_out.write(str(i)+ sep)
        for j in range(nr_cats):
            f_out.write(string_val(matrix[i,j])+" ")
            if j == nr_cats-1:
                f_out.write(sep+string_val(np.sum(matrix[i,:]))+" \\\\ \n")
            else:
                f_out.write(sep)
    f_out.write("\\hline \nsum")
    for i in range(nr_cats):
        f_out.write(sep + string_val(np.sum(matrix[:,i])) )
    f_out.write(" & \\\\ \n\\hline \n\\end{tabular} \n \\caption{"+title_case_name+"} \n \\label{} \n \\end{table}\n\n\n")
    
    fig_prefixes = ["acctrain_", "accval_", "err_"]
    for pref in fig_prefixes:    
        f_out.write("\n\\begin{figure}[h]\n\\centering\n\\includegraphics[width=0.5\\linewidth]{"+pref+title_case_name+".pdf}\n\\caption{"+title_case_name+"}\n\\label{}\n\\end{figure}\n\n")
    
    f_out.close()
    
def confusion_matrix(case_name, nr_cats, type, folder_suffix=None, name_suffix = ""):
      
    matrix = np.zeros((nr_cats,nr_cats))
    
    if type == "validation":
        data_set = "validationset.csv"
    elif type == "test":
        data_set = "testset.csv"
    
    else:
        print("unknown confusion matrix type")
        sys.exit()
    
    if folder_suffix==None:
        f = open(folder+"\\"+case_name+"\\"+data_set)
    else:
        f = open(folder+"\\"+folder_suffix+"\\"+case_name+"\\"+data_set)
    
    for line in f:
        line = line.split(",")
        matrix[int(line[1]),int(line[3])]+=1
    f.close()
        
    conf_matrix_to_file(case_name, matrix, nr_cats, suffix=name_suffix, folder_suffix=folder_suffix)
    
    matrix = matrix/np.sum(matrix)
    round[0]=True
    conf_matrix_to_file(case_name, matrix, nr_cats, suffix=name_suffix+"_perc", folder_suffix=folder_suffix)
            
def acc_graph(case_name, folder_suffix=None):
    if folder_suffix==None:
        f = open(folder+"\\"+case_name+r"\log.txt")
    else:
        f = open(folder+"\\"+folder_suffix+"\\"+case_name+r"\log.txt")
    legend = []
    first = True
    x = []
    y = [[],[],[],[]]
    for line in f:
        line = line.replace(" " , "")
        line = line.split(",")
        if first:
            first = False
            legend = [line[0],line[2],line[4],line[6], line[8]]
        x.append(int(line[1]))
        y[0].append(float(line[3]))
        y[1].append(float(line[5]))
        y[2].append(float(line[7]))
        y[3].append(float(line[9]))
    f.close()

    
    if "run" in case_name:
        title_case_name= case_name.split("_run")[0]
    title_case_name = title_case_name.replace("_","-")
    title_case_name = title_case_name.replace(".","-")    
    colors = ["r", "g", "b", "m"]
    
    for i in range(len(y)):
        fig, ax = plt.subplots(1)       
        fig.set_figheight(4)
        fig.set_figwidth(4)        
        print(i)
        ax.plot(x, y[i], color = colors[i], label=legend[i+1])     
        # box = ax.get_position()
        # ax.set_position([box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.7])    
        # col_len = 2
        # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=col_len)
        # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True)
        ax.set_xlabel("iteration")
        ax.set_ylabel(legend[i+1])
        ax.set_title(case_name+"\n")
        set_font(ax)
        if folder_suffix==None:
            image_name = folder + "\\"+case_name + "\\"+ legend[i+1]  +"_" + title_case_name + ".pdf"
        else:
            image_name = folder + "\\"+folder_suffix + "\\"+ legend[i+1]  +"_" + title_case_name + ".pdf"            
        fig.savefig(image_name, bbox_inches='tight')
        if folder_suffix==None:
            image_name = folder + "\\"+case_name + "\\"+ legend[i+1]  +"_" + title_case_name + ".png"        
        else:
            image_name = folder + "\\"+folder_suffix + "\\"+ legend[i+1]  +"_" + title_case_name + ".png"        
        fig.savefig(image_name, bbox_inches='tight')
        plt.close()
 
def final_comparison_input_settings():
    folder_suff = "politics_real"
    run_suff = "_politics_real"
    max_it = 100
    nr_runs = 2
    
    
    
    case_names = ["politics_lim_ns_o2_logas_hub_5.0E-4_0.005_40","politics_lim_ns_o0_logas_hub_5.0E-4_0.005_5","politics_lim_ns_random_o2_logas_hub_5.0E-4_0.005_40","politics_lim_ns_o2_logas_no_hub_5.0E-4_0.005_40","politics_lim_ns_o3_logas_hub_5.0E-4_0.005_40","politics_lim_ns_o2_logas_hub_timeind_5.0E-4_0.005_40","politics_lim_ns_o2_logas_hub_tarind5_5.0E-4_0.005_40","politics_lim_ns_o2_logas_hub_tarind10_5.0E-4_0.005_40","politics_lim_ns_o2_logas_hub_timeind_tarind5_5.0E-4_0.005_40"]
    labels = ["Plain","No context", "Random context", "No hub", "Window size 7", "Time indication", "Target encoding 5 bin", "Target encoding 10 bin", "Target enc. 5 bin + time indic."]
    for c in case_names:
        print(c)
    colors = ["Black", "Green", "LawnGreen","BlueViolet", "FireBrick","Fuchsia", "Aqua", "Blue",  "DodgerBlue"]
    best_runs = comparisons(case_names, colors, labels, suffix = run_suff, max_iter=50, round_vals=True, average=True, nr_runs=nr_runs, folder_suffix=folder_suff)
    
    nr_cats = 6
    f_out = open(r"D:\Users\Lydia\results_nn"+"\\"+folder_suff+r"\best_run_overview.txt","w")
    for i in range(len(case_names)):
        print(case_names[i], "best run", best_runs[i])
        case_name = case_names[i]+"_run"+str(best_runs[i])
        confusion_matrix(case_name, nr_cats, "validation", folder_suffix = folder_suff, name_suffix=labels[i]+"_val")
        confusion_matrix(case_name, nr_cats, "test", folder_suffix = folder_suff, name_suffix=labels[i]+"_test")
        acc_graph(case_name, folder_suffix = folder_suff)
        f_out.write(labels[i]+", "+str(best_runs[i])+"\n")
        
    f_out.close()
  
def comparison_politics_names():
    
    folder_suff = "poltics_names_all_limited_time_longer_new"
    run_suff = "_poltics_names_limited_time_longer_new"
    max_it = 500
    nr_runs = 100
    case_names = ["politics_names_o2_hub2_0.005_0.05_40","politics_names_o0_hub2_0.005_0.05_40","politics_names_o2_hub_random2_0.005_0.05_40"]
    
    # folder_suff = "poltics_names_allDocs"
    # run_suff = "_politics_names_allDocs"
    # max_it = 500
    # nr_runs = 100
    # case_names = ["politics_names_allDocs_o2_hub2_0.005_0.05_40","politics_names_allDocs_o0_hub2_0.005_0.05_40","politics_names_allDocs_o2_hub_random2_0.005_0.05_40"]
    
    labels = ["Plain","No context", "Random context"]
    for c in case_names:
        print(c)
    # colors = ["Aqua", "Blue",  "DodgerBlue"]
    colors = ["Red", "Blue",  "Green"]
    # colors = ["Crimson", "DarkViolet",  "DarkBlue"]
    best_runs = comparisons(case_names, colors, labels, suffix = run_suff, max_iter=max_it, round_vals=True, average=True, nr_runs=nr_runs, folder_suffix=folder_suff)

    nr_cats = 6
    f_out = open(r"D:\Users\Lydia\results_nn"+"\\"+folder_suff+r"\best_run_overview.txt","w")
    for i in range(len(case_names)):
        print(case_names[i], "best run", best_runs[i])
        case_name = case_names[i]+"_run"+str(best_runs[i])
        confusion_matrix(case_name, nr_cats, "validation", folder_suffix = folder_suff, name_suffix=labels[i]+"_val")
        confusion_matrix(case_name, nr_cats, "test", folder_suffix = folder_suff, name_suffix=labels[i]+"_test")
        acc_graph(case_name, folder_suffix = folder_suff)
        f_out.write(labels[i]+", "+str(best_runs[i])+"\n")
        
    f_out.close()
    
    
    

if __name__ == "__main__":
    
    line_thickness = 1
    nr_columns = 2
    fontsize = 9
      
    comparison_politics_names()
    
    # final_comparison_input_settings()
    
    # case_names = ["politics_lim_ns_swrem_whole_o2_logas_hub_5bins_tz_0.005_0.05_40", "politics_lim_ns_swrem_whole_o2_logas_5bins_tz_timeind_0.005_0.05_40", "politics_lim_ns_swrem_whole_o2_logas_5bins_tz_0.005_0.05_40", "politics_lim_ns_swrem_whole_o0_logas_5bins_tz_0.005_0.05_5", "politics_lim_ns_random_swrem_whole_o2_logas_5bins_tz_0.005_0.05_40", "politics_lim_ns_swrem_whole_o2_logas_hub_5bins_tz_timeind_0.005_0.05_40"]
    # labels = ["Hub", "Time indication", "Plain", "No context", "Random context", "Hub and time indication"]
    # for c in case_names:
        # print(c)
    # colors = ["r", "g", "b", "m", "y", "c"]
    # comparisons(case_names, colors, labels, suffix = "_data_settings")
    
    # case_names = ["optimize_politics_o2_0.005_0.03 60", "optimize_politics_o2_0.005_0.03 80", "optimize_politics_o2_0.005_0.05 60", "optimize_politics_o2_5.0E-4_0.03 60", "optimize_politics_o2_5.0E-4_0.03 80"]
    # labels = ["a=0.005 m=0.03 nh=60", "a=0.005 m=0.03 nh=80", "a=0.005 m=0.05 nh=60", "a=0.0005.0 m=0.03 nh=60", "a=0.0005 m=0.03 nh=80"]
    # for c in case_names:
        # print(c)
    # colors = ["r", "g", "b", "m", "y"]
    # print(len(case_names),len(labels),len(colors))
    # comparisons(case_names, colors, labels, suffix = "_param_settings")
    
    # case_names = ["optimize2_politics_o2_0.005_0.03 40", "optimize2_politics_o2_0.005_0.03 60", "optimize2_politics_o2_0.005_0.03 80", "optimize2_politics_o2_5.0E-4_0.03 40","optimize2_politics_o2_5.0E-4_0.03 60","optimize2_politics_o2_5.0E-4_0.03 80","optimize2_politics_o2_5.0E-4_0.005 40","optimize2_politics_o2_5.0E-4_0.005 60","optimize2_politics_o2_5.0E-4_0.005 80"]
    # labels = ["a=0.005 m=0.03 nh=40", "a=0.005 m=0.03 nh=60", "a=0.005 m=0.03 nh=80", "a=0.0005 m=0.03 nh=40", "a=0.0005 m=0.03 nh=60","a=0.0005 m=0.03 nh=80", "a=0.0005 m=0.005 nh=40","a=0.0005 m=0.005 nh=60","a=0.0005 m=0.005 nh=80"]
    # for c in case_names:
        # print(c)
    '''colors = ["Aqua", "Blue", "DodgerBlue", "Green", "LawnGreen", "YellowGreen", "Gold", "FireBrick","Orange"]'''
    # colors = ["Aqua", "Blue", "BlueViolet", "Green", "DeepPink", "GreenYellow", "Black", "Red","Orange"]
    # print(len(case_names),len(labels),len(colors))
    # comparisons(case_names, colors, labels, suffix = "_param_settings2", round_vals=True)
    
    # case_names = ["politics_lim_ns_swrem_whole_o2_logas_5bins_tz_0.005_0.05_40","politics_lim_ns_random_swrem_whole_o2_logas_5bins_tz_0.005_0.05_40","politics_lim_ns_swrem_whole_o0_logas_5bins_tz_0.005_0.05_5","politics_lim_ns_swrem_whole_o2_logas_hub_5bins_tz_0.005_0.05_40","politics_lim_ns_swrem_whole_o2_logas_5bins_tz_timeind_0.005_0.05_40","politics_lim_ns_swrem_whole_o2_logas_hub_5bins_tz_timeind_0.005_0.05_40","politics_lim_ns_swrem_whole_o3_logas_5bins_tz_0.005_0.05_40","politics_lim_ns_swrem_whole_o2_logas_5bins_tz_tarenc10_0.005_0.05_40","politics_lim_ns_swrem_whole_o2_logas_5bins_tz_tarenc5_0.005_0.05_80"]
    # labels = ["Plain","No context", "Random context", "Hub", "Time indication", "Hub and time indication",  "Window size 7",  "Target encoding 5 bin", "Target encoding 10 bin"]
    # for c in case_names:
        # print(c)
    # colors = ["Black", "Green", "LawnGreen", "Aqua", "Blue",  "DodgerBlue","BlueViolet", "FireBrick","Orange"]
    # comparisons(case_names, colors, labels, suffix = "_data_settings2", max_iter=50, round_vals=True)