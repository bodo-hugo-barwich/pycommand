#!/usr/bin/python3
'''
Tests to verify the Command Class Functionality

@version: 2021-04-03

@author: Bodo Hugo Barwich
'''
import sys
import os
import unittest
import re
from re import IGNORECASE

sys.path.append("../")

from libcommand import Command
from libcommand import runCommand



class TestCommand(unittest.TestCase):

  _sdirectory = ''
  _smodule = ''
  _stestscript = 'test_script.py'
  _itestpause = 3
  _iteststatus = 4


  def setUp(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))
    print("setUp - Test Directory: '{}'".format(os.getcwd()))
    print("setUp - Test Module: '{}'".format(__file__))

    self._sdirectory = os.getcwd() + '/'

    spath = os.path.abspath(__file__);

    slashpos = spath.rfind('/', 0)

    if slashpos != -1 :
      self._smodule = spath[slashpos + 1 : len(spath)]
    else :
      self._smodule = spath

    print("")


  def tearDown(self):
    pass


  def test_RunCommand(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._itestpause = 3

    arrrs = runCommand("{}{} {} {}".format(self._sdirectory, self._stestscript, self._itestpause, self._iteststatus))

    print("EXIT CODE: '{}'".format(arrrs[2]));

    self.assertFalse(arrrs[0] == '', "STDOUT was not captured.\n")

    print("STDOUT: '{}'".format(arrrs[0]));

    self.assertFalse(arrrs[1] == '', "STDERR was not captured.\n")

    print("STDERR: '{}'".format(arrrs[1]));

    print("")


  def test_ReadTimeout(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._itestpause = 3

    cmdtest = Command("{}{} {}".format(self._sdirectory, self._stestscript, self._itestpause))

    cmdtest.setDictOptions({'check': 2, 'profiling': 1, 'debug': True})

    self.assertNotEqual(cmdtest.getReadTimeout(), -1, "Read Timeout is not set")
    self.assertTrue(cmdtest.isProfiling, 'Profiling is not enabled')

    self.assertTrue(cmdtest.Launch(), "script '{}': Launch failed!".format(self._stestscript))
    self.assertTrue(cmdtest.Wait(), "script '{}': Execution failed!".format(self._stestscript))

    scriptlog = cmdtest.report
    scripterror = cmdtest.error
    iscriptstatus = cmdtest.status

    print("Execution Time: '{}'".format(cmdtest.execution_time));

    self.assertTrue(cmdtest.getExecutionTime() < cmdtest.getReadTimeout() * 2\
    , "Measured Time is greater or equal than the Read Timeout");

    print("EXIT CODE: '{}'".format(iscriptstatus))

    if(scriptlog is not None):
      print("STDOUT: '{}'".format(scriptlog))
    else:
      self.assertIsNotNone(scriptlog, "STDOUT was not captured")

    if(scripterror is not None):
      print("STDERR: '{}'".format(scripterror))
    else:
      self.assertIsNotNone(scripterror, "STDERR was not captured")

    print("")


  def test_ExecutionTimeout(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._itestpause = 4

    cmdtest = Command("{}{} {}".format(self._sdirectory, self._stestscript, self._itestpause)\
      , {'timeout': (self._itestpause - 2)})

    self.assertNotEqual(cmdtest.getTimeout(), -1, "Execution Timeout is not set")

    self.assertTrue(cmdtest.Launch(), "script '{}': Launch failed!".format(self._stestscript))
    self.assertFalse(cmdtest.Wait(), "script '{}': Execution did not fail".format(self._stestscript))

    scriptlog = cmdtest.report
    scripterror = cmdtest.error
    iscriptstatus = cmdtest.status

    print("ERROR CODE: '{}'".format(cmdtest.code))
    print("EXIT CODE: '{}'".format(iscriptstatus))

    self.assertEqual(cmdtest.code, 4, "ERROR CODE '4' was not returned")
    self.assertTrue(iscriptstatus < 1, "EXIT CODE is not correct")

    self.assertIsNotNone(scriptlog, "STDOUT was not captured")

    if scriptlog is not None :
      print("STDOUT: '{}'".format(scriptlog))

    self.assertIsNotNone(scripterror, "STDERR was not captured")

    if scripterror is not None :
      print("STDERR: '{}'".format(scripterror))

      pat_tmout = re.compile('Execution timed out', re.IGNORECASE)

      self.assertIsNotNone(pat_tmout.search(scripterror), "STDERR does not report Execution Timeout");

    #if(defined $rscripterror)

    print("")



if __name__ == "__main__":
  print("test module: '{}'".format(__file__))

  spath = os.path.abspath(__file__)

  print("test module absolute path: '{}'".format(spath))

  print("tests starting ...\n")
  #import sys;sys.argv = ['', 'Test.testConstructor']
  unittest.main()

  print("tests done.\n")

