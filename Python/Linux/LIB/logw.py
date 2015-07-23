
import sys,os.path,re,time;

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
        Today=(time.strftime("%d-%m-%Y"))
        LOG=sys.path[0]+'/LOG'
        LOGDIR=LOG+'/'+Today
        Scriptname= re.match( r'(.+)\.(.+)',sys.argv[0], re.M|re.I)
        LOGFILE = LOGDIR+'/'+Scriptname.group(1)+'.log'
        LOGF=open(LOGFILE, 'a')

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

