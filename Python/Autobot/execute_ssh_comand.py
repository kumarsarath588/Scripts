#!/usr/bin/python

import boto.ec2
import sys
import select
import paramiko
from connect_to_machine import connect_to_machine 

class execute_ssh_command:
   def __init__(self, INPUTS, host):
	self.host = host
        self.user = INPUTS['config']['user']
        self.key = INPUTS['config']['key']
  	self.ssh_class = connect_to_machine(INPUTS,self.host)

   def execute_command(self):
        self.ssh = self.ssh_class.connect_to_ec2()
	stdin, stdout, stderr = self.ssh.exec_command("sudo /bin/bash /tmp/script.sh", get_pty=True)
        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_exit_status() != 0:
               self.ssh.close()
               print "Error: " + str(stderr.readlines()) + ' stdout ' + str(stdout.readlines()) + ' exitcode ' + str(stdout.channel.recv_exit_status())
               sys.exit(1)
            else:
                if stdout.channel.recv_ready():
                   rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                   if len(rl) > 0:
                      # Print data from stdout
                       print stdout.channel.recv(1024),

        # Disconnect from the host
        print "Command done, closing SSH connection"
        self.ssh.close()

