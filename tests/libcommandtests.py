#!/usr/bin/python3
'''
Tests to verify the Command Class Functionality

@version: 2021-04-03

@author: Bodo Hugo Barwich
'''
import sys
import os
import unittest

sys.path.append("../")

from libcommand.command import Command
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
    print("setUp - Test Module: '{}'\n".format(__file__))

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

    arrrs = runCommand("{}{} {} {}".format(self._sdirectory, self._stestscript, self._itestpause, self._iteststatus))

    print("EXIT CODE: '{}'".format(arrrs[2]));

    self.assertFalse(arrrs[0] == '', "STDOUT was not captured.\n")

    print("STDOUT: '{}'".format(arrrs[0]));

    self.assertFalse(arrrs[1] == '', "STDERR was not captured.\n")

    print("STDERR: '{}'".format(arrrs[1]));

    print("")


  def test_ReadTimeout(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    cmdtest = Command("{}{} {}".format(self._sdirectory, self._stestscript, self._itestpause))

    cmdtest.setDictOptions({'check': 2, 'profiling': 1, 'debug': True})

    self.assertNotEqual(cmdtest.getReadTimeout(), -1, "Read Timeout is not set")
#    self.assertEqual(cmdtest.isProfiling, True, 'Profiling is not enabled')

    self.assertEqual(cmdtest.Launch(), True, "script '{}': Launch failed!".format(self._stestscript))
    self.assertEqual(cmdtest.Wait(), True, "script '{}': Execution failed!".format(self._stestscript))

    scriptlog = cmdtest.report
    scripterror = cmdtest.error
    iscriptstatus = cmdtest.status

    #ok($proctest->getExecutionTime < $proctest->getReadTimeout * 2, "Measured Time is smaller than the Read Timeout");

    #print("Execution Time: '", $proctest->getExecutionTime, "'\n");

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



if __name__ == "__main__":
  print("test module: '{}'".format(__file__))

  spath = os.path.abspath(__file__)

  print("test module absolute path: '{}'".format(spath))

  print("tests starting ...\n")
  #import sys;sys.argv = ['', 'Test.testConstructor']
  unittest.main()

  print("tests done.\n")

