
import sys,os.path,re,time;
# -*- Creating log directory and log file.
## Returning the values when sript is sucessful is left.
def open_logf():
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
        return 0;
