#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Job Puller
#
#  Copyright © 2019 Yohan Firmy
#

import re
import subprocess
import sys
import os
import requests
import configparser
import logging
import json
import signal
import time
from datetime import datetime

class Result:
  def __init__(self, result, resultDate):
    self.board = result
    self.date = resultDate

class SolverInfo:
  
  def __init__(self, config, solver):
      self.name = config.get('Solver', 'name')
      self.version = "1.7.2"
      self.machineType = config.get('Solver', 'machine.type')
      self.clusterName = config.get('Solver', 'cluster.name')
      self.capacity, self.score = solver.check_solver_capacity()

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
      returncode = process.poll()

      while returncode is None and resultsCount < self.resultsLimit:
        output = process.stdout.readline()
        returncode = process.poll()
        if output == '' and returncode is not None:
          break
        if output:
          line = output.decode('utf-8')
          self.process_line(line, foundResults)
          if len(foundResults) >= self.resultsChunkSize:
             if submitter is not None:
                submitter(job, foundResults, solverInfo)
             resultsCount = resultsCount + len(foundResults)
             del foundResults[:]

      if returncode is not None:
        process.terminate()

      if resultsCount < self.resultsLimit and len(foundResults) > 0:
        if submitter is not None:
           submitter(job, foundResults, solverInfo)
        resultsCount = resultsCount + len(foundResults)
      del foundResults[:]
      
      return resultsCount

  def process_line(self, line, foundResults):
      logging.debug(line)
      if(line.startswith(self.nextResultLinePattern)):
        solution = re.sub(self.resultLinePattern, r"\1", line)
        foundResults.append(Result(solution.rstrip(), now()))

  def check_solver_capacity(self):
    logging.info('Solver performance test at startup:')
    starttime = time.time()
    self.solve(self.evaluationJob, None, None)
    delay = time.time() - starttime
    logging.info('This solver can solve the reference job in '+str(delay)+' seconds (reference time is '+str(self.referenceTime)+' sec)')
    if delay < ( self.referenceTime / 2 ) :
      category = 'much faster'
      jobCapacity = self.defaultJobCapacity + 2
    if delay < ( self.referenceTime - 2 ) :
      category = 'faster'
      jobCapacity = self.defaultJobCapacity + 1
    if delay >= ( self.referenceTime - 2 ) and delay <= ( self.referenceTime + 2 ):
      category = 'reference'
      jobCapacity = self.defaultJobCapacity
    if delay > ( self.referenceTime + 2 ):
      category = 'slower'
      jobCapacity = self.defaultJobCapacity - 1
    if delay > ( self.referenceTime * 2 ):
      category = 'much slower'
      jobCapacity = self.defaultJobCapacity - 2
    logging.info('This solver speed class: '+category)
    logging.info('Solver job capacity: '+str(jobCapacity))
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

