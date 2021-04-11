# Command

Command - Python Package for Multiprocessing

Provides Classes to launch Child Processes asynchronously.\
The **Object Oriented Design** allows to create Groups of Child Processes and Child Process Pools to launch several child processes in an organized manner.

## Features
Some important Features are:
* Asynchronous Launch
* Reads Big Outputs
* Execution Timeout
* Configurable Read Interval
* Captures possible System Errors at Launch Time like "file not found" Errors
* Streamlined Error Handling while still providing the Outputs

## Motivation
This Module was conceived out of the need to launch multiple Tasks simultaneously while still keeping each Log and Error Messages and Exit Codes separately. \
As I developed it as Prototype at:
[Multi Process Manager](https://stackoverflow.com/questions/50177534/why-do-pipes-from-child-processes-break-sometimes-and-sometimes-not)\
The **Object Oriented Design** permits the implementation of the **[Command Pattern / Manager-Worker Pattern](https://en.wikipedia.org/wiki/Command_pattern)**.\
Providing a similar functionality as the [`subprocess.run` Function](https://docs.python.org/3/library/subprocess.html#subprocess.run) it can serve as a Procedural Replacement for this function without the need of special error handling of possible Exceptions.

## Usage
### runCommand() Function
Demonstrating the `runCommand()` Function Use Case:
```python

import unittest
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


 def test_RunCommand(self):
   print("{} - go ...".format(sys._getframe().f_code.co_name))

   self._itestpause = 3

   arrrs = runCommand("{}{} {} {}".format(self._sdirectory, self._stestscript, self._itestpause, self._iteststatus))

   print("EXIT CODE: '{}'".format(arrrs[2]));

   self.assertFalse(arrrs[0] == '', "STDOUT was not captured.")

   print("STDOUT: '{}'".format(arrrs[0]));

   self.assertFalse(arrrs[1] == '', "STDERR was not captured.")

   print("STDERR: '{}'".format(arrrs[1]));

   print("")


if __name__ == "__main__":
  unittest.main()


```

The Output shows how STDOUT, STDERR and EXIT Code are cleanly seperated.\
This will produce the Output:
```text
setUp - go ...
setUp - Test Directory: '/path/to/pycommand/tests'
setUp - Test Module: './commandtests.py'

test_RunCommand - go ...
EXIT CODE: '4'
STDOUT: 'Start - Time Now: '1617575015.5021873'
Number of arguments: 3 arguments.
Argument List: ['/path/to/pycommand/tests/test_script.py', '3', '4']
test script absolute path: '/path/to/pycommand/tests/test_script.py'
script 'test_script.py' START 0
script 'test_script.py' PAUSE '3' ...
script 'test_script.py' END 1
End - Time Now: '1617575018.503503'
script 'test_script.py' done in '3001.3158321380615' ms
script 'test_script.py' EXIT '4'
'
STDERR: 'script 'test_script.py' START 0 ERROR
script 'test_script.py' END 1 ERROR
'
```
