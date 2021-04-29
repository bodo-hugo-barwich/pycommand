#!/usr/bin/python3
'''
Tests to verify the CommandGroup Class Functionality

@version: 2021-04-25

@author: Bodo Hugo Barwich
'''
import sys
import os
import time
import re
from re import IGNORECASE

sys.path.append("./")
sys.path.append("../")

from libcommand import Command
from libcommand import CommandGroup



sdirectory = os.getcwd() + '/'
smodule = ''
stestscript = 'command_script.py'
itestpause = 3
iteststatus = 4

spath = os.path.abspath(__file__);

print("test script absolute path: '{}'".format(spath))

slashpos = spath.rfind('/', 0)

if slashpos != -1 :
  sdirectory = spath[0 : slashpos + 1]
  smodule = spath[slashpos + 1 : len(spath)]
else :
  smodule = spath


print("Test Directory: '{}'".format(sdirectory))
print("Test Module: '{}'".format(smodule))


def test_CommandGroupRun():
  print("{} - go ...".format(sys._getframe().f_code.co_name))

  stestscript = 'command_script.py'

  cmdgrp = CommandGroup();
  imaxpause = 3

  cmd = Command("{}{} {}".format(sdirectory, stestscript, 2)\
  , {'name': 'command-script:2s'})

  cmdgrp.Add(cmd)

  cmd = Command("{}{} {}".format(sdirectory, stestscript, 3)\
  , {'name': 'command-script:3s'})

  cmdgrp.Add(cmd)

  cmd = Command("{}{} {}".format(sdirectory, stestscript, 1)\
  , {'name': 'command-script:1s'})

  cmdgrp.Add(cmd)

  cmdcnt = cmdgrp.len

  assert cmdcnt == 3, "scripts (count: '{}'): were not added correctly".format(cmdcnt)

  itm = -1
  itmstrt = time.time()
  itmend = -1

  print("Command Group Execution Start - Time Now: '{}' s".format(itmstrt))

  assert cmdgrp.Run(), "Command Group Execution: Execution was not correct"

  itmend = time.time()
  itm = (itmend - itmstrt) * 1000;

  print("Command Group Execution End - Time Now: '{}' s".format(itmend))
  print("Command Group Execution finished in '{}' ms".format(itm))

  itm = int(itmend - itmstrt)

  print("Command Group Execution Time '{} / {}' s".format(itm, imaxpause))

  assert itm == imaxpause, "Command Group Execution longer than maximal Execution Time '{}' s"\
  .format(imaxpause)

  for icmd in range(0, cmdcnt) :
    cmd = cmdgrp.getiCommand(icmd);

    assert cmd is not None, "Command No. '$iprc': Not listed correctly".format(icmd)

    if cmd is not None :
      print("Command {}:".format(cmd.getNameComplete()))

      scriptlog = cmd.report
      scripterror = cmd.error
      iscriptstatus = cmd.status

      print("ERROR CODE: '{}'".format(cmd.code))
      print("EXIT CODE: '{}'".format(iscriptstatus))

      if scriptlog is not None :
        print("STDOUT: '{}'".format(scriptlog))
      else :
        assert scriptlog is not None, "STDOUT was not captured"

      if scripterror is not None :
        print("STDERR: '{}'".format(scripterror))
      else :
        assert scripterror is not None, "STDERR was not captured"

    #if cmd is not None
  #for icmd in range(0, cmdcnt)

  print("")



