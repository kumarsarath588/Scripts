#!/usr/bin/python

import sys
import time
import select
import paramiko

class connect_to_machine:
   """
   This class 'connect_to_machine' used to connect to machine to take ssh connection
   you need to choose appropriate methid in 'connect_to_machine' depending on type,
   of host you want to connect either to 'ec2' instance or physical machine.
   """

   def __init__(self, INPUTS, host):
        self.host = host
        self.user = INPUTS['config']['user']
        self.key = INPUTS['config']['key']
   def connect_to_ec2(self):
	i = 0
	while True:
	    #print "Trying to connect to %s (%i/120) " % (self.host, i)
	    try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(self.host,username=self.user, key_filename=self.key)
		print "Connected to %s" % self.host
		break
	    except paramiko.AuthenticationException:
		print "Authentication failed when connecting to %s" % self.host
		sys.exit(1)
	    except:
		print "Could not SSH to %s, waiting for it to start" % self.host
		i += 5
		time.sleep(5)

	    # If we could not connect within time limit
	    if i == 120:
		print "Could not connect to %s. Giving up" % self.host
		sys.exit(1)
        return ssh 	
