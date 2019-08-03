#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Solver Non-Regression Testing - Breadth-First Search version
#
#  Copyright © 2009-2019 Yohan Firmy
#

import sys
import re
import unittest
import subprocess

class E2NonRegTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
      #pClean = subprocess.Popen(["make", "clean"])
      #(stdoutData, stderrData) = pClean.communicate()
      pMake = subprocess.Popen(["make"])
      (stdoutData, stderrData) = pMake.communicate()

    def execute_commands(self, executable, commands):
      p = subprocess.Popen([executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      (stdoutData, stderrData) = p.communicate('\n'.join(commands)+'\nexit\n')
      return stdoutData.decode("utf-8")

    def execute_controlsample(self, commands):
      return self.execute_commands("bin/E2ControlSample-bfs", commands)

    def execute_worker(self, commands):
      return self.execute_commands("bin/E2Puzzle-bfs", commands)

    def execute_clue1(self, commands):
      return self.execute_commands("bin/E2Clue1-bfs", commands)

    def parse_solution(self, line, foundSolutionsList):
      solution = re.sub("^INFO Result (?:\d)+ : (\$(?:(?:\.|(?:[0-9]{1,3}(?:N|W|E|S)))\:)+\;)", r"\1", line)
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
        if(line.startswith("INFO Result 1 : ")):
          idxInitialBoard = idxInitialBoard+1
          foundSolutionsList = foundSolutions[initialboards[idxInitialBoard]]
          self.parse_solution(line, foundSolutionsList)
        else:
          if(line.startswith("INFO Result")):
            foundSolutionsList = foundSolutions[initialboards[idxInitialBoard]]
            self.parse_solution(line, foundSolutionsList)
      return foundSolutions

    def assert_solution_in_results(self, expectedSolution, foundResultsList, initialJob):
      errorMsg = "missing result " + expectedSolution + " in the results for the job " + initialJob
      self.assertIn(expectedSolution, foundResultsList, errorMsg)

    def assert_solutions_count(self, expectedSolutionCount, foundResultsList, initialJob):
      errorMsg = str(len(foundResultsList)) + " results founds from job " + initialJob + "(expected "+ str(expectedSolutionCount)+" results)"
      self.assertEquals(expectedSolutionCount, len(foundResultsList), errorMsg)

    def test_from_empty_board(self):
      job1 = "$.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$24E:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$20N:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$4S:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$0W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solutions_count(4, foundSolutionsList, job1)

    def test_with_1piece_1(self):
      job1 = "$0W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:.:.:.:24S:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$0W:.:.:.:20E:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solutions_count(3, foundSolutionsList, job1)

    def test_with_1piece_2(self):
      job1 = "$4S:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$4S:.:.:.:24S:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$4S:.:.:.:20E:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$4S:.:.:.:0N:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solutions_count(3, foundSolutionsList, job1)

    @unittest.skip("not necessary")
    def test_with_1piece_3(self):
      job1 = "$.:1W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

    def test_with_1piece_4(self):
      job1 = "$.:.:.:.:.:.:.:.:.:.:.:.:12W:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$24E:.:.:.:.:.:.:.:.:.:.:.:12W:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$20N:.:.:.:.:.:.:.:.:.:.:.:12W:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$4S:.:.:.:.:.:.:.:.:.:.:.:12W:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$0W:.:.:.:.:.:.:.:.:.:.:.:12W:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solutions_count(4, foundSolutionsList, job1)

    @unittest.skip("not necessary")
    def test_with_2pieces_1(self):
      job1 = "$0W:1W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

    def test_with_2pieces_2(self):
      job1 = "$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:24N:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:.:;", foundSolutionsList, job1)
      self.assert_solutions_count(2, foundSolutionsList, job1)

    def test_with_3pieces_1(self):
      job1 = "$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

    def test_with_3pieces_2(self):
      job1 = "$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:24N:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:24N:.:.:.:20S:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

    def test_with_4pieces(self):
      job1 = "$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:24W:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:10N:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:24W:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$0W:1W:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(2, foundSolutionsList, job1)

    def test_with_5pieces(self):
      job1 = "$0W:1W:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:24W:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:1W:2W:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

    def test_chain_empty_1piece(self):
      job1 = "$.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      job2 = "$0W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1, job2])
      foundSolutionsList1 = foundSolutions[job1]
      foundSolutionsList2 = foundSolutions[job2]
      self.assert_solution_in_results(u"$24E:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$20N:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$4S:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$0W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList1, job1)
      self.assert_solutions_count(4, foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$0W:.:.:.:24S:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList2, job2)
      self.assert_solution_in_results(u"$0W:.:.:.:20E:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList2, job2)
      self.assert_solution_in_results(u"$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList2, job2)
      self.assert_solutions_count(3, foundSolutionsList2, job2)

    def test_chain_1piece_empty(self):
      job1 = "$0W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      job2 = "$.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1, job2])
      foundSolutionsList1 = foundSolutions[job1]
      foundSolutionsList2 = foundSolutions[job2]
      self.assert_solution_in_results(u"$0W:.:.:.:24S:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$0W:.:.:.:20E:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList1, job1)
      self.assert_solutions_count(3, foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$24E:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList2, job2)
      self.assert_solution_in_results(u"$20N:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList2, job2)
      self.assert_solution_in_results(u"$4S:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList2, job2)
      self.assert_solution_in_results(u"$0W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;", foundSolutionsList2, job2)
      self.assert_solutions_count(4, foundSolutionsList2, job2)

    def test_clue1_1(self):
      job1 = "$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1E:20S:10W:.:.:.:23N:22S:6N:.:.:.:8W:16W:25S:24S:15W:17S:21S:13S:;"
      foundSolutions = self.execute_clue1_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1W:20S:10W:.:.:.:23N:22S:6N:.:.:32E:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1W:20S:10W:.:.:.:23N:22S:6N:.:.:18E:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1W:20S:10W:.:.:.:23N:22S:6N:.:.:18W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1W:20S:10W:.:.:.:23N:22S:6N:.:.:5W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1W:20S:10W:.:.:.:23N:22S:6N:.:.:4N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1W:20S:10W:.:.:.:23N:22S:6N:.:.:3N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1W:20S:10W:.:.:.:23N:22S:6N:.:.:2N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1W:20S:10W:.:.:.:23N:22S:6N:.:.:0N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solutions_count(8, foundSolutionsList, job1)
      
if __name__ == '__main__':
    unittest.main()