#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Job Puller
#
#  Copyright © 2019 Yohan Firmy
#

import requests
import configparser
import logging
import json
from eternity2utils import *

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

