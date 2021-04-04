'''
Definition of the libcommand Package
Definition of the runCommand() Function

@version: 2021-04-03

@author: Bodo Hugo Barwich
'''
__all__ = ['command']

from libcommand.command import Command



def runCommand(scommandline = '', options = {}):
  '''
  This Method launches a process defined by `scommandline` in a separate child process

  :param scommandline: The commmand and its parameters to be executed in the child process
  :type scommandline: string
  :param options: Additional options for the execution as key - value pairs
  :type options: dictionary
  :returns: Returns a Tuple with the STDOUT, STDERR and EXIT Code
  :rtype: tuple
  '''

  arrrs = ['', '', 0]

  cmd = Command(scommandline, options)

  if(cmd.Launch()):
    cmd.Wait()

  arrrs[0] = cmd.getReportString()
  arrrs[1] = cmd.getErrorString()
  arrrs[2] = cmd.getProcessStatus()

  if arrrs[2] == -1 :
    arrrs[2] = cmd.getErrorCode()

  cmd.freeResources()
  cmd = None

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