class E2ServerWrapper:
  
  def __init__(self, config):
      self.basepath = config.get('Server', 'basepath')
      api_path = "api/eternity2-server/v1/"
      self.user = config.get('Server', 'user')
      self.password = self.read_password(config)
      self.url_jobs = self.basepath + api_path + "jobs?size={}"
      self.url_result = self.basepath + api_path + "result"
      self.url_status = self.basepath + api_path + "status"
      self.url_health = self.basepath + "health"

  def read_password(self, config):
      with open( config.get('Server', 'password.file'), 'r') as file:
           password = file.read().replace('\n', '')
      return password

  def http_get(self, path):
      response = requests.get( path, auth=(self.user, self.password) )
      payload = response.json()
      response.raise_for_status()
      return payload

  def http_put(self, path, payload):
      headers = {'content-type': 'application/json'}
      response = requests.put(path, auth=(self.user, self.password), data=payload, headers=headers)
      response.raise_for_status()

  def http_post(self, path, payload):
      headers = {'content-type': 'application/json'}
      response = requests.post(path, auth=(self.user, self.password), data=payload, headers=headers)
      response.raise_for_status()

  def retrieve_jobs(self, jobSize):
      logging.info("Retrieving Jobs of size {}".format(jobSize))
      response = self.http_get( self.url_jobs.format(jobSize) )
      jobs = []
      if len(response)>0:
          logging.info("Received {} jobs:".format(len(response)))
          for item in response:
            job = item.get("job")
            logging.info(job)
            jobs.append( job )
      else:
          logging.info("No jobs received.")
      return jobs 

  def lock(self, job, retrievalDate, solverInfo):
      logging.info("Acquiring lock for job {}".format(job))
      self.http_put( self.url_status, self.buildLockPayload(job, retrievalDate, solverInfo) )

  def submit(self, job, results, solverInfo):
      logging.info("Submitting {} results for job {}".format(len(results), job))
      self.http_post( self.url_result, self.buildResultsPayload(job, results, solverInfo) )

  def buildResultsPayload(self, job, results, solverInfo):
      body = {"solver": {"name": solverInfo.name, "version": solverInfo.version, "machineType": solverInfo.machineType, "clusterName": solverInfo.clusterName, "score": solverInfo.score}, "job": job, "solutions": [], "dateJobTransmission": now() }
      for result in results:
        body.get("solutions").append( {"solution": result.board, "dateSolved": result.date} )
      payload = json.dumps(body)
      logging.debug(payload)
      return payload

  def buildLockPayload(self, job, retrievalDate, solverInfo):
      body = {"solver": {"name": solverInfo.name, "version": solverInfo.version, "machineType": solverInfo.machineType, "clusterName": solverInfo.clusterName, "score": solverInfo.score}, "job": job, "status": "PENDING", "dateJobTransmission": retrievalDate, "dateStatusUpdate": now()}
      return json.dumps(body)

  def check_health(self):
      status = self.http_get( self.url_health )
      logging.debug("Server status = {}".format(str(status)))

class Application:

  def __init__(self, configuration_filename):
      self.config = configparser.ConfigParser(os.environ)
      self.config.read(configuration_filename)
      loglevel = self.config.get('Logger', 'level')
      logging.basicConfig(stream=sys.stdout, level=loglevel, format='%(asctime)s [%(levelname)-5s] %(name)s: %(message)s')
      logging.info("Eternity II Job Puller Script")
      self.solver = E2SolverWrapper(self.config)
      self.server = E2ServerWrapper(self.config)
      self.info = SolverInfo(self.config, self.solver)
      self.interruption_requested = False

  def main(self):

      jobSize = self.info.capacity

      while(not self.interrupted()):
          try:
              self.server.check_health()
              jobs = self.server.retrieve_jobs(jobSize)
              retrievalDate = now()
              for job in jobs:
                  try:
                      self.server.lock( job, retrievalDate, self.info )
                      self.solver.solve( job, self.server.submit, self.info )
                      break
                  except requests.exceptions.HTTPError as e:
                    logging.error('Impossible to lock job ' + job)
                    logging.error(e)
              time.sleep(5)

          except Exception as e:
              logging.error('Impossible to reach the server (for health check or for job retrieval)')
              logging.error(e)
              logging.info('Waiting 60 seconds before retrying')
              time.sleep(60)

      logging.info("Interrupted. Goodbye.")

  def interrupted(self):
      return self.interruption_requested

  def request_interruption(self):
      logging.warning("Interruption requested")
      self.interruption_requested = True

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def receiveSignal(signalNumber, frame):
    logging.warning('Received: {}'.format(signalNumber))
    app.request_interruption()

def register_signals():
    signal.signal(signal.SIGTERM, receiveSignal)
    signal.signal(signal.SIGINT, receiveSignal)

def usage():
  print("usage: python pull/eternity2-job-puller.py --conf puller/conf/properties.ini")
  exit(1)

if __name__ == "__main__":

    if len(sys.argv)!=3 or sys.argv[1]!="--conf":
      usage()

    configuration_filename = sys.argv[2]
    register_signals()
    app = Application(configuration_filename)
    app.main()