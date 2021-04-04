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
* Streamlined treatment of Errors while still providing the Outputs

## Motivation

This Module was conceived out of the need to launch multiple Tasks simultaneously while still keeping each Log and Error Messages and Exit Codes separately. \
As I developed it as Prototype at:
[Multi Process Manager](https://stackoverflow.com/questions/50177534/why-do-pipes-from-child-processes-break-sometimes-and-sometimes-not)\
The **Object Oriented Design** permits the implementation of the **[Command Pattern / Manager-Worker Pattern](https://en.wikipedia.org/wiki/Command_pattern)**.\
Providing a similar functionality as the [`subprocess.run` Function](https://docs.python.org/3/library/subprocess.html#subprocess.run) it can serve as a Procedural Replacement for this function without the need of special treatment for possible errors with Exceptions.

# Usage
## runCommand() Function
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

	   self.assertFalse(arrrs[0] == '', "STDOUT was not captured.\n")

	   print("STDOUT: '{}'".format(arrrs[0]));

	   self.assertFalse(arrrs[1] == '', "STDERR was not captured.\n")

	   print("STDERR: '{}'".format(arrrs[1]));

	   print("")
```
