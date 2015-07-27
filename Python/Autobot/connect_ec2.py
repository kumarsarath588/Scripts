#!/usr/bin/python

import boto.ec2
import sys

def create_ec2_connection(INPUTS):
  """
  Connect to ec2 instance with respect to the provided region name
  """
  region=INPUTS['config']['region']
  default_region='us-east-1'
  try:
    conn = boto.ec2.connect_to_region(region)
    if str(conn.DefaultRegionName) != default_region:
        print "Invalid Region Name"
        sys.exit(1)
  except:
    print 'Error Occured while connecting to region'
    sys.exit(1)
  return conn

