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
from shlex import split



class Command(object):
  '''
  This is a Class interact with a physical Text File in a easy and convenient way.

  It offers Methods read and write from and to the File
  '''



  #----------------------------------------------------------------------------
  #Constructors


  def __init__(self, commandline = None):
    '''
    A `Command` Object can be instanciated with a `commandline`
    '''

    self._pid = -1
    self._name = ''
    self._scommand = ''
    self._process = None
    self._selector = None
    self._package_size = 8192
    self._read_timeout = 0
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
    if self._scommand != '' :
      sprcnm = self.getNameComplete()
      arrcmd = split(self._scommand)

      self._pid = -1
      self._process_status = -1

      try :
        self._process = subprocess.Popen(arrcmd, stdin = None\
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        self._pid = self._process.pid

        self._selector = selectors.DefaultSelector()

        self._selector.register(self._process.stdout, selectors.EVENT_READ, None)
        self._selector.register(self._process.stderr, selectors.EVENT_READ, None)

      except Exception as e :
        self._arr_err.append("Command '{}': Launch failed!".format(sprcnm))
        self._arr_err.append("Message: {}".format(str(e)))
        self._err_code = 1
        self._process = None


  def Check(self):
    irng = 0

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

        irng = 1

        if self._bdebug :
          self._arr_rpt.append("prc ({}): Read checking ...\n".format(self._pid))

        #Read the Messages from the Sub Process
        self.Read()

    return irng


  def Read(self):
    if self._process is not None :
      if self._bdebug :
        self._arr_rpt.append("prc ({}) [{}]: try read ...\n".format(self._pid, self._process_status))

      events = self._selector.select(self._read_timeout)
      scnk = None
      brd = True

      for key in events:
        if key.fileobj == self._process.stdout :
          scnk = self._process.stdout.read(self._package_size)

          if self._bdebug :
            self._arr_rpt.append("pipe ({}): reading report ...\n".format(key.fd))

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
              self._arr_rpt.append("pipe ({}): transmission done.\n".format(key.fd))

            self._selector.unregister(self._process.stdout)

        elif key.fileobj == self._process.stderr :
          scnk = self._process.stderr.read(self._package_size)

          if self._bdebug :
            self._arr_rpt.append("pipe ({}): reading error ...\n".format(key.fd))

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
              self._arr_rpt.append("pipe ({}): transmission done.\n".format(key.fd))

            self._selector.unregister(self._process.stderr)





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
        rsnm = "({}) '{}'".format(self._pid, self._command)

    else :  #The Process is not running
      if self._name != '' :
        #Identify the Process by its Name
        rsnm = "'{}'".format(self._name)
      else :
        #Identify the Process by its Command
        rsnm = "'{}'".format(self._command)

    return rsnm


