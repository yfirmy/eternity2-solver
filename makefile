
CFLAGS=-W -Wall -std=c++11 -I./src
LDFLAGS=-static

OBJDIR := obj
BINDIR := bin

EXEC = E2Clue1 E2Puzzle E2ControlSample
CLUE1_FILES = obj/E2Clue1 obj/E2Init_Clue1 obj/E2Job_Clue1 obj/E2Solver_Clue1 obj/E2Trace_Clue1
PUZZLE_FILES = obj/E2Puzzle obj/E2Init_Puzzle obj/E2Job_Puzzle obj/E2Solver_Puzzle obj/E2Trace_Puzzle
CONTROLSAMPLE_FILES = obj/E2ControlSample obj/E2Init_Sample obj/E2Job_Sample obj/E2Solver_Sample obj/E2Trace_Sample
COMMON_FILES = obj/E2Application obj/E2Logger

# Depth First Search object files

CLUE1_DFS_OBJ = $(CLUE1_FILES:=_dfs.o)
PUZZLE_DFS_OBJ = $(PUZZLE_FILES:=_dfs.o)
CONTROLSAMPLE_DFS_OBJ = $(CONTROLSAMPLE_FILES:=_dfs.o)
COMMON_DFS_OBJ = $(COMMON_FILES:=_dfs.o)

# Breadth First Search object files

CLUE1_BFS_OBJ = $(CLUE1_FILES:=_bfs.o)
PUZZLE_BFS_OBJ = $(PUZZLE_FILES:=_bfs.o)
CONTROLSAMPLE_BFS_OBJ = $(CONTROLSAMPLE_FILES:=_bfs.o)
COMMON_BFS_OBJ = $(COMMON_FILES:=_bfs.o)

all: $(EXEC:=-dfs) $(EXEC:=-bfs)

# creating directories if necessary

$(BINDIR)/:
	mkdir -p $(BINDIR)

$(OBJDIR)/:
	mkdir -p $(OBJDIR)

# Depth First Search applications

E2Clue1-dfs: $(CLUE1_DFS_OBJ) $(COMMON_DFS_OBJ) | $(BINDIR)/
	g++ $(LDFLAGS) -v -o bin/$@ $^

E2Puzzle-dfs: $(PUZZLE_DFS_OBJ) $(COMMON_DFS_OBJ) | $(BINDIR)/
	g++ $(LDFLAGS) -v -o bin/$@ $^

E2ControlSample-dfs: $(CONTROLSAMPLE_DFS_OBJ) $(COMMON_DFS_OBJ) | $(BINDIR)/
	g++ $(LDFLAGS) -v -o bin/$@ $^

# Breadth First Search applications

E2Clue1-bfs: $(CLUE1_BFS_OBJ) $(COMMON_BFS_OBJ) | $(BINDIR)/
	g++ $(LDFLAGS) -v -o bin/$@ $^

E2Puzzle-bfs: $(PUZZLE_BFS_OBJ) $(COMMON_BFS_OBJ) | $(BINDIR)/
	g++ $(LDFLAGS) -v -o bin/$@ $^

E2ControlSample-bfs: $(CONTROLSAMPLE_BFS_OBJ) $(COMMON_BFS_OBJ) | $(BINDIR)/
	g++ $(LDFLAGS) -v -o bin/$@ $^

# Main (DFS)

obj/E2Clue1_dfs.o: src/E2Applications/E2Clue1Solver/E2Clue1.cpp | $(OBJDIR)/
	g++ -DDEPTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Puzzle_dfs.o: src/E2Applications/E2PuzzleSolver/E2Puzzle.cpp | $(OBJDIR)/
	g++ -DDEPTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2ControlSample_dfs.o: src/E2Applications/E2ControlSampleSolver/E2ControlSample.cpp | $(OBJDIR)/
	g++ -DDEPTH_FIRST_SEARCH -DSAMPLE $(CFLAGS) -o $@ -c $^
	
# Main (BFS)

obj/E2Clue1_bfs.o: src/E2Applications/E2Clue1Solver/E2Clue1.cpp | $(OBJDIR)/
	g++ -DBREADTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Puzzle_bfs.o: src/E2Applications/E2PuzzleSolver/E2Puzzle.cpp | $(OBJDIR)/
	g++ -DBREADTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2ControlSample_bfs.o: src/E2Applications/E2ControlSampleSolver/E2ControlSample.cpp | $(OBJDIR)/
	g++ -DBREADTH_FIRST_SEARCH -DSAMPLE $(CFLAGS) -o $@ -c $^

# Init (DFS)

