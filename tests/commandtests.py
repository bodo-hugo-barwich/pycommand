#!/usr/bin/python3
'''
Tests to verify the Command Class Functionality

@version: 2021-04-10

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

    self._stestscript = 'test_script.py'
    self._itestpause = 3

    arrrs = runCommand("{}{} {} {}".format(self._sdirectory, self._stestscript, self._itestpause, self._iteststatus))

    print("EXIT CODE: '{}'".format(arrrs[2]));

    self.assertFalse(arrrs[0] == '', "STDOUT was not captured.")

    print("STDOUT: '{}'".format(arrrs[0]));

    self.assertFalse(arrrs[1] == '', "STDERR was not captured.")

    print("STDERR: '{}'".format(arrrs[1]));

    print("")


  def test_ReadTimeout(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._stestscript = 'test_script.py'
    self._itestpause = 3

    cmdtest = Command("{}{} {}".format(self._sdirectory, self._stestscript, self._itestpause))

    cmdtest.setDictOptions({'check': 2, 'profiling': True})

    self.assertNotEqual(cmdtest.getReadTimeout(), -1, 'Read Timeout is not set')
    self.assertTrue(cmdtest.isProfiling(), 'Profiling is not enabled')

    self.assertTrue(cmdtest.Launch(), "script '{}': Launch failed!".format(self._stestscript))
    self.assertTrue(cmdtest.Wait(), "script '{}': Execution failed!".format(self._stestscript))

    scriptlog = cmdtest.report
    scripterror = cmdtest.error
    iscriptstatus = cmdtest.status

    print("ERROR CODE: '{}'".format(cmdtest.code))
    print("EXIT CODE: '{}'".format(iscriptstatus))
    print("Execution Time: '{}'".format(cmdtest.execution_time));

    self.assertTrue(cmdtest.getExecutionTime() < cmdtest.getReadTimeout() * 2\
    , "Measured Time is greater or equal than the Read Timeout");

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

    self._stestscript = 'test_script.py'
    self._itestpause = 30

    cmdtest = Command("{}{} {}".format(self._sdirectory, self._stestscript, self._itestpause)\
      , {'timeout': 5, 'check': 1, 'profiling': True})

    self.assertNotEqual(cmdtest.getTimeout(), -1, 'Execution Timeout is not set')
    self.assertNotEqual(cmdtest.isProfiling(), 'Profiling is not enabled')

    self.assertTrue(cmdtest.Launch(), "script '{}': Launch failed!".format(self._stestscript))
    self.assertFalse(cmdtest.Wait(), "script '{}': Execution did not fail".format(self._stestscript))

    scriptlog = cmdtest.report
    scripterror = cmdtest.error
    iscriptstatus = cmdtest.status

    print("ERROR CODE: '{}'".format(cmdtest.code))
    print("EXIT CODE: '{}'".format(iscriptstatus))
    print("Execution Time: '{}'".format(cmdtest.execution_time));

    self.assertEqual(cmdtest.code, 4, "ERROR CODE '4' was not returned")

    if iscriptstatus == -15 :
      #Script informs Termination Signal
      self.assertEqual(iscriptstatus, -15, "EXIT CODE is not correct")
    else :
      #Script informs Termination Signal
      self.assertTrue(iscriptstatus <= 4, "EXIT CODE is not correct")

    self.assertTrue(cmdtest.getExecutionTime() < self._itestpause\
    , "Measured Time is greater or equal than the Full Run Time");

    self.assertIsNotNone(scriptlog, "STDOUT was not captured")

    if scriptlog is not None :
      print("STDOUT: '{}'".format(scriptlog))

    self.assertIsNotNone(scripterror, "STDERR was not captured")

    if scripterror is not None :
      print("STDERR: '{}'".format(scripterror))

      pat_tmout = re.compile('Execution timed out', re.IGNORECASE)

      self.assertIsNotNone(pat_tmout.search(scripterror), "STDERR does not report Execution Timeout");

    #if scripterror is not None

    print("")


  def test_ScriptNotFound(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._stestscript = 'no_script.sh'

    cmdtest = Command(self._sdirectory + self._stestscript)

    brunok = cmdtest.Launch() and cmdtest.Wait()

    scriptlog = cmdtest.report
    scripterror = cmdtest.error
    iscriptstatus = cmdtest.status

    print("ERROR CODE: '{}'".format(cmdtest.code))
    print("EXIT CODE: '{}'".format(iscriptstatus))

    if iscriptstatus == -1 :
      self.assertFalse(brunok, "script '{}': Execution did not fail".format(self._stestscript))
    else :
      self.assertFalse(brunok, "script '{}': Execution did not fail".format(self._stestscript))

    self.assertEqual(cmdtest.code, 1, "ERROR CODE '1' was not returned")

    if iscriptstatus == 255 :
      self.assertEqual(iscriptstatus, 255, "EXIT CODE '255' was not returned")
    else :
      self.assertEqual(iscriptstatus, 2, "EXIT CODE '2' was not returned")

    self.assertIsNotNone(scriptlog, "STDOUT was not captured")

    if scriptlog is not None :
      print("STDOUT: '{}'".format(scriptlog))

    self.assertIsNotNone(scripterror, "STDERR was not captured")

    if scripterror is not None :
      print("STDERR: '{}'".format(scripterror))

      pat_ntfnd = re.compile('no such file', re.IGNORECASE)

      self.assertIsNotNone(pat_ntfnd.search(scripterror), "STDERR does not report Not Found Error");

    #if scripterror is not None

    print("")


  def test_NoPermission(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._stestscript = 'noexec_script.py'

    cmdtest = Command(self._sdirectory + self._stestscript)

    brunok = cmdtest.Launch() and cmdtest.Wait()

    scriptlog = cmdtest.report
    scripterror = cmdtest.error
    iscriptstatus = cmdtest.status

    print("ERROR CODE: '{}'".format(cmdtest.code))
    print("EXIT CODE: '{}'".format(iscriptstatus))

    if iscriptstatus == -1 :
      self.assertFalse(brunok, "script '{}': Execution did not fail".format(self._stestscript))
    else :
      self.assertFalse(brunok, "script '{}': Execution did not fail".format(self._stestscript))

    self.assertEqual(cmdtest.code, 1, "ERROR CODE '1' was not returned")

    if iscriptstatus == 255 :
      self.assertEqual(iscriptstatus, 255, "EXIT CODE '255' was not returned")
    else :
      self.assertEqual(iscriptstatus, 13, "EXIT CODE '13' was not returned")

    self.assertIsNotNone(scriptlog, "STDOUT was not captured")

    if scriptlog is not None :
      print("STDOUT: '{}'".format(scriptlog))

    self.assertIsNotNone(scripterror, "STDERR was not captured")

    if scripterror is not None :
      print("STDERR: '{}'".format(scripterror))

      pat_noperm = re.compile('permission denied', re.IGNORECASE)

      self.assertIsNotNone(pat_noperm.search(scripterror), "STDERR does not report No Permission Error");

    #if scripterror is not None

    print("")


  def test_BashError(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._stestscript = 'nobashbang_script.py'

    cmdtest = Command(self._sdirectory + self._stestscript)

    brunok = cmdtest.Launch() and cmdtest.Wait()

    scriptlog = cmdtest.report
    scripterror = cmdtest.error
    iscriptstatus = cmdtest.status

    print("ERROR CODE: '{}'".format(cmdtest.code))
    print("EXIT CODE: '{}'".format(iscriptstatus))

    self.assertEqual(cmdtest.code, 1, "ERROR CODE '1' was not returned")
    self.assertEqual(iscriptstatus, 8, "EXIT CODE '8' was not returned")
    self.assertFalse(brunok, "script '{}': Execution did not fail".format(self._stestscript))

    self.assertIsNotNone(scriptlog, "STDOUT was not captured")

    if scriptlog is not None :
      print("STDOUT: '{}'".format(scriptlog))

    self.assertIsNotNone(scripterror, "STDERR was not captured")

    if scripterror is not None :
      print("STDERR: '{}'".format(scripterror))

      pat_synerr = re.compile('exec format error', re.IGNORECASE)

      self.assertIsNotNone(pat_synerr.search(scripterror), "STDERR does not report Bash Error");

    #if scripterror is not None

    print('')


  def test_PythonException(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    self._stestscript = 'exception_script.py'

    cmdtest = Command(self._sdirectory + self._stestscript)

    brunok = cmdtest.Launch() and cmdtest.Wait()

    scriptlog = cmdtest.report
    scripterror = cmdtest.error
    iscriptstatus = cmdtest.status

    print("ERROR CODE: '{}'".format(cmdtest.code))
    print("EXIT CODE: '{}'".format(iscriptstatus))

    self.assertEqual(cmdtest.code, 0, "ERROR CODE '0' was not returned")
    self.assertEqual(iscriptstatus, 1, "EXIT CODE '1' was not returned")
    self.assertTrue(brunok, "script '{}': Execution did fail".format(self._stestscript))

    self.assertIsNotNone(scriptlog, "STDOUT was not captured")

    if scriptlog is not None :
      print("STDOUT: '{}'".format(scriptlog))

    self.assertIsNotNone(scripterror, "STDERR was not captured")

    if scripterror is not None :
      print("STDERR: '{}'".format(scripterror))

      pat_except = re.compile('python exception', re.IGNORECASE)

      self.assertIsNotNone(pat_except.search(scripterror), "STDERR does not report the Python Exeception");

    #if scripterror is not None

    print('')



if __name__ == "__main__":
  print("test module: '{}'".format(__file__))

  spath = os.path.abspath(__file__)

  print("test module absolute path: '{}'".format(spath))

  print("tests starting ...\n")
  #import sys;sys.argv = ['', 'Test.testConstructor']
  unittest.main()

  print("tests done.\n")

