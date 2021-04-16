#!/usr/bin/python3
'''
Tests to verify the Command Class Functionality

@version: 2021-04-16

@author: Bodo Hugo Barwich
'''
import sys
import os
import re
from re import IGNORECASE

sys.path.append("./")
sys.path.append("../")

from libcommand import Command
from libcommand import runCommand



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



def test_RunCommand():
  print("{} - go ...".format(sys._getframe().f_code.co_name))

  stestscript = 'command_script.py'
  itestpause = 3

  arrrs = runCommand("{}{} {} {}".format(sdirectory, stestscript, itestpause, iteststatus))

  print("EXIT CODE: '{}'".format(arrrs[2]));

  assert arrrs[0] != '', "STDOUT was not captured."

  print("STDOUT: '{}'".format(arrrs[0]));

  assert arrrs[1] != '', "STDERR was not captured."

  print("STDERR: '{}'".format(arrrs[1]));

  print("")


def test_ReadTimeout():
  print("{} - go ...".format(sys._getframe().f_code.co_name))

  stestscript = 'command_script.py'
  itestpause = 3

  cmdtest = Command("{}{} {}".format(sdirectory, stestscript, itestpause))

  cmdtest.setDictOptions({'check': 2, 'profiling': True})

  assert cmdtest.getReadTimeout() != -1, 'Read Timeout is not set'
  assert cmdtest.isProfiling(), 'Profiling is not enabled'

  assert cmdtest.Launch(), "script '{}': Launch failed!".format(stestscript)
  assert cmdtest.Wait(), "script '{}': Execution failed!".format(stestscript)

  scriptlog = cmdtest.report
  scripterror = cmdtest.error
  iscriptstatus = cmdtest.status

  print("ERROR CODE: '{}'".format(cmdtest.code))
  print("EXIT CODE: '{}'".format(iscriptstatus))
  print("Execution Time: '{}'".format(cmdtest.execution_time));

  assert cmdtest.getExecutionTime() < cmdtest.getReadTimeout() * 2\
  , "Measured Time is greater or equal than the Read Timeout"

  if(scriptlog is not None):
    print("STDOUT: '{}'".format(scriptlog))
  else:
    assert scriptlog is not None, "STDOUT was not captured"

  if(scripterror is not None):
    print("STDERR: '{}'".format(scripterror))
  else:
    assert scripterror is not None, "STDERR was not captured"

  print("")


def test_ExecutionTimeout():
  print("{} - go ...".format(sys._getframe().f_code.co_name))

  stestscript = 'command_script.py'
  itestpause = 30

  cmdtest = Command("{}{} {}".format(sdirectory, stestscript, itestpause)\
    , {'timeout': 5, 'check': 1, 'profiling': True})

  assert cmdtest.getTimeout() != -1, 'Execution Timeout is not set'
  assert cmdtest.isProfiling(), 'Profiling is not enabled'

  assert cmdtest.Launch(), "script '{}': Launch failed!".format(stestscript)
  assert not cmdtest.Wait(), "script '{}': Execution did not fail".format(stestscript)

  scriptlog = cmdtest.report
  scripterror = cmdtest.error
  iscriptstatus = cmdtest.status

  print("ERROR CODE: '{}'".format(cmdtest.code))
  print("EXIT CODE: '{}'".format(iscriptstatus))
  print("Execution Time: '{}'".format(cmdtest.execution_time));

  assert cmdtest.code == 4, "ERROR CODE '4' was not returned"

  if iscriptstatus == -15 :
    #Script informs Termination Signal
    assert iscriptstatus == -15, "EXIT CODE is not correct"
  else :
    #Script informs Termination Signal
    assert iscriptstatus <= 4, "EXIT CODE is not correct"

  assert cmdtest.getExecutionTime() < itestpause\
  , "Measured Time is greater or equal than the Full Run Time"

  assert scriptlog is not None, "STDOUT was not captured"

  if scriptlog is not None :
    print("STDOUT: '{}'".format(scriptlog))

  assert scripterror is not None, "STDERR was not captured"

  if scripterror is not None :
    print("STDERR: '{}'".format(scripterror))

    pat_tmout = re.compile('Execution timed out', re.IGNORECASE)

    assert pat_tmout.search(scripterror) is not None, "STDERR does not report Execution Timeout"

  #if scripterror is not None

  print("")


