#!/usr/bin/python3
'''
Tests to verify the CommandGroup Class Functionality

@version: 2021-04-25

@author: Bodo Hugo Barwich
'''
import sys
import os
import unittest
import time
import re
from re import IGNORECASE

sys.path.append("./")
sys.path.append("../")

from libcommand import Command
from libcommand import CommandGroup



class TestCommandGroup(unittest.TestCase):

  _sdirectory = ''
  _smodule = ''
  _stestscript = 'command_script.py'
  _itestpause = 3
  _iteststatus = 4


  def setUp(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._sdirectory = os.getcwd() + '/'

    spath = os.path.abspath(__file__);

    slashpos = spath.rfind('/', 0)

    if slashpos != -1 :
      self._sdirectory = spath[0 : slashpos + 1]
      self._smodule = spath[slashpos + 1 : len(spath)]
    else :
      self._smodule = spath

    print("setUp - Test Directory: '{}'".format(self._sdirectory))
    print("setUp - Test Module: '{}'".format(self._smodule))
    print("")


  def tearDown(self):
    pass


  def test_CommandGroupRun(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._stestscript = 'command_script.py'

    cmdgrp = CommandGroup();
    imaxpause = 3

    cmd = Command("{}{} {}".format(self._sdirectory, self._stestscript, 2)\
    , {'name': 'command-script:2s'})

    cmdgrp.Add(cmd)

    cmd = Command("{}{} {}".format(self._sdirectory, self._stestscript, 3)\
    , {'name': 'command-script:3s'})

    cmdgrp.Add(cmd)

    cmd = Command("{}{} {}".format(self._sdirectory, self._stestscript, 1)\
    , {'name': 'command-script:1s'})

    cmdgrp.Add(cmd)

    cmdcnt = cmdgrp.len

    self.assertEqual(cmdcnt, 3, "scripts (count: '{}'): were not added correctly".format(cmdcnt))

    itm = -1
    itmstrt = time.time()
    itmend = -1

    print("Command Group Execution Start - Time Now: '{}' s".format(itmstrt))

    self.assertTrue(cmdgrp.Run(), "Command Group Execution: Execution was not correct");

    itmend = time.time()
    itm = (itmend - itmstrt) * 1000;

    print("Command Group Execution End - Time Now: '{}' s".format(itmend))
    print("Command Group Execution finished in '{}' ms".format(itm))

    itm = int(itmend - itmstrt)

    print("Command Group Execution Time '{} / {}' s".format(itm, imaxpause))

    self.assertEqual(itm, imaxpause, "Command Group Execution longer than maximal Execution Time '{}' s"\
    .format(imaxpause))

    for icmd in range(0, cmdcnt) :
      cmd = cmdgrp.getiCommand(icmd);

      self.assertIsNotNone(cmd, "Command No. '$iprc': Not listed correctly".format(icmd))

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
          self.assertIsNotNone(scriptlog, "STDOUT was not captured")

        if scripterror is not None :
          print("STDERR: '{}'".format(scripterror))
        else :
          self.assertIsNotNone(scripterror, "STDERR was not captured")

      #if cmd is not None
    #for icmd in range(0, cmdcnt)

    print("")



if __name__ == "__main__":
  print("test module: '{}'".format(__file__))

  spath = os.path.abspath(__file__)

  print("test module absolute path: '{}'".format(spath))

  print("tests starting ...\n")
  #import sys;sys.argv = ['', 'Test.testConstructor']
  unittest.main()

  print("tests done.\n")
