__all__ = ['command']

from libcommand.command import Command



def runCommand(scommandline = ''):
  arrrs = ['', '', 0]

  if(scommandline != ''):
    cmd = Command(scommandline)

    if(cmd.Launch()):
      cmd.Check()

      arrrs[0] = cmd.getReportString()
      arrrs[1] = cmd.getErrorString()
      arrrs[2] = cmd.getErrorCode()
    else:
      arrrs[2] = 1

  else:
    arrrs[0] = ''
    arrrs[1] = ''
    arrrs[2] = 3

  return arrrs


def runCommandWithOptions(commandoptions = {}):
  arrrs = ['', '', 0]

  if('command' in commandoptions):
    cmd = Command(commandoptions['command'])

    if(cmd.Launch()):
      cmd.Check()
    else:
      arrrs[2] = 1

  else:
    arrrs[0] = ''
    arrrs[1] = ''
    arrrs[2] = 3

  return arrrs

