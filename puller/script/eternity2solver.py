#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Job Puller
#
#  Copyright © 2019 Yohan Firmy
#

import re
import subprocess
import configparser
import time
import logging
import json
from eternity2utils import *

class E2SolverWrapper:

  def __init__(self, config):
      self.boardSize = int(config.get('Board', 'size'))
      self.command = config.get('Solver', 'command')
      self.resultLinePattern = config.get('Solver', 'solution.pattern')
      self.beginResultLinePattern = config.get('Solver', 'solution.beginning.pattern')
      self.nextResultLinePattern = config.get('Solver', 'solution.following.pattern')
      self.resultsChunkSize = int(config.get('Solver', 'results.chunk.size'))
      self.resultsLimit = int(config.get('Solver', 'results.limit.per.job'))
      self.evaluationJob = config.get('Solver', 'performance.evaluation.job')
      self.referenceTime = int(config.get('Solver', 'performance.reference.time'))
      self.defaultJobCapacity  =int(config.get('Solver', 'default.job.capacity'))
      self.jobPattern = r'\$((\d{1,3}[WNES]\:)|(\.\:)){'+str(self.boardSize)+r'};'

  def fatal(self, message):
      logging.critical(message)
      exit(1)

  def check(self, job):
      if not re.match(self.jobPattern, job ):
        self.fatal("bad request: the given job is malformed.")

  def execute_command(self, command, job, submitter, solverInfo):
      logging.debug(command)
      process = subprocess.Popen([command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      inputJob = job+'\nexit\n'
      process.stdin.write(inputJob.encode('utf-8'))
      process.stdin.close()

      foundResults = []
      resultsCount = 0
      output = process.stdout.readline()
      returncode = process.poll()

      while output is not None and returncode is None and resultsCount < self.resultsLimit:

        if len(output.strip()) > 0:
          self.process_line( output.decode('utf-8').strip(), foundResults)

        if len(foundResults) >= self.resultsChunkSize:
          if submitter is not None:
            submitter(job, foundResults, solverInfo)
          resultsCount = resultsCount + len(foundResults)
          del foundResults[:]

        output = process.stdout.readline()
        returncode = process.poll()

      if returncode is not None:
        process.terminate()

      if submitter is not None:
        submitter(job, foundResults, solverInfo)

      resultsCount = resultsCount + len(foundResults)
      del foundResults[:]
      
      return resultsCount

  def process_line(self, line, foundResults):
      logging.debug('Solver output: [' + line + ']')
      if(line.startswith(self.nextResultLinePattern)):
        solution = re.sub(self.resultLinePattern, r"\1", line)
        foundResults.append(SolverResult(solution.rstrip(), now()))

  def check_solver_capacity(self):
    logging.info('Solver performance test at startup:')
    starttime = time.time()
    self.solve(self.evaluationJob, None, None)
    delay = time.time() - starttime
    logging.info('This solver can solve the reference job in '+str(delay)+' seconds (reference time is '+str(self.referenceTime)+' sec)')
    jobCapacity = self.defaultJobCapacity
    return jobCapacity, ( delay / self.referenceTime )

  def solve(self, job, submitter, solverInfo):
    self.check(job)
    logging.info("Solving job {}".format(job))
    resultsCount = self.execute_command( self.command, job, submitter, solverInfo )
    logging.info("Finished solving")
    if resultsCount > 0:
      logging.info("Found {} results.".format(resultsCount))
    else:
      logging.info("No result")
