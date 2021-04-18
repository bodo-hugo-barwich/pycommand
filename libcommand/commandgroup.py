'''
This Module provides the `CommandGroup` Class which manages multiple `Command` objects.
It executes and monitores the `Command` objects.

:version: 2021-04-18

:author: Bodo Hugo Barwich
'''
__docformat__ = "restructuredtext en"

import sys
import math
import time
from datetime import datetime

from .command import Command



#==============================================================================
# The CommandGroup Class


class CommandGroup(object):
  '''
  This is a Class to manage multiple `Command` object whom execution is related in time.

  It offers Methods to run, monitor and access the `Command` objects
  '''



  #----------------------------------------------------------------------------
  #Constructors

  def __init__(self, options = {}):
    '''
    A `CommandGroup` Object can be instantiated with a set of initial options `options`

    :param options: Additional options for the execution as key - value pairs
    :type options: dictionary
    '''

    self._arr_commands = []
    self._check_interval = -1
    self._read_timeout = 0
    self._execution_timeout = -1
    self._time_execution = -1
    self._time_start = -1
    self._time_end = -1
    self._arr_rpt = []
    self._arr_err = []
    self._sreport = None
    self._serror = None
    self._err_code = 0
    self._bprofiling = False
    self._bquiet = False
    self._bdebug = False

    if len(options) > 0 :
      self.setDictOptions(options)



  #----------------------------------------------------------------------------
  #Administration Methods


  def setDictOptions(self, options = {}):
    if 'debug' in options :
      self._bdebug = options['debug']

    if 'quiet' in options :
      self._bquiet = options['quiet']

    if 'check' in options :
      self.setCheckInterval(options['check'])

    if 'read' in options :
      self.setCheckInterval(options['read'])

    if 'readtimeout' in options :
      self.setCheckInterval(options['readtimeout'])

    if 'timeout' in options :
      self.setTimeout(options['timeout'])


  def setCheckInterval(self, icheckinterval = -1):
    try :
      self._check_interval = int(icheckinterval)
    except :
      #The Parameter is not a Number
      self._check_interval = -1

    if self._check_interval < -1 :
      #Disable Check Interval
      self._check_interval = -1

    if self._check_interval > 0 \
    and len(self._arr_commands) > 0 :
      irdtmout = math.floor(self._check_interval / len(self._arr_commands))

      #Save the required Read Timeout
      self.setReadTimeout(irdtmout)

    #if self._check_interval > 0 and len(self._arr_commands) > 0


  def setReadTimeout(self, ireadtimeout = 1):
    try :
      self._read_timeout = int(ireadtimeout)
    except :
      #The Parameter is not a Number
      #Disable Read Timeout
      self._read_timeout = 0

    if self._read_timeout < 0 :
      #Disable Read Timeout
      self._read_timeout = 0

    if len(self._arr_commands) > 0 :
      for cmd in self._arr_commands :
        cmd.setReadTimeout(self._read_timeout)

    #if len(self._arr_commands) > 0


  def setTimeout(self, iexecutiontimeout = -1 ):
    try :
      self._execution_timeout = int(iexecutiontimeout)
    except :
      #The Parameter is not a Number
      #Disable Execution Timeout
      self._execution_timeout = -1

    if self._execution_timeout < -1 :
      self._execution_timeout = -1


  def Add(self, ocommand = None):
    ors = None

    if ocommand is not None :
      ors = ocommand

      if not isinstance('Command', ors) :
        ors = None

    #if ocommand is not None

    if ors is None :
      #Create a new Command Object
      ors = Command()

    #Add the Command Object to the List
    self._arr_commands.append(ors)

    return ors


  def addsCommandLine(self, scommandline = '', options = {}):
    #Create a new Command Object
    ors = Command(scommandline, options)

    #Add the Command Object to the List
    self._arr_commands.append(ors)

    return ors


  def Launch(self):
    irs = 0
    icmdcnt = len(self._arr_commands)

    if self._bdebug :
      self._arr_rpt.append("{} - go ...\n".format(sys._getframe(0).f_code.co_name))
      self._arr_rpt.append("arr cmd cnt: '{}'\n".format(icmdcnt))

    if icmdcnt > 0 :
      cmd = None
      scmdnm = ''
      icmdidx = -1

      stmnow = None


      if self._check_interval > 0 \
      and self._read_timeout > 0 \
      and self._read_timeout * icmdcnt > self._check_interval :
        #Re-adjust the Check Interval
        self.setCheckInterval(self._check_interval)

      if self._execution_timeout > -1 :
        #Keep track of the Start Time
        self._start_time = time.time()

      for icmdidx in range(0, icmdcnt):
        cmd = self._arr_commands[icmdidx]

        if cmd is not None :
          scmdnm = "No. '{}' - {}".format(icmdidx, cmd.getNameComplete())

          stmnow = datetime.now().strftime('%F %T')

          self._arr_rpt.append("{} : Sub Process {}: Launching ...\n".format(stmnow, scmdnm))

          #Launch the Sub Process through Process::SubProcess::Launch()
          if cmd.Launch() :
            stmnow  = datetime.now().strftime('%F %T')

            self._arr_rpt.append("{} : Sub Process {}: Launch OK - PID ({})\n"\
            .format(stmnow, scmdnm, cmd.getProcessID()))

            irs += 1
          else :  #Sub Process Launch failed
            if cmd.code > self._err_code :
              #Keep the Child Process Error Code
              self._err_code = cmd.code

            self._arr_err.append("Sub Process {}: Launch failed!\nMessage: {}\n"\
            .format(scmdnm, cmd.error))

          #if cmd.Launch()
        #if cmd is not None
      #for icmdidx in range(0, icmdcnt)
    #if icmdcnt > 0


    return irs


  def checkiCommand(self, iindex):
    brs = False

    cmd =  self.getiCommand(iindex)

    if cmd is not None :
      if cmd.isRunning():
        brs = cmd.Check()

    return brs


  def Check(self):
    irs = 0
    icmdcnt = len(self._arr_commands);

    if self._bdebug :
      self._arr_rpt.append("{} - go ...\n".format(sys._getframe(0).f_code.co_name))
      self._arr_rpt.append("arr cmd cnt: '{}'\n".format(icmdcnt))

    if icmdcnt > 0 :
      cmd = None
      scmdnm = None
      icmdidx = 0
      bchkgo = True

      stmnow = None

      while bchkgo \
      and icmdidx < icmdcnt :
        cmd = self._arr_commands[icmdidx]

        if cmd is not None :
          scmdnm = cmd.getNameComplete()

          if self._bdebug :
            self._arr_rpt.append("Sub Process {}: checking ...\n".format(scmdnm))

          if cmd.isRunning():
            if cmd.Check():
              #Count the Running Child Processes
              irs += 1
            else :  #The Child Process has finished
              stmnow = datetime.now().strftime('%F %T')

              self._arr_rpt.append("{} : Sub Process {}: finished with [{}]\n"\
              .format(stmnow, scmdnm, cmd.status))

              #cmd.freeResources()
            #if cmd.Check()

            if self._execution_timeout > -1 :
              if time.time() - self._start_time > self._execution_timeout :
                #Stop the Checks on Execution Timeout
                bchkgo = False

          else :  #The Sub Process is already finished
            if cmd.getProcessID() > 0 :
              if self._bdebug :
                self._arr_rpt.append("Sub Process {}: already finished with [{}]\n"\
                .format(scmdnm, cmd.status))

              #cmd.freeResources()
            #if cmd.getProcessID() > 0
          #if cmd.isRunning()
        #if cmd is not None

        icmdidx  += 1

      #while bchkgo and icmdidx < icmdcnt
    #if icmdcnt > 0

    #Count of the Running Child Processes
    return irs


  def Wait(self, options = {}):
    #At least check the Child Processes once
    irng = 1
    brs = False

    itmchk = -1
    itmchkstrt = -1
    itmchkend = -1
    itmrng = -1
    itmrngstrt = -1
    itmrngend = -1

    if self._bdebug :
      self._arr_rpt.append("{} - go ...\n".format(sys._getframe(0).f_code.co_name))

    if len(options) > 0 :
      self.setDictOptions(options)

    if self._start_time < 1 :
      #Set the Start Time if it is not set yet
      self._start_time = time.time()

    #As long as there are Running Child Processes
    while irng > 1 :
      if self._check_interval > -1 \
      or self._execution_timeout > -1 :
        if itmchkstrt < 1 :
          #Take the Time measured at Launch Time
          itmchkstrt = self._start_time
        else :  #It is not the first Check
          itmchkstrt = time.time()

        if self._execution_timeout > -1 :
          if itmrngstrt < 1 :
            itmrng = 0
            itmrngstrt = itmchkstrt

        #if self._execution_timeout > -1
      #if self._check_interval > -1 or self._execution_timeout > -1

      #Check the Child Processes
      irng = self.Check()

      if irng > 0 :
        if self._check_interval > -1 \
        or self._execution_timeout > -1 :
          itmchkend = time.time()
          itmrngend = itmchkend

          itmchk = itmchkend - itmchkstrt
          itmrng = itmrngend - itmrngstrt

          if self._bdebug :
            self._arr_rpt.append("wait - tm rng: '{}'; tm chk: '{}'\n".format(itmrng, itmchk))

          if self._execution_timeout > -1 \
          and itmrng >= self._execution_timeout :
            self._arr_err.append("Sub Processes 'Count: {}': Execution timed out!\n".format(irng))
            self._arr_err.append("Execution Time '{} / {}'\nProcesses will be terminated.\n"\
            .format(itmrng, self._execution_timeout))

            if self._err_code < 4 :
              self._err_code = 4

            self.Terminate()
            irng = -1
          #if self._execution_timeout > -1 and itmrng >= self._execution_timeout

          if irng > 0 \
          and itmchk < self._check_interval :
            if self._bdebug :
              self._arr_rpt.append("wait - sleep '{}' s ...\n".format(self._check_interval - itmchk))

            time.sleep(self._check_interval - itmchk)

        #if self._check_interval > -1 or self._execution_timeout > -1
      #if irng > 0
    #while irng > 1

    if irng == 0 :
      #Mark as Finished correctly
      brs = True
    elif irng < 0 :
      #Mark as Failed if the Sub Process was Terminated
      brs = False

    return brs


  def Run(self, options = {}):
    brs = False

    if self._bdebug :
      self._arr_rpt.append("{} - go ...\n".format(sys._getframe(0).f_code.co_name))

    if len(options) > 0 :
      self.setDictOptions(options)

    if self.Launch() :
      brs = self.Wait()
    else :  #Child Process Launch failed
      self._arr_err.append("Sub Processes: Process Launch failed!\n")

    return brs


  def Terminate(self):
    if self._bdebug :
      self._arr_rpt.append("'{}' : Signal to '{}'\n"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    self._arr_err.append("Sub Processes: Processes terminating ...\n")

    for cmd in self._arr_commands :
      if cmd.isRunning() :
        #Terminate the Child Process
        cmd.Terminate()

    #for cmd in self._arr_commands


  def Kill(self):
    if self._bdebug :
      self._arr_rpt.append("'{}' : Signal to '{}'\n"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    self._arr_err.append("Sub Processes: Processes killing ...\n")

    for cmd in self._arr_commands :
      if cmd.isRunning() :
        #Kill the Child Process
        cmd.Kill()

    #for cmd in self._arr_commands


  def freeResources(self):
    if self._bdebug :
      self._arr_rpt.append("'{}' : Signal to '{}'\n"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    for cmd in self._arr_commands :
      #Free all Child Processes System Resources
      cmd.freeResources()

    #for cmd in self._arr_commands


  def clearErrors(self):
    if self._bdebug :
      sdbgmsg = "'{}' : Call on '{}'\n"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name)

    for cmd in self._arr_commands :
      #Free all Child Processes System Resources
      cmd.clearErrors()

    #for cmd in self._arr_commands

    self._arr_rpt = []
    self._arr_err = []
    self._sreport = None
    self._serror = None
    self._err_code = 0

    self._time_start = -1

    if self._bprofiling :
      self._time_execution = -1
      self._time_end = -1

    if self._bdebug :
      #Readd last Debug Message
      self._arr_rpt.append(sdbgmsg)



  #----------------------------------------------------------------------------
  #Consultation Methods


  def getiCommand(self, iindex):
    rscmd = None

    try :
      iidx = int(iindex)
    except :
      #Index must be a positive whole Number
      iidx = -1

    if iidx > -1 \
    and iidx < len(self._arr_commands) :
      rscmd = self._arr_commands[iidx]

    return rscmd


  def getCheckInterval(self):
    return self._check_interval


  def getReadTimeout(self):
    return self._read_timeout


  def getTimeout(self):
    return self._execution_timeout


  def getCommandCount(self):
    return len(self._arr_commands)


  def getRunningCount(self):
    irng = 0

    for cmd in self._arr_commands :
      if cmd.isRunning() :
        irng += 1

    #for cmd in self._arr_commands

    return irng


  def getFreeCount(self):
    ifrrs = 0

    for cmd in self._arr_commands :
      if not cmd.isRunning() :
        ifrrs += 1

    #for cmd in self._arr_commands

    return ifrrs


  def getFinishedCount(self):
    ifnshd = 0

    for cmd in self._arr_commands :
      if not cmd.isRunning() \
      and cmd.getProcessID > 0 :
        #The Child Process was launched, has finished and was not reset yet
        ifnshd += 0

    #for cmd in self._arr_commands

    return ifnshd


  def getReportString(self):
    if self._sreport is None :
      self._sreport = ''.join(self._arr_rpt)

    return self._sreport


  def getErrorString(self):
    if self._serror is None :
      self._serror = ''.join(self._arr_err)

    return self._serror


  def getErrorCode(self):
    return self._err_code


  def isProfiling(self):
    return self._bprofiling


  def isDebug(self):
    return self._bdebug


  def isQuiet(self):
    return self._bquiet




  #-----------------------------------------------------------------------------------------
  #Properties


  len = property(getCommandCount)
  report = property(getReportString)
  error = property(getErrorString)
  code = property(getErrorCode)


