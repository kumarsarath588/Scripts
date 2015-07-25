#!/usr/bin/python

import paramiko
from connect_to_machine import connect_to_machine

class execute_copy:
   def __init__(self, INPUTS, host):
        self.host = host
        self.user = INPUTS['config']['user']
        self.key = INPUTS['config']['key']
        self.file = INPUTS['config']['operation']['file']
        self.ssh_class = connect_to_machine(INPUTS,self.host)

   def copy(self):
   	self.ssh = self.ssh_class.connect_to_ec2()
        sftp = self.ssh.open_sftp()
        sftp.put(self.file,'/tmp/'+self.file)
  	sftp.close()
	print "copied successfully!" 
 	self.ssh.close()