def test_ScriptNotFound():
  print("{} - go ...".format(sys._getframe().f_code.co_name))

  stestscript = 'no_script.sh'

  cmdtest = Command(sdirectory + stestscript)

  brunok = cmdtest.Launch() and cmdtest.Wait()

  scriptlog = cmdtest.report
  scripterror = cmdtest.error
  iscriptstatus = cmdtest.status

  print("ERROR CODE: '{}'".format(cmdtest.code))
  print("EXIT CODE: '{}'".format(iscriptstatus))

  if iscriptstatus == -1 :
    assert not brunok, "script '{}': Execution did not fail".format(stestscript)
  else :
    assert not brunok, "script '{}': Execution did not fail".format(stestscript)

  assert cmdtest.code == 1, "ERROR CODE '1' was not returned"

  if iscriptstatus == 255 :
    assert iscriptstatus == 255, "EXIT CODE '255' was not returned"
  else :
    assert iscriptstatus == 2, "EXIT CODE '2' was not returned"

  assert scriptlog is not None, "STDOUT was not captured"

  if scriptlog is not None :
    print("STDOUT: '{}'".format(scriptlog))

  assert scripterror is not None, "STDERR was not captured"

  if scripterror is not None :
    print("STDERR: '{}'".format(scripterror))

    pat_ntfnd = re.compile('no such file', re.IGNORECASE)

    assert pat_ntfnd.search(scripterror) is not None, "STDERR does not report Not Found Error"

  #if scripterror is not None

  print("")


def test_NoPermission():
  print("{} - go ...".format(sys._getframe().f_code.co_name))

  stestscript = 'noexec_script.py'

  cmdtest = Command(sdirectory + stestscript)

  brunok = cmdtest.Launch() and cmdtest.Wait()

  scriptlog = cmdtest.report
  scripterror = cmdtest.error
  iscriptstatus = cmdtest.status

  print("ERROR CODE: '{}'".format(cmdtest.code))
  print("EXIT CODE: '{}'".format(iscriptstatus))

  if iscriptstatus == -1 :
    assert not brunok, "script '{}': Execution did not fail".format(stestscript)
  else :
    assert not brunok, "script '{}': Execution did not fail".format(stestscript)

  assert cmdtest.code == 1, "ERROR CODE '1' was not returned"

  if iscriptstatus == 255 :
    assert iscriptstatus == 255, "EXIT CODE '255' was not returned"
  else :
    assert iscriptstatus == 13, "EXIT CODE '13' was not returned"

  assert scriptlog is not None, "STDOUT was not captured"

  if scriptlog is not None :
    print("STDOUT: '{}'".format(scriptlog))

  assert scripterror is not None, "STDERR was not captured"

  if scripterror is not None :
    print("STDERR: '{}'".format(scripterror))

    pat_noperm = re.compile('permission denied', re.IGNORECASE)

    assert pat_noperm.search(scripterror) is not None, "STDERR does not report No Permission Error"

  #if scripterror is not None

  print("")


def test_BashError():
  print("{} - go ...".format(sys._getframe().f_code.co_name))

  stestscript = 'nobashbang_script.py'

  cmdtest = Command(sdirectory + stestscript)

  brunok = cmdtest.Launch() and cmdtest.Wait()

  scriptlog = cmdtest.report
  scripterror = cmdtest.error
  iscriptstatus = cmdtest.status

  print("ERROR CODE: '{}'".format(cmdtest.code))
  print("EXIT CODE: '{}'".format(iscriptstatus))

  assert cmdtest.code == 1, "ERROR CODE '1' was not returned"
  assert iscriptstatus == 8, "EXIT CODE '8' was not returned"
  assert not brunok, "script '{}': Execution did not fail".format(stestscript)

  assert scriptlog is not None, "STDOUT was not captured"

  if scriptlog is not None :
    print("STDOUT: '{}'".format(scriptlog))

  assert scripterror is not None, "STDERR was not captured"

  if scripterror is not None :
    print("STDERR: '{}'".format(scripterror))

    pat_synerr = re.compile('exec format error', re.IGNORECASE)

    assert pat_synerr.search(scripterror) is not None, "STDERR does not report Bash Error"

  #if scripterror is not None

  print('')


def test_PythonException():
  print("{} - go ...".format(sys._getframe().f_code.co_name))

  stestscript = 'exception_script.py'

  cmdtest = Command(sdirectory + stestscript)

  brunok = cmdtest.Launch() and cmdtest.Wait()

  scriptlog = cmdtest.report
  scripterror = cmdtest.error
  iscriptstatus = cmdtest.status

  print("ERROR CODE: '{}'".format(cmdtest.code))
  print("EXIT CODE: '{}'".format(iscriptstatus))

  assert cmdtest.code == 0, "ERROR CODE '0' was not returned"
  assert iscriptstatus == 1, "EXIT CODE '1' was not returned"
  assert brunok, "script '{}': Execution did fail".format(stestscript)

  assert scriptlog is not None, "STDOUT was not captured"

  if scriptlog is not None :
    print("STDOUT: '{}'".format(scriptlog))

  assert scripterror is not None, "STDERR was not captured"

  if scripterror is not None :
    print("STDERR: '{}'".format(scripterror))

    pat_except = re.compile('python exception', re.IGNORECASE)

    assert pat_except.search(scripterror) is not None, "STDERR does not report the Python Exeception"

  #if scripterror is not None

  print('')

