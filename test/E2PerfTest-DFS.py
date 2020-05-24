#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Solver Performance Testing - Depth-First Search version
#
#  Copyright © 2009-2019 Yohan Firmy
#

import sys
import re
import unittest
import subprocess

class E2PerfTest(unittest.TestCase):

    def execute_commands(self, executable, commands):
      p = subprocess.Popen([executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      (stdoutData, stderrData) = p.communicate('\n'.join(commands)+'\nexit\n')
      return stdoutData.decode("utf-8")

    def execute_controlsample(self, commands):
      return self.execute_commands("bin/E2ControlSample-dfs", commands)

    def execute_worker(self, commands):
      return self.execute_commands("bin/E2Puzzle-dfs", commands)

    def execute_clue1(self, commands):
      return self.execute_commands("bin/E2Clue1-dfs", commands)

    def parse_solution(self, line, foundSolutionsList):
      solution = re.sub("^INFO Solution (?:\d)+ : (\$(?:(?:\.|(?:[0-9]{1,3}(?:N|W|E|S)))\:)+\;)", r"\1", line)
      foundSolutionsList.append(solution)

    def execute_ctrlsample_test(self, initialboards):
      results = self.execute_controlsample( initialboards )
      return self.parse_solutions(initialboards, results)

    def execute_challenge_test(self, initialboards):
      results = self.execute_worker( initialboards )
      return self.parse_solutions(initialboards, results)

    def execute_clue1_test(self, initialboards):
      results = self.execute_clue1( initialboards )
      return self.parse_solutions(initialboards, results)

    def parse_solutions(self, initialboards, results): 
      foundSolutions = {}
      idxInitialBoard = -1
      for initialboard in initialboards:
        foundSolutionsList = []
        foundSolutions[initialboard]=foundSolutionsList

      for line in results.split("\n") :
        if(line.startswith("INFO Solution 1 : ")):
          idxInitialBoard = idxInitialBoard+1
          foundSolutionsList = foundSolutions[initialboards[idxInitialBoard]]
          self.parse_solution(line, foundSolutionsList)
        else:
          if(line.startswith("INFO Solution ")):
            foundSolutionsList = foundSolutions[initialboards[idxInitialBoard]]
            self.parse_solution(line, foundSolutionsList)
      return foundSolutions

    def assert_solution_in_results(self, expectedSolution, foundResultsList, initialJob):
      errorMsg = "missing solution " + expectedSolution + " in the results for the job " + initialJob
      self.assertIn(expectedSolution, foundResultsList, errorMsg)

    def assert_solutions_count(self, expectedSolutionCount, foundResultsList, initialJob):
      errorMsg = str(len(foundResultsList)) + " solutions founds from job " + initialJob + "(expected "+ str(expectedSolutionCount)+" solutions)"
      self.assertEquals(expectedSolutionCount, len(foundResultsList), errorMsg)

    def skipped_test_clue1_performance(self):
      job1 = "$35S:27W:30S:12S:14W:33N:11S:34N:.:.:.:19N:9W:.:.:.:.:20S:10W:.:.:.:.:22S:6N:.:.:.:.:16W:25S:24S:15W:17S:21S:13S:;"
      foundSolutions = self.execute_clue1_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solutions_count(288768, foundSolutionsList, job1)

    def test_challenge_performance(self):
      job1 = "$3N:59E:57E:54E:48E:38E:53E:37E:52E:34E:55E:29E:43E:47E:35E:2E:18N:228S:224W:247N:90E:229E:89W:219E:245E:253S:158W:170N:238W:254W:99W:58S:19N:.:.:.:.:.:.:.:.:.:.:.:.:.:86E:22S:23N:.:.:.:.:.:.:.:.:.:.:.:.:.:121S:50S:7N:.:.:.:.:.:.:.:.:.:.:.:.:.:235S:17S:51N:.:.:.:.:.:.:.:.:.:.:.:.:.:107W:42S:12N:.:.:.:.:.:.:.:.:.:.:.:.:.:124E:46S:49N:.:.:.:.:.:.:.:.:.:.:.:.:.:230W:45S:11N:.:.:.:.:.:.:.:.:.:.:.:.:.:231E:33S:44N:.:.:.:.:.:.:.:.:.:.:.:.:.:202W:40S:10N:.:.:.:.:.:.:.:.:.:.:.:.:.:192E:20S:21N:.:.:.:.:.:.:.:.:.:.:.:.:.:209W:39S:5N:.:.:.:.:.:.:.:.:.:.:.:.:.:117W:13S:14N:.:.:.:.:.:.:.:.:.:.:.:.:.:131E:24S:6N:.:.:.:.:.:.:.:.:126W:141W:88S:73N:198W:252E:32S:1W:41W:4W:9W:36W:8W:25W:15W:26W:27W:28W:31W:30W:16W:56W:0S:;"
      foundSolutions = self.execute_challenge_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solutions_count(0, foundSolutionsList, job1)
      
if __name__ == '__main__':
    unittest.main()