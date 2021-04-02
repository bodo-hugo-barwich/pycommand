'''
Tests to verify the Command Class Functionality

@version: 2021-04-02

@author: Bodo Hugo Barwich
'''
import sys
import unittest
import os

sys.path.append("../libcommand")

from libcommand import Command



class TestCommand(unittest.TestCase):


  def setUp(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))
    print("setUp - Test Directory: '{}'".format(os.getcwd()))
    print("setUp - Test Module: '{}'\n".format(__file__))
    print("")


  def tearDown(self):
    pass


