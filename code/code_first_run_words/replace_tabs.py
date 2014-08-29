
def replace_tabs(filename, file_out):
    f_in = open(filename, 'r')
    f_out = open(file_out, 'w')
    for line in f_in:
        line = line.replace("\t", "    ")
        f_out.write(line)
    f_in.close()
    f_out.close()

if __name__ == "__main__":
    name_in = r"K:\Lydia\smrThesis\code\code_first_run_words\freqs_landscape.py"
    name_out = r"K:\Lydia\smrThesis\code\code_first_run_words\freqs_landscapeN.py"
    replace_tabs(name_in, name_out)