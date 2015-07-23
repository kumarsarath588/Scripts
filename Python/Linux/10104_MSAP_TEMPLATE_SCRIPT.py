# *** INFOSTART ***
#
# Script Name   : 10104_MSAP_TEMPLATE_SCRIPT.py
# Version       : 1.0
# Description   : Template script for MSAP Scripting - Python Script ( using Library 10004 )
# Written By    : Sarath Kumar.K (sk109342)
# Written Date  : 6-Nov-2013
# Compatibility : Shell 1.0 & 2.0
# 
# *** INFOEND ***

# -*- Adding library file to sys.path and using MSAP Automation library 10004.
import sys
LIB_DIR=sys.path[0]+'/LIB/'
sys.path.append(LIB_DIR)

import MSAP_AUTOMATION_LIB_10004

# -*- Subroutine to exit script after printing the mandatory.
# -*- variables RETCODE and RETDESC.
# -*- This should be used only if library is missing or if logging has failed.
# -*- Values for RETDESC and RETCODE should be passed as arguments.
def error_exit(ERRMSG,ERRCODE):
	print 'RETCODE=' + str(ERRCODE) + '#@#RETDESC=' + str(ERRMSG);
	print 'RETCODE=' + str(ERRCODE);
	print 'RETDESC=' + ERRMSG;
	sys.exit(str(ERRCODE));

# -*- This is to send STD error or STD output to null or make it without appearing.
f = open('/dev/null', 'w')
#sys.stdout = f
sys.stderror = f

# -*- Opening Logfile.
LOG_STATUS=MSAP_AUTOMATION_LIB_10004.open_logf();
if (LOG_STATUS != 0):
	error_exit('Error while opening Log file.',1);

# -*- Reading the input arguments.
MSAP_AUTOMATION_LIB_10004.read_input_vars()

# -*- Checking whether the mandatory arguments exists and are not empty.
VAR_STATUS=MSAP_AUTOMATION_LIB_10004.check_mandatory_vars("RTRIP,DELIM")# -*- Should be replaced with the actual arguments.
if (VAR_STATUS != ''):
	MSAP_AUTOMATION_LIB_10004.exit_script('Arguments "' + VAR_STATUS + '" missing or empty.',1)

# -*- Test Code Should be repalced with your actual code.
for var in MSAP_AUTOMATION_LIB_10004.INPUTVARS.keys():
	MSAP_AUTOMATION_LIB_10004.OUTPUTVARS[var]=MSAP_AUTOMATION_LIB_10004.INPUTVARS[var]
	MSAP_AUTOMATION_LIB_10004.send_ags_feedback(50,0,'Processing ' + var);

# -*- Exiting the script after writing the output variables.
MSAP_AUTOMATION_LIB_10004.exit_script ('Script Completed Successfully.',0);

