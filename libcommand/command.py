'''
This Module provides the `Command` Class which launches a Single Child Process
in asynchronous Mode and captures possible Errors.

:version: 2020-08-25

:author: Bodo Hugo Barwich
'''
__docformat__ = "restructuredtext en"

import sys
import subprocess
import selectors
import time
from shlex import split



class Command(object):
  '''
  This is a Class launches a Child Process and reads its STDOUT and STDERR continously
  and stores them in Memory

  It offers Methods to access the Result Output and possible Errors
  '''



  #----------------------------------------------------------------------------
  #Constructors


  def __init__(self, commandline = None):
    '''
    A `Command` Object can be instantiated with a `commandline`
    `commmandline` is the executable plus the command line parameters passed to it

    :param commandline: The commmand to be executed in the child process
    :type commandline: string
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
    self._bdebug = False

    if commandline is not None :
      self._scommand = commandline




  #-----------------------------------------------------------------------------------------
  #Administration Methods


  def Launch(self):
    '''
    This Method launches the process defined by `commandline` in a separate child process

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
        self._arr_rpt.append("cmd: '{}'".format(self._scommand))

      self._pid = -1
      self._process_status = -1

      try :
        #Launch the Child Process
        self._process = subprocess.Popen(arrcmd, stdin = None\
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        self._pid = self._process.pid

        #Create Pipe IO Selector
        self._selector = selectors.DefaultSelector()

        self._selector.register(self._process.stdout, selectors.EVENT_READ, None)
        self._selector.register(self._process.stderr, selectors.EVENT_READ, None)

        brs = True

        if self._bdebug :
          self._arr_rpt.append("Sub Process {}: Launch OK - PID ({})"\
          .format(sprcnm, self._pid))

      except Exception as e :
        self._arr_err.append("Command '{}': Launch failed!".format(sprcnm))
        self._arr_err.append("Message: {}".format(str(e)))
        self._err_code = 1
        self._pid = -1
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
        #A Child Process has finished

        #Read the Process Status Code
        self._process_status = self._process.returncode

        if self._bdebug :
          self._arr_rpt.append("prc ({}): done.".format(self._pid))

        #Read the Last Messages from the Sub Process
        self.Read()

      else :
        #------------------------
        #The Child Process is running

        brng = True

        if self._bdebug :
          self._arr_rpt.append("prc ({}): Read checking ...".format(self._pid))

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

    if self._process is not None :
      if self._bdebug :
        self._arr_rpt.append("prc ({}) [{}]: try read ...".format(self._pid, self._process_status))

      events = self._selector.select(self._read_timeout)
      scnk = None
      brd = True

      for key in events:
        if key.fileobj == self._process.stdout :
          scnk = self._process.stdout.read(self._package_size)

          if self._bdebug :
            self._arr_rpt.append("pipe ({}): reading report ...".format(key.fd))

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
              self._arr_rpt.append("pipe ({}): transmission done.".format(key.fd))

            self._selector.unregister(self._process.stdout)

        elif key.fileobj == self._process.stderr :
          scnk = self._process.stderr.read(self._package_size)

          if self._bdebug :
            self._arr_rpt.append("pipe ({}): reading error ...".format(key.fd))

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
              self._arr_rpt.append("pipe ({}): transmission done.".format(key.fd))

            self._selector.unregister(self._process.stderr)


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

          if(self._bdebug):
            self._arr_rpt.append("wait tm rng: '{}'\n".format(itmrng))

          if(itmrng >= self._execution_timeout):
            self._arr_err.append("Sub Process {}: Execution timed out!\n".format(sprcnm))
            self._arr_err.append("Execution Time '{} / {}'\n".format(itmrng, self._execution_timeout))
            self._arr_err.append("Process will be terminated.\n")

            if(self._err_code < 4):
              self._err_code = 4

            #Terminate the Timed Out Sub Process
            self.Terminate()
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
      self._arr_err.append("'{}' : Signal to '{}'"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    if self.isRunning():
      self._arr_err.append("Sub Process {}: Process terminating ...".format(sprcnm))

      if self._process is not None :
        self._process.terminate()

      self.Check()
    else :  #Sub Process is not running
      self._arr_err.append("Sub Process ${sprcnm}: Process is not running.".format(sprcnm))


  def Kill(self):
    sprcnm = self.getNameComplete()

    if self._bdebug :
      self._arr_err.append("'{}' : Signal to '{}'"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    if self.isRunning() :
      self._arr_err.append("Sub Process {}: Process killing ...".format(sprcnm))

      if self._process is not None :
        self._process.kill()

      #Mark Process as have been killed
      self._process_status = 4

      if self._err_code < 4 :
        self._err_code = 4

    else :  #Sub Process is not running
      self._arr_err.append("Sub Process ${sprcnm}: Process is not running.".format(sprcnm))


  def freeResources(self):
    if self._bdebug :
      self._arr_rpt.append("'{}' : Signal to '{}'"\
      .format(sys._getframe(1).f_code.co_name, sys._getframe(0).f_code.co_name))

    if self.isRunning() :
      #Kill a still running Sub Process
      self.Kill()

    #Resource can only be freed if the Sub Process has terminated
    if not self.isRunning() :
      self._selector = None



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


  def getReadTimeout(self):
    return self._read_timeout


  def isRunning(self):
    brng = False

    #The Process got a Process ID but did not get a Process Status Code yet
    if self._pid > 0 and self._process_status < 0 :
      brng = True

    return brng


  def getReportString(self):
    if self._sreport is None :
      self._sreport = "\n".join(self._arr_rpt)

    return self._sreport


  def getErrorString(self):
    if self._serror is None :
      self._serror = "\n".join(self._arr_err)

    return self._serror


  def getErrorCode(self):
    return self._err_code


  def isDebug(self):
    return self._bdebug

