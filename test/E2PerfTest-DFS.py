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

    def execute_worker_test(self, initialboards):
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

    def test_clue1_performance(self):
      job1 = "$35S:27W:30S:12S:14W:33N:11S:34N:.:.:.:19N:9W:.:.:.:.:20S:10W:.:.:.:.:22S:6N:.:.:.:.:16W:25S:24S:15W:17S:21S:13S:;"
      foundSolutions = self.execute_clue1_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solutions_count(288768, foundSolutionsList, job1)
      
if __name__ == '__main__':
    unittest.main()