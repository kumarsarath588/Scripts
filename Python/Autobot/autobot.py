#!./venv/bin/python

import boto.ec2
import yaml
import time
import os.path
import sys
from ec2_creation import ec2_creation
from execute_ssh_comand import execute_ssh_command
from execute_copy import execute_copy
from connect_ec2 import create_ec2_connection

def mandatory_items(path,items):
    for item in items:
      if not path[item]:
         print "Error: mandatory item '%s' not found" % str(item)


fname='config.yml'

if not os.path.isfile(fname):
   print "Error: config file 'config.yml' not found"
   sys.exit(1)

with open('config.yml', "r") as yaml_file:
        INPUTS=yaml.load(yaml_file)

conn=''
#man=['']
#if not INPUTS['name'] or not INPUTS['config'] or not INPUTS['config']['provider']:
 
try:
   INPUTS['name']
   INPUTS['config']
   INPUTS['config']['provider']
except KeyError:
   print "Error: define 'name/config/provider' in 'config.yml'"
   sys.exit(1)
if INPUTS['config']['provider'] == 'ec2':
   conn=create_ec2_connection(INPUTS)
   ec2=ec2_creation(INPUTS,conn)
   status=ec2.create_ec2_instance()
   if INPUTS['config']['operation']['type'] == 'script':
      if not INPUTS['config']['operation']['file']:
         print "Error: for operation type 'script' file variable is mandatory"
      else:
         if not os.path.isfile(INPUTS['config']['operation']['file']):
            print "Error: script file '%s' not found" % INPUTS['config']['operation']['file']
         else:
            copy=execute_copy(INPUTS, status[0].instances[0].ip_address)
            copy.copy()
            ssh=execute_ssh_command(INPUTS, status[0].instances[0].ip_address)
            ssh.execute_command()
   else:
      print 'Error: Invalid operation \'%s\'', INPUTS['config']['operation']['type']
   ec2.terminate_ec2_instance(id=status[0].instances[0].id)
elif INPUTS['config']['provider'] == 'ssh':
   print "ssh"
else:
   print 'Error: Invalid provider \'%s\'', INPUTS['config']['provider']
