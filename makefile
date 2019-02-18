
CFLAGS=-W -Wall -std=c++11 -I./src

CLUE1_OBJ_FILES = obj/E2Clue1.o obj/E2Init_Clue1.o obj/E2Job_Clue1.o obj/E2Solver_Clue1.o obj/E2Trace_Clue1.o 
PUZZLE_OBJ_FILES = obj/E2Puzzle.o obj/E2Init_Puzzle.o obj/E2Job_Puzzle.o obj/E2Solver_Puzzle.o obj/E2Trace_Puzzle.o
CONTROLSAMPLE_OBJ_FILES = obj/E2ControlSample.o obj/E2Init_Sample.o obj/E2Job_Sample.o obj/E2Solver_Sample.o obj/E2Trace_Sample.o
COMMON_OBJ_FILES = obj/E2Application.o obj/E2Logger.o 

all: E2Clue1 E2Puzzle E2ControlSample

E2Clue1: $(CLUE1_OBJ_FILES) $(COMMON_OBJ_FILES)
	g++ -v -o bin/E2Clue1 $(CLUE1_OBJ_FILES) $(COMMON_OBJ_FILES)

E2Puzzle: $(PUZZLE_OBJ_FILES) $(COMMON_OBJ_FILES)
	g++ -v -o bin/E2Puzzle $(PUZZLE_OBJ_FILES) $(COMMON_OBJ_FILES)

E2ControlSample: $(CONTROLSAMPLE_OBJ_FILES) $(COMMON_OBJ_FILES)
	g++ -v -o bin/E2ControlSample $(CONTROLSAMPLE_OBJ_FILES) $(COMMON_OBJ_FILES)

obj/E2Clue1.o: src/E2Applications/E2Clue1Solver/E2Clue1.cpp
	g++ -DCLUE1 $(CFLAGS) -o obj/E2Clue1.o -c src/E2Applications/E2Clue1Solver/E2Clue1.cpp

obj/E2Puzzle.o: src/E2Applications/E2PuzzleSolver/E2Puzzle.cpp
	g++ -DPUZZLE $(CFLAGS) -o obj/E2Puzzle.o -c src/E2Applications/E2PuzzleSolver/E2Puzzle.cpp

obj/E2ControlSample.o: src/E2Applications/E2ControlSampleSolver/E2ControlSample.cpp
	g++ -DSAMPLE $(CFLAGS) -o obj/E2ControlSample.o -c src/E2Applications/E2ControlSampleSolver/E2ControlSample.cpp

obj/E2Init_Clue1.o: src/E2Logic/E2Init.cpp
	g++ -DCLUE1 $(CFLAGS) -o obj/E2Init_Clue1.o -c src/E2Logic/E2Init.cpp

obj/E2Init_Puzzle.o: src/E2Logic/E2Init.cpp
	g++ -DPUZZLE $(CFLAGS) -o obj/E2Init_Puzzle.o -c src/E2Logic/E2Init.cpp

obj/E2Init_Sample.o: src/E2Logic/E2Init.cpp
	g++ -DSAMPLE  $(CFLAGS) -o obj/E2Init_Sample.o -c src/E2Logic/E2Init.cpp

obj/E2Job_Clue1.o: src/E2Logic/E2Job.cpp
	g++ -DCLUE1 $(CFLAGS) -o obj/E2Job_Clue1.o -c src/E2Logic/E2Job.cpp

obj/E2Job_Puzzle.o: src/E2Logic/E2Job.cpp
	g++ -DPUZZLE $(CFLAGS) -o obj/E2Job_Puzzle.o -c src/E2Logic/E2Job.cpp

obj/E2Job_Sample.o: src/E2Logic/E2Job.cpp
	g++ -DSAMPLE $(CFLAGS) -o obj/E2Job_Sample.o -c src/E2Logic/E2Job.cpp

obj/E2Solver_Clue1.o: src/E2Logic/E2Solver.cpp
	g++ -DCLUE1 $(CFLAGS) -o obj/E2Solver_Clue1.o -c src/E2Logic/E2Solver.cpp

obj/E2Solver_Puzzle.o: src/E2Logic/E2Solver.cpp
	g++ -DPUZZLE $(CFLAGS) -o obj/E2Solver_Puzzle.o -c src/E2Logic/E2Solver.cpp

obj/E2Solver_Sample.o: src/E2Logic/E2Solver.cpp
	g++ -DSAMPLE $(CFLAGS) -o obj/E2Solver_Sample.o -c src/E2Logic/E2Solver.cpp

obj/E2Trace_Clue1.o: src/E2Logic/E2Trace.cpp
	g++ -DCLUE1 $(CFLAGS) -o obj/E2Trace_Clue1.o -c src/E2Logic/E2Trace.cpp

obj/E2Trace_Puzzle.o: src/E2Logic/E2Trace.cpp
	g++ -DPUZZLE $(CFLAGS) -o obj/E2Trace_Puzzle.o -c src/E2Logic/E2Trace.cpp

obj/E2Trace_Sample.o: src/E2Logic/E2Trace.cpp
	g++ -DSAMPLE $(CFLAGS) -o obj/E2Trace_Sample.o -c src/E2Logic/E2Trace.cpp

obj/E2Logger.o: src/E2Logic/E2Logger.cpp
	g++ $(CFLAGS) -o obj/E2Logger.o -c src/E2Logic/E2Logger.cpp

obj/E2Application.o: src/E2Logic/E2Application.cpp
	g++ $(CFLAGS) -o obj/E2Application.o -c src/E2Logic/E2Application.cpp

clean:
	rm obj/*.o
	rm bin/*
	
