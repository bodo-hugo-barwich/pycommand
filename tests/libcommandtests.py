'''
Tests to verify the Command Class Functionality

@version: 2021-04-02

@author: Bodo Hugo Barwich
'''
import sys
import os
import unittest

sys.path.append("../")
sys.path.append("../libcommand")

from libcommand import *
from libcommand import runCommand




class TestCommand(unittest.TestCase):

  _stestscript = 'test_script.py'
  _itestpause = 3
  _iteststatus = 4


  def setUp(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))
    print("setUp - Test Directory: '{}'".format(os.getcwd()))
    print("setUp - Test Module: '{}'\n".format(__file__))
    print("")


  def tearDown(self):
    pass


  def test_RunCommand(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))


    arrrs = runCommand("{} {} {}".format(self._stestscript, self._itestpause, self._iteststatus))


    print("EXIT CODE: '", arrrs[2], "'");

    self.assertFalse(arrrs[0] == '', "STDOUT was not captured.\n")

    print("STDOUT: '", arrrs[0], "'");

    self.assertFalse(arrrs[1] == '', "STDERR was not captured.\n")

    print("STDERR: '", arrrs[1], "'");


    print("")


