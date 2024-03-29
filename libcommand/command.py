'''
This Module provides the `Command` Class which launches a Single Child Process
in asynchronous Mode and captures possible Errors.

:version: 2021-10-17

:author: Bodo Hugo Barwich
'''
__docformat__ = "restructuredtext en"

import sys
import subprocess
import selectors
import time
from shlex import split



#==============================================================================
# The Command Class


class Command(object):
  '''
  This is a Class launches a Child Process and reads its STDOUT and STDERR continuously
  and stores them in Memory

  It offers Methods to access the Result Output and possible Errors

  :see: `Command.report`
  :see: `Command.error`
  :see: `Command.status`
  :see: `Command.code`
  '''



  #----------------------------------------------------------------------------
  #Constructors


  def __init__(self, scommandline = None, options = {}):
    '''
    A `Command` Object can be instantiated with a `scommandline`
    `scommandline` is the executable plus the command line parameters passed to it

    :param scommandline: The commmand and its parameters to be executed in the child process
    :type scommandline: string
    :param options: Additional options for the execution as key - value pairs
    :type options: dictionary

    :see: `Command.setDictOptions`
    '''

    self._pid = -1
    self._name = ''
    self._scommand = ''
    self._process = None
    self._selector = None
    self._package_size = 8192
    self._read_timeout = 0
    self._execution_timeout = -1
    self._arr_rpt = []
    self._arr_err = []
    self._sreport = None
    self._serror = None
    self._err_code = 0
    self._process_status = -1
    self._time_execution = -1
    self._time_start = -1
    self._time_end = -1
    self._bprofiling = False
    self._bdebug = False

    if scommandline is not None :
      self._scommand = scommandline

    if len(options) > 0 :
      self.setDictOptions(options)


  def __del__(self):
    '''
    On Destruction any still running Child Processes are killed
    and the Lists of str Objects will be freed
    '''
    self.freeResources()

    self._arr_rpt = None
    self._arr_err = None



  #-----------------------------------------------------------------------------------------
  #Administration Methods


  def setDictOptions(self, options = {}):
    '''
    This Method configures the `Command` object from a dictionary in the parameter `options`.
    The recognized keys are:
    * `name` - user defined name of the object
    * `command` - the command to be run in the child process with its parameters
    * `check`|`read`|`readtimeout` - time in seconds to watch the child process
    * `timeout` - maximal execution time for the child process
    * `debug` - enable debug messages
    * `profiling` - enable time measurements

    The values `command` and `profiling` can only be set when the child process is not running yet

    :param options: Additional options for the execution as key - value pairs
    :type options: dictionary

    :see: `Command.read_timeout`
    :see: `Command.timeout`
    '''
    if('name' in options):
      #Set the Name
      self._name = options['name']

    if('check' in options):
      self.setReadTimeout(options['check'])

    if('read' in options):
      self.setReadTimeout(options['read'])

    if('readtimeout' in options):
      self.setReadTimeout(options['readtimeout'])

    if('timeout' in options):
      self.setTimeout(options['timeout'])

    if('debug' in options):
      self.setDebug(options['debug'])

    #Attributes that cannot be changed in Running State
    if(not self.isRunning()):
      if('command' in options):
        self.setCommand(options['command'])

      if('profiling' in options):
        self.setProfiling(options['profiling'])

    #if(not self.isRunning())


  def setName(self, sname = ''):
    self._name = sname


  def setCommand(self, scommandline = ''):
    #Attributes that cannot be changed in Running State
    if(not self.isRunning()):
      self._scommand = scommandline

      self._process = None
      self._pid = -1
      self._process_status = -1

    #unless($self->isRunning)



  def setReadTimeout(self, ireadtimeout = 1):
    if(ireadtimeout > -1):
      #Enable the Read Timeout
      self._read_timeout = ireadtimeout
    else:
      #Disable the Read Timeout
      self._read_timeout  = 0


  def setTimeout(self, iexecutiontimeout = -1):
    self._execution_timeout = iexecutiontimeout

    if(self._execution_timeout < -1):
      #Disable Execution Timeout
      self._execution_timeout = -1


  def setProfiling(self, bisprofiling = True):
    self._bprofiling = bisprofiling


  def setDebug(self, bisdebug = True):
    self._bdebug = bisdebug


  def Launch(self):
    '''
    This Method launches the process defined by the `Command.command_line` Property in a separate child process

    :returns: Returns `True` if the launch of the child process succeeded
    :rtype: boolean
    '''
    brs = False

    if self._scommand != '' :
      #------------------------
      #Execute the configured Command

      sprcnm = self.getNameComplete()
      #Parse the Command Line
      arrcmd = split(self._scommand)

      if self._bdebug :
        self._arr_rpt.append("cmd arr: '{}'\n".format(str(arrcmd)))

      self._pid = -1
      self._process_status = -1

      if self._bdebug :
        self._arr_rpt.append("cmd pfg '{}'\n".format(self._bprofiling))

      if self._bprofiling :
        self._time_start = time.time()

      try :
        #Launch the Child Process
        self._process = subprocess.Popen(arrcmd, bufsize = self._package_size, stdin = None\
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        self._pid = self._process.pid

        #Create Pipe IO Selector
        self._selector = selectors.DefaultSelector()

        self._selector.register(self._process.stdout, selectors.EVENT_READ, None)
        self._selector.register(self._process.stderr, selectors.EVENT_READ, None)

        brs = True

        if self._bdebug :
          self._arr_rpt.append("Sub Process {}: Launch OK - PID ({})\n"\
          .format(sprcnm, self._pid))
          self._arr_rpt.append("prc ({}) - stdout: '{}'\n".format(self._pid, str(self._process.stdout)))
          self._arr_rpt.append("prc ({}) - stderr: '{}'\n".format(self._pid, str(self._process.stderr)))

      except Exception as e :
        self._arr_err.append("Command '{}': Launch failed with {}!\n".format(sprcnm, e.__class__.__name__))
        self._arr_err.append("Exception [{}] Message: {}\n".format(e.errno, str(e)))
        self._err_code = 1
        self._process_status = e.errno
        self._process = None

    #if self._scommand != ''

    return brs



  def Check(self):
    '''
    This Method checks whether the child process is still running and reads
    its Output and Errors with the `Read()` Method

    :returns: Returns `True` if the child process is still running
    :rtype: boolean

    :see: `Command.Read()`
    '''

    brng = False

    if self._process is not None :
      if self._process.poll() is not None :
        #------------------------
        #Child Process has finished

        #Read the Process Status Code
        self._process_status = self._process.returncode

        if self._bdebug :
          self._arr_rpt.append("prc ({}): finished with [{}].\n".format(self._pid, self._process_status))

        if self._bprofiling :
          self._time_end = time.time()

          self._time_execution = self._time_end - self._time_start

          if self._bdebug :
            self._arr_rpt.append("Time Execution: '{}' s\n".format(self._time_execution))

        #if(self._bprofiling)

        if self._bdebug :
          self._arr_rpt.append("prc ({}) [{}]: Read do ...\n".format(self._pid, self._process_status))

        #Read the Last Messages from the Sub Process
        self.Read()

        #Free the Pipe Selector Resources
        self._freeSelector()

      else :
        #------------------------
        #The Child Process is running

        brng = True

        if self._bdebug :
          self._arr_rpt.append("prc ({}) [{}]: Read do ...\n".format(self._pid, self._process_status))

        #Read the Messages from the Sub Process
        self.Read()

      #if self._process.poll() is not None
    #if self._process is not None

    return brng


  def Read(self):
    '''
    This Method checks whether there is data available on the STDOUT and STDERR pipes
    and reads any available data.
    The collected data can be read with the `getReportString()` and `getErrorString()` Methods

    :see: `Command.getReportString()`
    :see: `Command.getErrorString()`
    '''
    if(self._sreport is not None):
      self._sreport = None

    if(self._serror is not None):
      self._serror = None

    if self._process is not None :
      if self._bdebug :
        self._arr_rpt.append("prc ({}) [{}]: try read ...\n".format(self._pid, self._process_status))

      events = self._selector.select(self._read_timeout)
      scnk = None
      brd = True

      if self._bdebug :
        self._arr_rpt.append("prc ({}): '{}' read events\n".format(self._pid, len(events)))

      for key in events:
        if self._bdebug :
          self._arr_rpt.append("prc ({}) - event: '{}'\n".format(self._pid, str(key[0])))

        if key[0].fileobj == self._process.stdout :
          #------------------------
          #Read STDOUT

          if self._bdebug :
            self._arr_rpt.append("pipe ({}): reading report ...\n".format(key[0].fd))

          scnk = self._process.stdout.read1(self._package_size) #-1

          if scnk is not None :
            scnk = str(scnk, sys.stdout.encoding)

            if scnk != '' :
              self._arr_rpt.append(scnk)
            else :
              brd = False
          else :
            brd = False

          if not brd :
            if self._bdebug :
              self._arr_rpt.append("pipe ({}): transmission done.\n".format(key[0].fd))

            self._selector.unregister(self._process.stdout)
            self._process.stdout.close()

        elif key[0].fileobj == self._process.stderr :
          #------------------------
          #Read STDERR

          if self._bdebug :
            self._arr_rpt.append("pipe ({}): reading error ...\n".format(key[0].fd))

          scnk = self._process.stderr.read1(self._package_size) # -1

          if scnk is not None :
            scnk = str(scnk, sys.stderr.encoding)

            if scnk != '' :
              self._arr_err.append(scnk)
            else :
              brd = False
          else :
            brd = False

          if not brd :
            if self._bdebug :
              self._arr_rpt.append("pipe ({}): transmission done.\n".format(key[0].fd))

            self._selector.unregister(self._process.stderr)
            self._process.stderr.close()

      #for key in events

      if self._bdebug :
        self._arr_rpt.append("prc ({}): reading done.\n".format(self._pid))

    #if self._process is not None


  def Wait(self):
    '''
    This Method continuously checks whether the child process is still running with the `Check()` Method.
    If an Execution Timeout is established the child process is terminated when the time limit is reached

    :returns: Returns `True` if the child process has finished correctly
    :rtype: boolean

    :see: `Command.Check()`
    '''
    irng = 1
    brs = False

    sprcnm = self.getNameComplete()

    itmrng = -1
    itmrngstrt = -1
    itmrngend = -1

    if(self._execution_timeout > -1):
      itmrng = 0
      itmrngstrt = time.time()

    while(irng > 0):

      #Check the Sub Process
      irng = int(self.Check())

      if(irng > 0):
        if(self._execution_timeout > -1):
          itmrngend = time.time()

          itmrng = itmrngend - itmrngstrt

          if self._bdebug :
            self._arr_rpt.append("wait tm rng: '{}'\n".format(itmrng))

          if itmrng >= self._execution_timeout :
            self._arr_err.append("Sub Process {}: Execution timed out!\n".format(sprcnm))
            self._arr_err.append("Execution Time '{} / {}'\n".format(itmrng, self._execution_timeout))
            self._arr_err.append("Process will be terminated.\n")

            if(self._err_code < 4):
              self._err_code = 4

            #Terminate the Timed Out Sub Process
            self.Terminate()

            #Try to reap the Sub Process again
            if self.Check() :
              #Kill the blocked Sub Process
              self.Kill()

            #Mark the Sub Process as finished with Error
            irng = -1

          #if(itmrng >= self._execution_timeout)
        #if(self._execution_timeout > -1)
      # if(irng > 0)
    #while(irng > 0):

    if(irng == 0):
      #Mark as Finished correctly
      brs = True

    return brs


  def Terminate(self):
    sprcnm = self.getNameComplete()

    if self._bdebug :
      self._arr_rpt.append("'{}' : Signal to '{}'\n"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    if self.isRunning():
      self._arr_err.append("Sub Process {}: Process terminating ...\n".format(sprcnm))

      if self._process is not None :
        self._process.terminate()

      self.Check()
    else :  #Sub Process is not running
      self._arr_err.append("Sub Process ${sprcnm}: Process is not running.\n".format(sprcnm))


  def Kill(self):
    sprcnm = self.getNameComplete()

    if self._bdebug :
      self._arr_rpt.append("'{}' : Signal to '{}'\n"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    if self.isRunning() :
      self._arr_err.append("Sub Process {}: Process killing ...\n".format(sprcnm))
      print("Sub Process {}: Process killing ...\n".format(sprcnm))

      if self._process is not None :
        self._process.kill()

      #Mark Process as have been killed
      self._process_status = 4

      if self._err_code < 4 :
        self._err_code = 4

    else :  #Sub Process is not running
      self._arr_err.append("Sub Process ${sprcnm}: Process is not running.\n".format(sprcnm))


  def _freeSelector(self):
    if self._bdebug :
      self._arr_rpt.append("'{}' : Signal to '{}'\n"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    #Resource can only be freed if the Sub Process has terminated
    if not self.isRunning() :
      if self._selector is not None :
        pipes = list(self._selector.get_map().keys())

        #print("pipes list: '{}'".format(str(pipes)))

        for pp in pipes :
          key = self._selector.get_key(pp)

          #print("key: '{}'".format(str(key)))

          if self._bdebug :
            self._arr_rpt.append("pipe ({}): not closed. Closing now ...\n".format(key.fd))

          self._selector.unregister(key.fileobj)
          key.fileobj.close()

        #for pp in pipes

        self._selector.close()
        self._selector = None



  def freeResources(self):
    if self._bdebug :
      self._arr_rpt.append("'{}' : Signal to '{}'\n"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    if self.isRunning() :
      #Kill a still running Sub Process
      self.Kill()

    #Free the Pipe Selector Resources
    self._freeSelector()

    #Free the Sub Process Object
    self._process = None


  def clearErrors(self):

    self._pid = -1
    self._process_status = -1

    self._arr_rpt = []
    self._arr_err = []
    self._sreport = None
    self._serror = None
    self._err_code = 0

    if self._bprofiling :
      self._time_execution = -1
      self._time_start = -1
      self._time_end = -1



  #-----------------------------------------------------------------------------------------
  #Consultation Methods


  def getProcessID(self):
    return self._pid


  def getName(self):
    return self._name


  def getNameComplete(self):
    rsnm = ''

    if self._pid > -1 :
      #The Process is running
      #Identify the Process by its PID if it is running
      if self._name != '' :
        #Add its Name
        rsnm = "({}) '{}'".format(self._pid, self._name)
      else :
        #Add its Command
        rsnm = "({}) '{}'".format(self._pid, self._scommand)

    else :  #The Process is not running
      if self._name != '' :
        #Identify the Process by its Name
        rsnm = "'{}'".format(self._name)
      else :
        #Identify the Process by its Command
        rsnm = "'{}'".format(self._scommand)

    return rsnm


  def getCommand(self):
    return self._scommand


  def getReadTimeout(self):
    '''
    Command.read_timeout Property which represents the time in seconds which the `Command` object
    will wait for output from the child process.
    This must be a positive Integer. Negative Integers are interpreted with the value "0"

    :returns: Time in seconds to watch the child process
    :rtype: integer
    '''
    return self._read_timeout


  def getTimeout(self):
    '''
    Command.timeout Property which represents the time in seconds after which the `Command` object
    must forcefully terminate the child process.
    By default this is disabled with the value of "-1"

    :returns: Time in seconds before forcefully terminating the child process
    :rtype: integer
    '''
    return self._execution_timeout


  def isRunning(self):
    '''
    This Method reports whether the Child Process is still running

    :returns: Whether the Child Process is still running
    :rtype: boolean
    '''
    brng = False

    #The Process got a Process ID but did not get a Process Status Code yet
    if self._pid > 0 and self._process_status == -1 :
      brng = True

    return brng


  def getReportString(self):
    '''
    Command.report Property which represents all Report Messages

    :returns: All Report Messages as single String joined seamlessly
    :rtype: string
    '''
    if self._sreport is None :
      self._sreport = ''.join(self._arr_rpt)

    return self._sreport


  def getErrorString(self):
    '''
    Command.error Property which represents all Error Messages

    :returns: All Error Messages as single String joined seamlessly
    :rtype: string
    '''
    if self._serror is None :
      self._serror = ''.join(self._arr_err)

    return self._serror


  def getErrorCode(self):
    '''
    Command.code Property which holds the highest Error Code.
    On successful execution this is "0" and on error this is a positive Integer
    This value is populated by the `Command` library

    :returns: The Highest recorded Error Code
    :rtype: integer
    '''
    return self._err_code


  def getProcessStatus(self):
    '''
    Command.status Property which holds the child process Exit Code.
    This value is populated by the child process according to its logic.
    On a running child process this is "-1" and on a finished child process this holds the Exit Code
    according to the child process logic
    On a killed process this will also be "-1" when no Exit Code could be read.
    Mostly `Command.code` will hold the Error Code "4" then

    :returns: The Child Process Exit Code
    :rtype: integer
    '''
    return self._process_status


  def getExecutionTime(self):
    return self._time_execution


  def isProfiling(self):
    return self._bprofiling


  def isDebug(self):
    return self._bdebug



  #-----------------------------------------------------------------------------------------
  #Properties


  name = property(getName, setName)
  command_line = property(getCommand, setCommand)
  read_timeout = property(getReadTimeout, setReadTimeout)
  timeout = property(getTimeout, setTimeout)
  execution_time = property(getExecutionTime)
  profiling = property(isProfiling, setProfiling)
  debug = property(isDebug, setDebug)
  report = property(getReportString)
  error = property(getErrorString)
  code = property(getErrorCode)
  status = property(getProcessStatus)
