#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Eternity II Solver Non-Regression Testing - Depth-First Search version
#
#  Copyright © 2009-2019 Yohan Firmy
#

import sys
import re
import unittest
import subprocess

class E2NonRegTest(unittest.TestCase):

    def execute_commands(self, executable, commands):
      p = subprocess.Popen([executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      commandline = '\n'.join(commands)+'\nexit\n'
      (stdoutData, stderrData) = p.communicate(commandline.encode('utf-8'))
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
      self.assertEqual(expectedSolutionCount, len(foundResultsList), errorMsg)

    def test_from_empty_board(self):
      job1 = "$.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$24E:23E:22E:21E:20E:19E:18E:17E:16E:15E:14E:13E:12E:11E:10E:9E:8E:7E:6E:5E:4E:3E:2E:1E:0E:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$20N:15N:10N:5N:0N:21N:16N:11N:6N:1N:22N:17N:12N:7N:2N:23N:18N:13N:8N:3N:24N:19N:14N:9N:4N:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$4S:9S:14S:19S:24S:3S:8S:13S:18S:23S:2S:7S:12S:17S:22S:1S:6S:11S:16S:21S:0S:5S:10S:15S:20S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(4, foundSolutionsList, job1)

    def test_with_1piece_1(self):
      job1 = "$0W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

    def test_with_1piece_2(self):
      job1 = "$4S:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$4S:9S:14S:19S:24S:3S:8S:13S:18S:23S:2S:7S:12S:17S:22S:1S:6S:11S:16S:21S:0S:5S:10S:15S:20S:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

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
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

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
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

    def test_with_3pieces(self):
      job1 = "$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

    def test_with_4pieces(self):
      job1 = "$0W:.:.:.:4W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:20W:.:.:.:24W:;"
      foundSolutions = self.execute_ctrlsample_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList, job1)
      self.assert_solutions_count(1, foundSolutionsList, job1)

    def test_chain_empty_1piece(self):
      job1 = "$.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      job2 = "$0W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1, job2])
      foundSolutionsList1 = foundSolutions[job1]
      foundSolutionsList2 = foundSolutions[job2]
      self.assert_solution_in_results(u"$24E:23E:22E:21E:20E:19E:18E:17E:16E:15E:14E:13E:12E:11E:10E:9E:8E:7E:6E:5E:4E:3E:2E:1E:0E:;", foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$20N:15N:10N:5N:0N:21N:16N:11N:6N:1N:22N:17N:12N:7N:2N:23N:18N:13N:8N:3N:24N:19N:14N:9N:4N:;", foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$4S:9S:14S:19S:24S:3S:8S:13S:18S:23S:2S:7S:12S:17S:22S:1S:6S:11S:16S:21S:0S:5S:10S:15S:20S:;", foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList1, job1)
      self.assert_solutions_count(4, foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList2, job2)
      self.assert_solutions_count(1, foundSolutionsList2, job2)

    def test_chain_1piece_empty(self):
      job1 = "$0W:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      job2 = "$.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:;"
      foundSolutions = self.execute_ctrlsample_test([job1, job2])
      foundSolutionsList1 = foundSolutions[job1]
      foundSolutionsList2 = foundSolutions[job2]
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList1, job1)
      self.assert_solutions_count(1, foundSolutionsList1, job1)
      self.assert_solution_in_results(u"$24E:23E:22E:21E:20E:19E:18E:17E:16E:15E:14E:13E:12E:11E:10E:9E:8E:7E:6E:5E:4E:3E:2E:1E:0E:;", foundSolutionsList2, job2)
      self.assert_solution_in_results(u"$20N:15N:10N:5N:0N:21N:16N:11N:6N:1N:22N:17N:12N:7N:2N:23N:18N:13N:8N:3N:24N:19N:14N:9N:4N:;", foundSolutionsList2, job2)
      self.assert_solution_in_results(u"$4S:9S:14S:19S:24S:3S:8S:13S:18S:23S:2S:7S:12S:17S:22S:1S:6S:11S:16S:21S:0S:5S:10S:15S:20S:;", foundSolutionsList2, job2)
      self.assert_solution_in_results(u"$0W:1W:2W:3W:4W:5W:6W:7W:8W:9W:10W:11W:12W:13W:14W:15W:16W:17W:18W:19W:20W:21W:22W:23W:24W:;", foundSolutionsList2, job2)
      self.assert_solutions_count(4, foundSolutionsList2, job2)

    def test_clue1_1(self):
      job1 = "$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:.:.:.:1E:20S:10W:.:.:.:23N:22S:6N:.:.:.:8W:16W:25S:24S:15W:17S:21S:13S:;"
      foundSolutions = self.execute_clue1_test([job1])
      foundSolutionsList = foundSolutions[job1]
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:0N:5E:4W:1E:20S:10W:3S:2E:28E:23N:22S:6N:29E:18S:32E:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:0N:5E:2W:1E:20S:10W:3S:4E:28E:23N:22S:6N:29E:18S:32E:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:0N:5E:4W:1E:20S:10W:3S:2E:28E:23N:22S:6N:29E:18N:32E:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:0N:5E:2W:1E:20S:10W:3S:4E:28E:23N:22S:6N:29E:18N:32E:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18S:32S:3W:1E:20S:10W:28N:2W:0E:23N:22S:6N:29E:4E:5W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18S:3E:32N:1E:20S:10W:28N:2W:0E:23N:22S:6N:29E:4E:5W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18N:32S:3W:1E:20S:10W:28N:2W:0E:23N:22S:6N:29E:4E:5W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18N:3E:32N:1E:20S:10W:28N:2W:0E:23N:22S:6N:29E:4E:5W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18S:32S:3W:1E:20S:10W:28N:4W:0E:23N:22S:6N:29E:2E:5W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18S:3E:32N:1E:20S:10W:28N:4W:0E:23N:22S:6N:29E:2E:5W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18N:32S:3W:1E:20S:10W:28N:4W:0E:23N:22S:6N:29E:2E:5W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18N:3E:32N:1E:20S:10W:28N:4W:0E:23N:22S:6N:29E:2E:5W:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18S:32S:3W:1E:20S:10W:28N:5W:2S:23N:22S:6N:29E:0E:4N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18S:3E:32N:1E:20S:10W:28N:5W:2S:23N:22S:6N:29E:0E:4N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18N:32S:3W:1E:20S:10W:28N:5W:2S:23N:22S:6N:29E:0E:4N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18N:3E:32N:1E:20S:10W:28N:5W:2S:23N:22S:6N:29E:0E:4N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:0N:5E:4W:1E:20S:10W:32W:2E:28E:23N:22S:6N:29E:18S:3N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:0N:5E:2W:1E:20S:10W:32W:4E:28E:23N:22S:6N:29E:18S:3N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:0N:5E:4W:1E:20S:10W:32W:2E:28E:23N:22S:6N:29E:18N:3N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:0N:5E:2W:1E:20S:10W:32W:4E:28E:23N:22S:6N:29E:18N:3N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18S:32S:3W:1E:20S:10W:28N:5W:4S:23N:22S:6N:29E:0E:2N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18S:3E:32N:1E:20S:10W:28N:5W:4S:23N:22S:6N:29E:0E:2N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18N:32S:3W:1E:20S:10W:28N:5W:4S:23N:22S:6N:29E:0E:2N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solution_in_results(u"$35S:27W:30S:12S:14W:33N:11S:34N:31N:26S:7S:19N:9W:18N:3E:32N:1E:20S:10W:28N:5W:4S:23N:22S:6N:29E:0E:2N:8W:16W:25S:24S:15W:17S:21S:13S:;", foundSolutionsList, job1)
      self.assert_solutions_count(24, foundSolutionsList, job1)
      
if __name__ == '__main__':
    unittest.main()