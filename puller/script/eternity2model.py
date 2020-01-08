#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Job Puller
#
#  Copyright © 2019 Yohan Firmy
#

import configparser
from enum import Enum

class SolverResult:
  def __init__(self, result, resultDate):
    self.board = result
    self.date = resultDate

class SolverInfo:
  def __init__(self, config, solver):
      self.name = config.get('Solver', 'name')
      self.version = "1.8.0"
      self.machineType = config.get('Solver', 'machine.type')
      self.clusterName = config.get('Solver', 'cluster.name')
      self.capacity, self.score = solver.check_solver_capacity()

class SolverStatus(Enum):
      STARTED = 1
      REQUESTING = 2
      WAITING = 3
      SOLVING = 4
      REPORTING = 5
      STOPPED = 6
