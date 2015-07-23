#!/usr/bin/python
# *** INFOSTART ***
#
# Script Name   : MSAP_AUTOMATION_LIB_10004.py
# Version       : 1.1
# Description   : Library to be used for MSAP Scripting - Python Scripts
# Written By    : Sarath Kumar.K (sk109342)
# Written Date  : 25-OCT-2013
# Modified By   : Sarath Kumar.K (sk109342)
# Modified Date : 06-NOV-2013
# Compatibility : Shell 1 & 2
# Dependencies  : sys,os.path,re,time
# Usage:
#	import MSAP_AUTOMATION_LIB_10004
import sys,os.path,re,time;

# -*- Declaring global variables.
global LOGF,INPUTVARS,OUTPUTVARS,logw,check_sfb,open_logf,read_input_vars,exit_script,DEFAULT_DELIM,SHELLV,DEFAULT_SFB,MIS_VARS,SFB;

DEFAULT_DELIM='#@#';
SFB='';
DEFAULT_SFB=0;
DEFAULT_SHELLV=2;

INPUTVARS = {};
OUTPUTVARS = {};
OUTPUTVARS['RETCODE']=0;
OUTPUTVARS['RETDESC']="Script Executed.";


# -*- Subroutine for writing a log message to a log file with the type and timestamp
# -*- The arguments are log message and type of the message
# -*- 1 - INFO
# -*- 2 - WARN
# -*- 3 - ERROR
# -*- 4 - START
# -*- 5 - END
# -*- Any other type will be logged as UNKNOWN
# -*- This sub routine requires log file to be opened by open_logf function before this is called
def logw(LOG_MSG,LOGT):
	LOG_STR=""
	if (LOGT==1):
		LOG_STR='[ INFO    ] '
	elif (LOGT==1):
                LOG_STR='[ INFO    ] '
	elif (LOGT==2):
                LOG_STR='[ WARN    ] '
	elif (LOGT==3):
                LOG_STR='[ ERROR   ] '
	elif (LOGT==4):
                LOG_STR='[ START   ] '
	elif (LOGT==5):
                LOG_STR='[ END     ] '
	else:
                LOG_STR='[ UNKNOWN ] '
	LOG_STR=LOG_STR+time.strftime("%c")+"  "+ LOG_MSG+'\n'
	LOGF.write(LOG_STR)

# -*- Creating log directory and log file.
## Returning the values when sript is sucessful is left.
def open_logf():
	global LOGF
	LOGF=0;
	Today=(time.strftime("%d-%m-%Y"))
	LOG=sys.path[0]+'/LOG'
	LOGDIR=LOG+'/'+Today
	if ( not os.path.exists(LOG)):
		os.makedirs(LOG)	
	if ( not os.path.exists(LOGDIR)):
		os.makedirs(LOGDIR)
	Scriptname= re.match( r'(.+)\.(.+)',sys.argv[0], re.M|re.I)
	if Scriptname:
		LOGFILE = LOGDIR+'/'+Scriptname.group(1)+'.log'
		if (not os.path.isfile(LOGFILE)):
			file(LOGFILE, 'w')
	LOGF=open(LOGFILE, 'a')
	logw("*** Script Execution Started ***",4);
	return 0;

# -*- Subroutine to check the SFB (Send AGS FeedBack) status of the script and update the SFB variable
# -*- This sets the SFB variable depending on the SFB variable got from the input 
# -*- or from the DEFAULT_SFB variable
def check_sfb():
	if 'SFB' in INPUTVARS.keys():
		matchobj=re.match( r'(\d+)', INPUTVARS['SFB'], re.M|re.I)
		if matchobj:
			if (matchobj.group(1)!=0):
				logw('Send AGS Feedback Enabled',1)
				return 1;
		elif(DEFAULT_SFB !=0):
                        logw('Send AGS Feedback Enabled',1)
			return 1;
	elif(DEFAULT_SFB != 0):
		logw('Send AGS Feedback Enabled',1)
		return 1;
	logw('Send AGS Feedback Disabled',1);
	return 0;
	
