import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import thesis_utilities

folder_puzz = r"D:\Users\Lydia\results puzzle"
folder_cooc = r"D:\Users\Lydia\results word cooc"

fontsize = 20
name_size = 7
fig_size = 10

def get_party_color():
    result = {}
    
    result["vvd"]="Aqua"
    result["pvda"]="Blue"
    result["sp"]= "Red"
    result["cda"]="Chartreuse"
    result["d66"]="DarkGreen"
    result["pvv"]= "DarkSeaGreen"
    result["christenunie"]= "SaddleBrown"
    result["groenlinks"]="DarkOrange"
    result["sgp"]= "LightGrey"
    result["pvdd"]= "BlueViolet"
    result["50plus"]="DarkSlateBlue"
    
    return result

def set_font(ax):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]+ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(fontsize)

def check_landscape(case_name_puzz, case_name_cooc, landscape_size):
    
    landscape = thesis_utilities.grid_from_file(folder_puzz+"\\"+case_name_puzz+r"\grid_final.txt")
    party_names = thesis_utilities.get_name_club_link(folder_cooc+"\\"+case_name_cooc+r"\names_parties.csv")
    party_color = get_party_color()
    
    fig, ax = plt.subplots(1)       
    fig.set_figheight(fig_size)
    fig.set_figwidth(fig_size)
    
    for ir in range(landscape_size):
        i = landscape_size-ir-1
        for j in range(landscape_size):
            name = landscape[ir][j]
            # print(name)
            if name != None:
                name_disp = name.split("_")[-1]
                ax.text(j*name_size+0.2, i+0.5, name_disp, color="White",fontsize=fontsize, bbox=dict(facecolor=party_color[party_names[name]], edgecolor="White"))
    ax.set_xlim([0,name_size*landscape_size])
    ax.set_ylim([0,landscape_size+1])
    plt.show()
    
    # image_name = folder + "\\"+case_name + "\\"+ legend[i+1]  +"_" + title_case_name + ".pdf"
    # fig.savefig(image_name, bbox_inches='tight')
    # image_name = folder + "\\"+case_name + "\\"+ legend[i+1]  +"_" + title_case_name + ".png"        
    # fig.savefig(image_name, bbox_inches='tight')
    # plt.close()
    
if __name__ == "__main__":
    
    case_name_cooc = "politics_names"
    # case_name_puzz = "politics_names_result"
    case_name_puzz = "politics_names_RANDOM"
    landscape_size = 11
    
    check_landscape(case_name_puzz, case_name_cooc, landscape_size)