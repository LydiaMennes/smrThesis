import sys
import os
lib_path = r"K:\Lydia\smrThesis\code\code_first_run_words\libsvm-3.19\python"
sys.path.append(lib_path)
lib_path2 = r"K:\Lydia\smrThesis\code\code_first_run_words\libsvm-3.19\windows"
# sys.path.append(lib_path2)
code_dir = r"K:\Lydia\smrThesis\code\code_first_run_words"

os.chdir(lib_path)
from svmutil import *
os.chdir(code_dir)




if __name__ == "__main__":
    print("hello world")