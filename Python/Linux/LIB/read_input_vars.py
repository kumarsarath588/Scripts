#!/usr/bin/python

import sys,re
global INPUTVARS;
INPUTVARS = {};

# -*-Reading Input variables.
def read_input_vars():
        if (len(sys.argv) >= 2):
                for arg in sys.argv:
                        matchObj = re.match( r'(.*)=(.*)', arg, re.M|re.I)
                        if matchObj:
                                INPUTVARS[matchObj.group(1)]= matchObj.group(2);
	return INPUTVARS	