# -*-Reading Input variables.
def read_input_vars():
	global SFB;
	global SHELLV;
	if (len(sys.argv) >= 2):
		for arg in sys.argv:
			matchObj = re.match( r'(.*)=(.*)', arg, re.M|re.I)
			if matchObj:
				INPUTVARS[matchObj.group(1)]= matchObj.group(2);
	# -*- Checking the shell version 1 or 2
	if 'SHELLV' in INPUTVARS.keys():
		INPUT_SHELLV=INPUTVARS['SHELLV'];
		if (INPUT_SHELLV == 1):
				SHELLV=1;
				logw ('Shell Version 1',1);
				return SHELLV;
		elif(DEFAULT_SHELLV == 1):
				SHELLV=1;
                                logw ('Shell Version 1',1);
                                return SHELLV;
	elif(DEFAULT_SHELLV == 1):
        	SHELLV=1;
                logw ('Shell Version 1',1);
                return SHELLV;
	SHELLV=2;
        logw ('Shell Version 2',1);
	SFB=check_sfb()
	return SHELLV;

# -*- Subroutine to send AGS feedback
# -*- Prints the feedback message in required format to the STDOUT
# -*- only if the SFB value is set to 1
# -*- This will also log the feedback message

def send_ags_feedback(INPUT1,INPUT2,INPUT3):
	if( SFB == 1 and SHELLV != 1 ):
		FB='\$AGSFeedback -progress ' + str(INPUT1) + ' -error ' + str(INPUT2) + ' -message \"';
		if (INPUT2 == 0 ):
			FB= FB+'<font color=\'green\'>'+ INPUT3 +'</font>';
		else:
			FB=FB+'<font color=\'red\'>'+ INPUT3 +'</font>';
		FB=FB+'\"';
		logw(FB,1);
		print FB;


# -*- Exit point for the script
# -*- Sets the RETDESC and RETCODE Output variables
# -*- Prints the given string to log and exit with the given exit code
# -*- This also write the output variables to the STDOUT
def exit_script(EXIT_STR,EXIT_CODE):
	OUTPUTVARS['RETDESC']=EXIT_STR
	OUTPUTVARS['RETCODE']=EXIT_CODE
	write_output_vars()
	logw(EXIT_STR,1 )
	logw('Script exiting with : '+str(EXIT_CODE),1)
	logw('*** Script Execution Completed ***',5)
	LOGF.close()
	sys.exit(str(EXIT_CODE));

# -*- Subroutine to write the output variables to the STDOUT
# -*- Writes the variables in Shellv1 or 2 format depending on the SHELLV variable
# -*- The arguments will be written from a dictionary - OUTPUTVARS
# -*- The delimiter used for Shell v1 will be taken from DELIM variable read from the command line input
# -*- or from the DEFAULT_DELIM variable
# -*- Each line with one variable will be printed in case of Shell V2
def write_output_vars():
	if (SHELLV==1):
		logw('Printing Output Variables in Shell 1 Format',1)
		if 'DELIM' in INPUTVARS.keys():
			if (INPUTVARS['DELIM'] != ""):
				DELIM=INPUTVARS['DELIM']
			else:
				DELIM=DEFAULT_DELIM	
		else:
			DELIM=DEFAULT_DELIM
		OUTSTR=""
		for VAR in OUTPUTVARS.keys():
			OUTSTR = str(OUTSTR) + str(VAR) + "=" + str(OUTPUTVARS[VAR]) + str(DELIM)
		print OUTSTR;
	else:
		logw('Printing Output Variables in Shell 2 Format',1)
		for VAR in OUTPUTVARS.keys():
			OUTSTR = str(VAR) + "=" + str(OUTPUTVARS[VAR])
			print OUTSTR;

# -*- Subroutine to check whether the mandory variables exist and not empty
# -*- If one or more variables do not exists or empty then this will return the
# -*- comma seperated variable names
# -*- If all the variables exists and if they are not empty then this will return an empty string
def check_mandatory_vars(Mandatory_vars):
	str= Mandatory_vars.split(',')
	MIS_VARS=""
	for var in str:
		if var in INPUTVARS.keys():
			if (INPUTVARS[var] != ""):
				logw('Variable \"' + var + '\" exist and not empty.',1)
			else:
				logw('Variable \"' + var + '\" is empty.',3)
				MIS_VARS=MIS_VARS + var + ','
		else:
			logw('Variable \"' + var + '\" does not exist.',3)
			MIS_VARS= MIS_VARS + var + ','
	# -*- Remove last comma(,).
	matchOb = re.match( r'^(.*),$', MIS_VARS , re.M|re.I)
	if matchOb:
		MIS_VARS=matchOb.group(1)
	return MIS_VARS

1;

