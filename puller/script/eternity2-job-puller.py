#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Job Puller
#
#  Copyright © 2019 Yohan Firmy
#

import sys
import os
import requests
import configparser
import logging
import signal
import time
import random
from eternity2utils import *
from eternity2model import *
from eternity2solver import E2SolverWrapper
from eternity2server import E2ServerWrapper

class Application:

  def __init__(self, configuration_filename):
      self.config = configparser.ConfigParser(os.environ)
      self.config.read(configuration_filename)
      loglevel = self.config.get('Logger', 'level')
      logging.basicConfig(stream=sys.stdout, level=loglevel, format='%(asctime)s [%(levelname)-5s] %(name)s: %(message)s')
      logging.info("Eternity II Job Puller Script")
      self.solver = E2SolverWrapper(self.config)
      self.server = E2ServerWrapper(self.config)
      self.server.postEvent( self.config.get('Solver', 'name'), SolverStatus.STARTED )
      self.info = SolverInfo(self.config, self.solver)
      self.interruption_requested = False
      self.retryCount = 0
      self.currentJob = None

  def main(self):

      jobSize = self.info.capacity

      while(not self.interrupted()):
          try:
              self.server.check_health()
              self.server.postEvent( self.info.name, SolverStatus.REQUESTING )
              jobs = self.server.retrieve_jobs(jobSize)
              retrievalDate = now()
              for job in jobs:
                  try:
                      self.server.lock( job, retrievalDate, self.info )
                      self.currentJob = job
                      self.server.postEvent( self.info.name, SolverStatus.SOLVING )
                      self.solver.solve( job, self.server.submit, self.info )
                      self.currentJob = None
                      self.retryCount = 0
                      break
                  except requests.exceptions.HTTPError as e:
                    logging.error('Impossible to lock job ' + job)
                    logging.error(e)

              self.server.postEvent( self.info.name, SolverStatus.WAITING )
              time.sleep(5)

          except Exception as e:
              logging.error('Impossible to reach the server (for health check or for job retrieval)')
              logging.error(e)
              waitingDelay = 60+(self.retryCount*30)+random.randrange(20)
              self.retryCount = self.retryCount+1
              logging.info('Waiting '+str(waitingDelay)+' seconds before retrying ('+str(self.retryCount)+')')
              self.server.postEvent( self.info.name, SolverStatus.WAITING )
              time.sleep(waitingDelay)

      logging.info("Interrupted. Goodbye.")

  def interrupted(self):
      return self.interruption_requested

  def giveup_current_job(self):
      self.server.giveup( self.currentJob, self.info )

  def request_interruption(self):
      logging.warning("Interruption requested")
      self.interruption_requested = True
      self.giveup_current_job()
      self.server.postEvent( self.info.name, SolverStatus.STOPPED )

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