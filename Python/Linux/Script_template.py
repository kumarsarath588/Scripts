#!/usr/bin/python
import sys
from LIB import *

INPUTVARS = {};
OUTPUTVARS = {};

def exit_script(EXIT_STR,EXIT_CODE):
        OUTPUTVARS['RETDESC']=EXIT_STR
        OUTPUTVARS['RETCODE']=EXIT_CODE
        write_output_vars(OUTPUTVARS)
        logw(EXIT_STR,1 )
        logw('Script exiting with : '+str(EXIT_CODE),1)
        logw('*** Script Execution Completed ***',5)
        sys.exit(str(EXIT_CODE));

LOG_STATUS=open_logf();
if (LOG_STATUS != 0):
        exit_script('Error while opening Log file.',1);

logw("*** Script Execution Started ***",4);


INPUTVARS=read_input_vars()

for k in INPUTVARS.keys():
  	OUTPUTVARS[k]=INPUTVARS[k]

exit_script('over',10)