obj/E2Init_Clue1_dfs.o: src/E2Logic/E2Init.cpp
	g++  -DDEPTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Init_Puzzle_dfs.o: src/E2Logic/E2Init.cpp
	g++  -DDEPTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2Init_Sample_dfs.o: src/E2Logic/E2Init.cpp
	g++  -DDEPTH_FIRST_SEARCH -DSAMPLE  $(CFLAGS) -o $@ -c $^

# Init (BFS)

obj/E2Init_Clue1_bfs.o: src/E2Logic/E2Init.cpp
	g++  -DBREADTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Init_Puzzle_bfs.o: src/E2Logic/E2Init.cpp
	g++  -DBREADTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2Init_Sample_bfs.o: src/E2Logic/E2Init.cpp
	g++  -DBREADTH_FIRST_SEARCH -DSAMPLE  $(CFLAGS) -o $@ -c $^


# Job (DFS)

obj/E2Job_Clue1_dfs.o: src/E2Logic/E2Job.cpp
	g++ -DDEPTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Job_Puzzle_dfs.o: src/E2Logic/E2Job.cpp
	g++ -DDEPTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2Job_Sample_dfs.o: src/E2Logic/E2Job.cpp
	g++ -DDEPTH_FIRST_SEARCH -DSAMPLE $(CFLAGS) -o $@ -c $^

# Job (BFS)

obj/E2Job_Clue1_bfs.o: src/E2Logic/E2Job.cpp
	g++ -DBREADTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Job_Puzzle_bfs.o: src/E2Logic/E2Job.cpp
	g++ -DBREADTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2Job_Sample_bfs.o: src/E2Logic/E2Job.cpp
	g++ -DBREADTH_FIRST_SEARCH -DSAMPLE $(CFLAGS) -o $@ -c $^

# Solver (DFS)

obj/E2Solver_Clue1_dfs.o: src/E2Logic/E2Solver.cpp
	g++ -DDEPTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Solver_Puzzle_dfs.o: src/E2Logic/E2Solver.cpp
	g++ -DDEPTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2Solver_Sample_dfs.o: src/E2Logic/E2Solver.cpp
	g++ -DDEPTH_FIRST_SEARCH -DSAMPLE $(CFLAGS) -o $@ -c $^

# Solver (BFS)

obj/E2Solver_Clue1_bfs.o: src/E2Logic/E2Solver.cpp
	g++ -DBREADTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Solver_Puzzle_bfs.o: src/E2Logic/E2Solver.cpp
	g++ -DBREADTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2Solver_Sample_bfs.o: src/E2Logic/E2Solver.cpp
	g++ -DBREADTH_FIRST_SEARCH -DSAMPLE $(CFLAGS) -o $@ -c $^

# Trace (DFS)

obj/E2Trace_Clue1_dfs.o: src/E2Logic/E2Trace.cpp
	g++ -DDEPTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Trace_Puzzle_dfs.o: src/E2Logic/E2Trace.cpp
	g++ -DDEPTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2Trace_Sample_dfs.o: src/E2Logic/E2Trace.cpp
	g++ -DDEPTH_FIRST_SEARCH -DSAMPLE $(CFLAGS) -o $@ -c $^

# Trace (BFS)

obj/E2Trace_Clue1_bfs.o: src/E2Logic/E2Trace.cpp
	g++ -DBREADTH_FIRST_SEARCH -DCLUE1 $(CFLAGS) -o $@ -c $^

obj/E2Trace_Puzzle_bfs.o: src/E2Logic/E2Trace.cpp
	g++ -DBREADTH_FIRST_SEARCH -DPUZZLE $(CFLAGS) -o $@ -c $^

obj/E2Trace_Sample_bfs.o: src/E2Logic/E2Trace.cpp
	g++ -DBREADTH_FIRST_SEARCH -DSAMPLE $(CFLAGS) -o $@ -c $^

# Common (DFS)

obj/E2Logger_dfs.o: src/E2Logic/E2Logger.cpp
	g++ -DDEPTH_FIRST_SEARCH $(CFLAGS) -o $@ -c $^

obj/E2Application_dfs.o: src/E2Logic/E2Application.cpp
	g++ -DDEPTH_FIRST_SEARCH $(CFLAGS) -o $@ -c $^

# Common (BFS)

obj/E2Logger_bfs.o: src/E2Logic/E2Logger.cpp
	g++ -DBREADTH_FIRST_SEARCH $(CFLAGS) -o $@ -c $^

obj/E2Application_bfs.o: src/E2Logic/E2Application.cpp
	g++ -DBREADTH_FIRST_SEARCH $(CFLAGS) -o $@ -c $^

clean:
	rm obj/*.o
	rm bin/*
	
