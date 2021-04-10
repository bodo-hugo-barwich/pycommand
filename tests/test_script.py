#!/usr/bin/python3
'''
This Script is the Test Script which is run in the Command Module Test
It generates Output to STDOUT and STDERR
It returns the EXIT CODE passed as Parameter. Only Positive Integer EXIT CODES are allowed

:version: 2021-04-10

:author: Bodo Hugo Barwich
'''
import sys
import os
import time



itm = -1;
itmstrt = -1;
itmend = -1;


itmstrt = time.time()

print("Start - Time Now: '{}'".format(itmstrt))

print('Number of arguments: {} arguments.'.format(len(sys.argv)))
print('Argument List: {}'.format(str(sys.argv)))


smodule = '';
spath = os.path.abspath(__file__);

print("test script absolute path: '{}'".format(spath))

slashpos = spath.rfind('/', 0)

if slashpos != -1 :
  smodule = spath[slashpos + 1 : len(spath)]
else :
  smodule = spath

print("script '{}' START 0 ERROR".format(smodule), file = sys.stderr)


if(len(sys.argv) > 1):
  try :
    ipause = int(sys.argv[1])
  except Exception as e :
    print("script '{}' Parameter '{}': Parameter Invalid! Whole Number expected.".format(smodule, sys.argv[1])\
    , file = sys.stderr)
    print("script '{}' Exception Message: {}".format(smodule, str(e)), file = sys.stderr)

    ipause = 0

else:
  ipause = 0

if(len(sys.argv) > 2):
  try :
    ierr = int(sys.argv[2])
  except Exception as e :
    print("script '{}' Parameter '{}': Parameter Invalid! Whole Number expected.".format(smodule, sys.argv[2])\
    , file = sys.stderr)
    print("script '{}' Exception Message: {}".format(smodule, str(e)), file = sys.stderr)

    ierr = 1

else:
  ierr = 0

if(ipause < 0):
  print("script '{}' Parameter '{}': Parameter Invalid! Positive Whole Number expected.".format(smodule, ipause)\
  , file = sys.stderr)
  ipause = 0

if(ierr < 0):
  print("script '{}' Parameter '{}': Parameter Invalid! Positive Whole Number expected.".format(smodule, ierr)\
  , file = sys.stderr)
  ierr = 1

print("script '{}' START 0".format(smodule))

print("script '{}' PAUSE '{}' ...".format(smodule, ipause))

time.sleep(ipause)

print("script '{}' END 1".format(smodule))

print("script '{}' END 1 ERROR".format(smodule), file = sys.stderr)


itmend = time.time()

itm = (itmend - itmstrt) * 1000

print("End - Time Now: '{}'".format(itmend))

print("script '{}' done in '{}' ms".format(smodule, itm))

print("script '{}' EXIT '{}'".format(smodule, ierr))


sys.exit(ierr)
