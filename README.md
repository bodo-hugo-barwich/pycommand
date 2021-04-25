[![Automated Tests](https://github.com/bodo-hugo-barwich/pycommand/actions/workflows/python-package.yml/badge.svg)](https://github.com/bodo-hugo-barwich/pycommand/actions/workflows/python-package.yml) [![Build Status](https://travis-ci.com/bodo-hugo-barwich/pycommand.svg?branch=master)](https://travis-ci.com/bodo-hugo-barwich/pycommand)

# Command

Command - Python Package for Multiprocessing

Provides Classes to launch Child Processes asynchronously.\
The **Object Oriented Design** allows to create Groups of Child Processes and Child Process Pools to launch several child processes in an organized manner.

## Features
Some important Features are:
* Low Dependencies (uses only Python Core Packages)\
  Low Dependency Usage leads to:
  	* Very High Compatibility (only Python 3 is required)
  	* Easy Installation
	* Small Memory Footprint (Simple Structure Design leads to low Memory Usage)
	* Fast Startup (very few additional Libraries to load)
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
Providing a similar functionality as the [`subprocess.run()` Function](https://docs.python.org/3/library/subprocess.html#subprocess.run) it can serve as a Procedural Replacement for this function without the need of special error handling of possible Exceptions. \
This implementation aimes especially for Low Dependencies and Easy Installation.

### Example Use Case
The Power of this Library is best shown by an Example Use Case as seen in the `test_CommandGroupRun()` Test:
Having 3 Jobs at hand of 2 seconds, 3 seconds and 1 second running them sequencially would take aproximately **6 seconds**.
But using the `CommandGroup` Class it takes effectively only **3 seconds** to complete.
And still each Job can be evaluated separately by their own Results keeping Log Message separate from Error Messages and viewing them in their context.
```text
test module: './commandgrouptests.py'
test module absolute path: '/path/to/pycommand/tests/commandgrouptests.py'
tests starting ...

setUp - go ...
setUp - Test Directory: '/path/to/pycommand/tests/'
setUp - Test Module: 'commandgrouptests.py'

test_CommandGroupRun - go ...
Command Group Execution Start - Time Now: '1619352416.777284' s
Command Group Execution End - Time Now: '1619352419.8313038' s
Command Group Execution finished in '3054.0199279785156' ms
Command Group Execution Time '3 / 3' s
Command  (4202) 'command-script:2s' :
ERROR CODE: ' 0 '
EXIT CODE: '0'
STDOUT: ' Start - Time Now: '1619352416.82219'
Number of arguments: 2 arguments.
Argument List: ['/path/to/pycommand/tests/command_script.py', '2']
test script absolute path: '/path/to/pycommand/tests/command_script.py'
script 'command_script.py' START 0
script 'command_script.py' PAUSE '2' ...
script 'command_script.py' END 1
End - Time Now: '1619352418.8242822'
script 'command_script.py' done in '2002.0921230316162' ms
script 'command_script.py' EXIT '0'
 '
STDERR: ' script 'command_script.py' START 0 ERROR
script 'command_script.py' END 1 ERROR
 '
Command  (4203) 'command-script:3s' :
ERROR CODE: ' 0 '
EXIT CODE: '0'
STDOUT: ' Start - Time Now: '1619352416.824399'
Number of arguments: 2 arguments.
Argument List: ['/path/to/pycommand/tests/command_script.py', '3']
test script absolute path: '/path/to/pycommand/tests/command_script.py'
script 'command_script.py' START 0
script 'command_script.py' PAUSE '3' ...
script 'command_script.py' END 1
End - Time Now: '1619352419.8276176'
script 'command_script.py' done in '3003.218650817871' ms
script 'command_script.py' EXIT '0'
 '
STDERR: ' script 'command_script.py' START 0 ERROR
script 'command_script.py' END 1 ERROR
 '
Command  (4204) 'command-script:1s' :
ERROR CODE: ' 0 '
EXIT CODE: '0'
STDOUT: ' Start - Time Now: '1619352416.8315842'
Number of arguments: 2 arguments.
Argument List: ['/path/to/pycommand/tests/command_script.py', '1']
test script absolute path: '/path/to/pycommand/tests/command_script.py'
script 'command_script.py' START 0
script 'command_script.py' PAUSE '1' ...
script 'command_script.py' END 1
End - Time Now: '1619352417.832275'
script 'command_script.py' done in '1000.6906986236572' ms
script 'command_script.py' EXIT '0'
 '
STDERR: ' script 'command_script.py' START 0 ERROR
script 'command_script.py' END 1 ERROR
 '
```

## Usage
### runCommand() Function
The `pytest` test suite `test_RunCommand()` demonstrates the `runCommand()` Function Use Case
which is easy to use and straight forward:
```python

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
