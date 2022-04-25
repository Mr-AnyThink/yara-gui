import re
import os

CWD = os.path.dirname(os.path.realpath(__file__)) #Find current working directory
yaraIndex = open(CWD + "/rules/index.yar", "rt")
# the output file which stores result
yaraActiveIndex = open(CWD + "/rules/active_index.yar", "wt")
# iteration for each line in the input file
for line in yaraIndex:
	# replacing the string and write to output file
    error = re.findall('.*MALW_AZORULT.*',line)
    if len(error) == 0:
	    yaraActiveIndex.write(line.replace('./', CWD + "/rules/"))
#closing the input and output files
yaraIndex.close()
yaraActiveIndex.close()