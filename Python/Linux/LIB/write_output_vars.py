from logw import logw
def write_output_vars(OUTPUTVARS):
	logw('Printing Output Variables in Shell 2 Format',1)
        for VAR in OUTPUTVARS.keys():
          OUTSTR = str(VAR) + "=" + str(OUTPUTVARS[VAR])
          print OUTSTR;

