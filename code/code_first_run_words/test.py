from __future__ import division
import datetime
import string
import sys

from pympler import summary
from pympler import muppy

	
def get_frequencies():

	lists = []
	for i in range(1000):
		lists.append([1,2,3])
		if i%500==0:
			print("\n\n=====")
			all_objects = muppy.get_objects()
			sum1 = summary.summarize(all_objects)
			s = summary.print_(sum1)
			print(type(s))

	
if __name__ == "__main__":
	old_stdout = sys.stdout
	try:
		mem_file = open("TEST_log.txt","w")
		sys.stdout = mem_file
		get_frequencies()
	finally:
		sys.stdout = old_stdout
		mem_file.close()