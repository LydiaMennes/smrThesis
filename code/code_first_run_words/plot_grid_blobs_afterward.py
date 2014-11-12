from thesis_utilities import *
import sys
import matplotlib.pyplot as plt

figure_size = 5
fontsize = 9

def set_font(ax):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]+ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(fontsize)

def get_blobs(blob_file):
    f = open(blob_file)
    blobs = []
    for line in f:
        line=line.replace("\n","")
        line = line.split(" ")
        del line[2]
        del line[0]
        blobs.append(line)
    f.close()
    return blobs
    
def get_blob_nr(word, blobs):
    index = 0
    for blob in blobs:
        if word in blob:
            return index
        index+=1
    print("unfound word-"+ word+"-")
    print("-"+blobs[46][-1]+"-")
    sys.exit()

def plot_grid_afterwards(landscape_file, size, blob_file, used_marker, title, suffix = ""):
    grid = grid_from_file(landscape_file)
    blobs = get_blobs(blob_file)
    colors = get_colors()
    ticks = []
    
    fig, ax = plt.subplots(1) 
    fig.set_figheight(figure_size)
    fig.set_figwidth(figure_size)
    for i in range(size):
        y = size-i-1
        for x in range(size):
            word = grid[i][x]
            if word != None:                
                blob_nr = get_blob_nr(word, blobs)        
                if x==0 and y<10:
                    print(word, blob_nr)
                prop_plot=ax.scatter( x, y, c=colors[blob_nr%len(colors)], marker=used_marker)
                prop_plot.set_edgecolor("none")
        
    ax.axis([-1, size, -1, size])
    ax.set_title(title)
    plt.xticks(ticks)
    plt.yticks(ticks)
    set_font(ax)
    image_name = folder+"\\"+title.replace(" ", "_")+"_"+suffix+".pdf"
    fig.savefig(image_name, bbox_inches='tight')
    plt.close()  
                
    
            
    
if __name__ == "__main__":
    landscape_folder = r"D:\Users\Lydia\results puzzle"

    folder = r"D:\Users\Lydia\figures_landscape"
    size = 90
    # large or small
    marker = "."
    
    figure_size = 5
    fontsize = 9
    
    title = "Initialized grid"
    suff = "pol_lim_ns_normal"
    case_name = "politics_limit1000_no_stem"
    landscape_file_case_name = landscape_folder+"\\"+case_name+r"\grid_initial.txt"
    blob_file_case_name = landscape_folder+"\\"+case_name+r"\blob_file.txt"
    
    plot_grid_afterwards(landscape_file_case_name, size, blob_file_case_name, marker, title, suffix=suff)
    
    title = "Result after puzzle"
    suff = "pol_lim_ns_normal"
    case_name = "politics_limit1000_no_stem"
    landscape_file_case_name = landscape_folder+"\\"+case_name+r"\grid_final.txt"
    blob_file_case_name = landscape_folder+"\\"+case_name+r"\blob_file.txt"
    
    plot_grid_afterwards(landscape_file_case_name, size, blob_file_case_name, marker, title, suffix=suff)
    
    
    title = "Initialized grid"
    suff = "pol_lim_ns_stripy"
    case_name = "politics_limit1000_no_stem_stripy"
    landscape_file_case_name = landscape_folder+"\\"+case_name+r"\grid_initial.txt"
    blob_file_case_name = landscape_folder+"\\"+case_name+r"\blob_file.txt"
    
    plot_grid_afterwards(landscape_file_case_name, size, blob_file_case_name, marker, title,suffix=suff)
    
    
    size = 172
    title = "Initialized grid"
    suff = "pol_big"
    case_name = "politics_big_stem"
    landscape_file_case_name = landscape_folder+"\\"+case_name+r"\grid_initial.txt"
    blob_file_case_name = landscape_folder+"\\"+case_name+r"\blob_file.txt"
    
    plot_grid_afterwards(landscape_file_case_name, size, blob_file_case_name, marker, title,suffix=suff)
        
    
    
    
    