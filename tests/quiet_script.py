#!/usr/bin/python3
'''
This Script is the Test Script which is run in the Process::SubProcess Module Test
It does not generate any Output
It returns the EXIT CODE passed as Parameter. Only Integer EXIT CODES are allowed

:version: 2021-04-26

:author: Bodo Hugo Barwich
'''
import sys
import time



if(len(sys.argv) > 1):
  try :
    ipause = int(sys.argv[1])
  except Exception as e :
    ipause = 0

else:
  ipause = 0

if(len(sys.argv) > 2):
  try :
    ierr = int(sys.argv[2])
  except Exception as e :
    ierr = 1

else:
  ierr = 0

if(ipause < 0):
  ipause = 0

if(ierr < 0):
  ierr = 1

time.sleep(ipause)


sys.exit(ierr)
