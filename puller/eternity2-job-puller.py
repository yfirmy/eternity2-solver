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

class E2SolverWrapper:

  def __init__(self, config):
      self.boardSize = int(config.get('Board', 'size'))
      self.command = config.get('Solver', 'command')
      self.resultLinePattern = config.get('Solver', 'solution.pattern')
      self.beginResultLinePattern = config.get('Solver', 'solution.beginning.pattern')
      self.nextResultLinePattern = config.get('Solver', 'solution.following.pattern')
      self.jobPattern = r'\$((\d{1,3}[WNES]\:)|(\.\:)){'+str(self.boardSize)+r'};'

  def fatal(self, message):
      logging.critical(message)
      exit(1)

  def check(self, job):
      if not re.match(self.jobPattern, job ):
        self.fatal("bad request: the given job is malformed.")

  def execute_command(self, command, jobs):
      p = subprocess.Popen([command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      (stdoutData, stderrData) = p.communicate('\n'.join(jobs)+'\nexit\n')
      return stdoutData.decode("utf-8")

  def parse_result(self, line, foundSolutionsList):
      solution = re.sub(self.resultLinePattern, r"\1", line)
      foundSolutionsList.append(Result(solution, now()))

  def parse_results(self, initialboards, results): 
      foundResults = {}
      idxInitialBoard = -1
      for initialboard in initialboards:
        foundResultsList = []
        foundResults[initialboard]=foundResultsList

      for line in results.split("\n") :
        if(line.startswith(self.beginResultLinePattern)):
          idxInitialBoard = idxInitialBoard+1
          foundResultsList = foundResults[initialboards[idxInitialBoard]]
          self.parse_result(line, foundResultsList)
        else:
          if(line.startswith(self.nextResultLinePattern)):
            foundResultsList = foundResults[initialboards[idxInitialBoard]]
            self.parse_result(line, foundResultsList)
      return foundResults 

  def check_solver_capacity(self):
  	return 24

  def solve(self, job):
    self.check(job)
    logging.info("Solving job {}".format(job))
    rawResults = self.execute_command( self.command, [job] )
    foundResults = self.parse_results( [job], rawResults)
    logging.info("Finished solving")
    if foundResults[job] is not None and len(foundResults[job])>0:
      logging.info("Found results:\n{}".format( "\n".join( map(lambda r: r.board, foundResults[job]) )))
    else:
      logging.info("No result")
    return foundResults[job]


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

  def lock(self, job, retrievalDate):
      logging.info("Acquiring lock for job {}".format(job))
      self.http_put( self.url_status, self.buildLockPayload(job, retrievalDate) )

  def submit(self, job, results):
      logging.info("Submitting results for job {}".format(job))
      self.http_put( self.url_result, self.buildResultsPayload(job, results) )

  def buildResultsPayload(self, job, results):
      body = {"job": job, "solutions": [], "dateJobTransmission": now() }
      for result in results:
        body.get("solutions").append( {"solution": result.board, "dateSolved": result.date} )
      return json.dumps(body)

  def buildLockPayload(self, job, retrievalDate):
      body = {"job": job, "status": "PENDING", "dateJobTransmission": retrievalDate, "dateStatusUpdate": now()}
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
      self.solver = E2SolverWrapper(self.config)
      self.server = E2ServerWrapper(self.config)
      self.interruption_requested = False

  def main(self):

      logging.info("Eternity II Job Puller Script")
      jobSize = self.solver.check_solver_capacity()

      self.server.check_health()

      while(not self.interrupted()):
          jobs = self.server.retrieve_jobs(jobSize)
          retrievelDate = now()
          for job in jobs:
              try:
                  self.server.lock( job, retrievelDate )
                  results = self.solver.solve( job )
                  self.server.submit( job, results )
                  break
              except requests.exceptions.HTTPError as e:
                logging.error('Impossible to lock job ' + job)
          time.sleep(5)

      logging.info("Interrupted. Goodbye.")

  def interrupted(self):
      return self.interruption_requested

  def request_interruption(self):
      logging.warning("Interruption requested")
      self.interruption_requested = True

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

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