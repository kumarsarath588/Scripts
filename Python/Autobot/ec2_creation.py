#!/usr/bin/python

import boto.ec2
import sys
import time
from boto.ec2.instancestatus import InstanceStatusSet

class ec2_creation:

   def __init__(self, INPUTS, conn):
	self.ami = INPUTS['config']['ami']
	self.key = INPUTS['config']['keyname']
	self.sg  = 'default'
	self.ins = 't1.micro'
	self.conn=conn
   def create_ec2_instance(self):
	"""
	Create intance in given region based on instance information/ami id
	"""
	print 'Info: The instance which you wanted to create is \'' + self.ami + '\' using key pair \'' + self.key + '\' and with \'' + self.sg + '\' security group'
        try:
	    reservations = self.conn.run_instances(self.ami,key_name=self.key,instance_type=self.ins,security_groups=[self.sg])
       	    print 'Info: Created instance \'%s\'' % reservations.instances[0].id
        except:
            print 'Error: Not able to create instance with ami id: %s' % self.ami
            sys.exit(1)
	clock = 0
	status=''
        while True:
           try:
              status = self.conn.get_all_reservations(instance_ids=reservations.instances[0].id)
           except:
              print 'Error: Not able to get status of created instance: %s' % reservations.instances[0].id
           if status[0].instances[0].state == 'running':
              break
           else:
              print "pending... starting instance " + str(clock) + " sec"
              time.sleep(3)
              clock += 3
              if clock == 60:
                 print "Instance %s not comming to running state" % reservations.instances[0].id
                 self.conn.close()
                 sys.exit(1)
        return status

   def terminate_ec2_instance(self,id=None):
        """
        Terminate intance in given region based on instance id
        """
   	try:
            self.conn.terminate_instances(instance_ids=[id])
            print 'Info: Instance \'%s\' terminated' % id
	except:
	    print 'Error: Unable to terminate the instance: %s' % id
