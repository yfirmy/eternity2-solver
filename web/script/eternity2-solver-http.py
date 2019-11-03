#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Solver REST API for Breadth-First Search
#
#  Copyright © 2019 Yohan Firmy
#

from flask import Flask, abort
import sys
import re
import subprocess
import configparser

app = Flask(__name__)
config = configparser.ConfigParser()

class E2SolverExecutor:

    def __init__(self, job):
        self.job = job
        self.boardSize = int(config.get('Board', 'size'))
        self.command = config.get('Solver', 'command')
        self.resultLinePattern = config.get('Solver', 'pattern')
        self.beginResultLinePattern = config.get('Solver', 'beginning.pattern')
        self.nextResultLinePattern = config.get('Solver', 'following.pattern')
        self.jobPattern = r"\$((\d{1,3}[WNES]\:)|(\.\:)){"+str(self.boardSize)+"};"

    def run(self):
      self.check_job()
      rawResults = self.execute_command( self.command, [self.job] )
      foundResults = self.parse_results( [self.job], rawResults)
      return foundResults[self.job]

    def check_job(self):
      if not re.match(self.jobPattern, self.job ):
        abort(400, "bad request: the given job is malformed.")

    def execute_command(self, command, jobs):
      p = subprocess.Popen([command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      commandline = '\n'.join(jobs)+'\nexit\n'
      (stdoutData, stderrData) = p.communicate(commandline.encode('utf-8'))
      return stdoutData.decode("utf-8")

    def parse_result(self, line, foundSolutionsList):
      solution = re.sub(self.resultLinePattern, r"\1", line)
      foundSolutionsList.append(solution)

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

def toJSON(results):
  return "[" + ', '.join(map( lambda job : "{\"job\": \""+job+"\"}", results )) + "]"

@app.route("/api/eternity2-solver/v1/sub-jobs/<job>")
def subjobs(job):
    executor = E2SolverExecutor(job)
    results = executor.run()
    response = app.response_class(
        response = toJSON(results),
        status = 200,
        mimetype = 'application/json'
    )
    return response

@app.route("/api/eternity2-solver/v1/health")
def health():
    response = app.response_class(
        response = "{\"status\": \"UP\"}",
        status = 200,
        mimetype = 'application/json'
    )
    return response

def usage():
  print("usage: python web/eternity2-solver-http.py --conf web/conf/properties.ini")
  exit(1)

if __name__ == "__main__":

     if len(sys.argv)!=3 or sys.argv[1]!="--conf":
       usage()

     config.read(sys.argv[2])
     app.run(host='0.0.0.0', port=int(config.get('Server', 'port')))
