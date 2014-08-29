import math
from collections import defaultdict
import random
import matplotlib.pyplot as plt
from thesis_utilities import *
import os
import datetime
import sys

class nameBox:
	def __init__(self, name, color, blob_nr):
		self.name = name
		self.blob_nr = blob_nr
		self.color = color

def print_grid(grid):
	print("grid")
	for i in range(len(grid[0])):
		for j in range(len(grid)):
			print(grid[j][i], end = "")
		print("")
		
def grid_figures(output_directory, new_grid, grid_size, iter, fig_nr=None, suffix=""):
	image_name = output_directory + r"\space_to_grid_new" + suffix	
	fig = plt.figure(figsize=(8,8))
	for i in range(grid_size):
		for j in range(grid_size):
			if new_grid[i][j]!=None:
				plt.plot(j, grid_size-1-i, c=new_grid[i][j][1], marker='.')				
	plt.axis([-1,grid_size+1, -1, grid_size+1])
	plt.title("BLOB TEST")
	fig.savefig(image_name+str(iter)+".pdf", bbox_inches='tight')
	if fig_nr!=None:
		fig.savefig(image_name+four_digit_string(fig_nr)+".png")
	plt.close()
		
def space_to_grid(grid, color_list, nr_words, output_directory_s, old_grid_size):
    output_directory = output_directory_s+r"\intermediate_grids"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)	
        print("directory made")	
        
    new_grid = defaultdict(lambda: defaultdict(lambda: None))

    grid_size = math.ceil(math.sqrt(nr_words))
    ratio =grid_size/old_grid_size
    shift_resize =ratio/2
    # shift_resize = 0
    grid.append([0]*len(grid[0]))
    colors = {}
    print("old_grid_size", old_grid_size, "grid_size", grid_size)
    print("old_nr_words", len(grid[0]), "new nr words", nr_words)

    elems_found = 0
    empty_blobs = 0
    for i in reversed(range(len(grid[0]))):
        grid[0][i]= math.floor(grid[0][i]*ratio+shift_resize)
        grid[1][i]= math.floor(grid[1][i]*ratio+shift_resize)		
        grid[4][i]=1
        colors[grid[2][i]]= color_list[i%len(color_list)]
        new_grid[grid[0][i]][grid[1][i]] = (grid[2][i], colors[grid[2][i]], i)	
        elems_found+= len(grid[3][i])
        if len(grid[3][i])==0:
            print("empty blobbieblob")
            empty_blobs+=1
            for j in range(len(grid)):
                del grid[j][i]

    iter = 0
    fig_nr = 0
    nr_to_be_added=nr_words - len(grid[0])-empty_blobs
    count = 0
    print("nr of blobs", len(grid[0]),"2b added", nr_to_be_added, "nr actually found", elems_found)
    while len(grid[0])>0:
        elem_index = random.randrange(nr_to_be_added)
        blob = 0
        words_seen = 0
        # print("nr blobs:", len(grid[0]))
        # print("elem_index", elem_index)
        while words_seen + len(grid[3][blob]) <= elem_index:
            # print("current blob", blob,"current_words seen", words_seen)
            words_seen += len(grid[3][blob])
            blob += 1	
            if blob == len(grid[0]):
                print("Out of grid bound. words seen:", words_seen, "elem_index", elem_index, "last length", len(grid[3][blob-1]))
                sys.exit()
		# print("current blob", blob)
		# print("current_words seen", words_seen)
        word_nr = elem_index - words_seen
        # print("word_nr", word_nr)
        word = grid[3][blob][word_nr]
        blob_row = grid[0][blob]
        blob_col = grid[1][blob]			
		
        added = False
        while not added:
            size = grid[4][blob]
            for i in range(-size,size+1):
                for j in [-size, size]:
                    if not added:
                        if blob_row+i >=0 and blob_row+i<grid_size and blob_col+j>=0 and blob_col+j<grid_size:
                            if new_grid[blob_row+i][blob_col+j] == None:
                                added = True
                                new_grid[blob_row+i][blob_col+j]=(word, colors[grid[2][blob]], blob)
								# print("added to", blob_row+i, blob_col+j, "blob nr", blob)
                        if blob_row+j >=0 and blob_row+j<grid_size and blob_col+i>=0 and blob_col+i<grid_size and not added:
                            if new_grid[blob_row+j][blob_col+i] == None:
                                added = True
                                # print("added to", blob_row+j, blob_col+i)
                                new_grid[blob_row+j][blob_col+i]=(word, colors[grid[2][blob]], blob)
            if added:
                nr_to_be_added -= 1
                del grid[3][blob][word_nr]
                if len(grid[3][blob])==0:
                    for i in range(len(grid)):
                        del grid[i][blob]
            else:
                grid[4][blob]+=1
                if grid[4][blob] == grid_size:
                    print("fatal not found. Grid_size:", grid_size,"words",nr_words)
                    sys.exit()
		
        iter+=1

        if iter%500 == 0 or iter==1:
            print(iter, datetime.datetime.now())
            grid_figures(output_directory, new_grid, grid_size, iter, fig_nr)
            fig_nr+=1

    print("transform final grid")
    grid_figures(output_directory, new_grid, grid_size, "final", fig_nr)
    for i in range(grid_size):
        for j in range(grid_size):
            if new_grid[i][j] != None:
                new_grid[i][j] = nameBox(new_grid[i][j][0], new_grid[i][j][1], new_grid[i][j][2])	
    print("DONE")
    grid_to_file(output_directory_s, grid_size, "from_stg_process.txt", new_grid)
	
    return new_grid
							
if __name__ == "__main__":
	print("NOTHING HERE DUDE")