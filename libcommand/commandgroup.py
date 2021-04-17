'''
This Module provides the `CommandGroup` Class which manages multiple `Command` objects.
It executes and monitores the `Command` objects.

:version: 2021-04-17

:author: Bodo Hugo Barwich
'''
__docformat__ = "restructuredtext en"

import math

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
      self._check_interval = icheckinterval
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
      self._read_timeout = ireadtimeout
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
      self._execution_timeout = iexecutiontimeout
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





