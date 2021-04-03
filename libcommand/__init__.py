'''
Definition of the libcommand Package
Definition of the runCommand() Function

@version: 2021-04-03

@author: Bodo Hugo Barwich
'''
__all__ = ['command']

from libcommand.command import Command



def runCommand(scommandline = ''):
  '''
  This Method launches a process defined by `scommandline` in a separate child process

  :returns: Returns a Tuple with the STDOUT, STDERR and EXIT Code
  :rtype: tuple
  '''

  arrrs = ['', '', 0]

  cmd = Command(scommandline)

  if(cmd.Launch()):
    cmd.Wait()

  arrrs[0] = cmd.getReportString()
  arrrs[1] = cmd.getErrorString()
  arrrs[2] = cmd.getProcessStatus()

  if arrrs[2] == -1 :
    arrrs[2] = cmd.getErrorCode()

  cmd.freeResources()

  return arrrs


def runCommandWithOptions(commandoptions = {}):
  '''
  This Method launches a process defined by `commandoptions['command']` in a separate child process
  Additional options in `commandoptions` are also configured before launching the child process

  :returns: Returns a Tuple with the STDOUT, STDERR and EXIT Code
  :rtype: tuple
  '''
  arrrs = ['', '', 0]

  if('command' in commandoptions):
    cmd = Command()

    cmd.setDictOptions(commandoptions)

    if(cmd.Launch()):
      cmd.Wait()

      arrrs[0] = cmd.getReportString()
      arrrs[1] = cmd.getErrorString()
      arrrs[2] = cmd.getProcessStatus()

      if arrrs[2] == -1 :
        arrrs[2] = cmd.getErrorCode()

      cmd.freeResources()

    else: #if(cmd.Launch())
      arrrs[2] = 1

  else:
    arrrs[0] = ''
    arrrs[1] = ''
    arrrs[2] = 3

  return arrrs

