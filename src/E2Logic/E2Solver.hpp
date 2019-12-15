//
//  Eternity II Solver Core Logic 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifndef E2Solver_hpp
#define E2Solver_hpp

#include <iostream>
#include "E2Init.hpp"
#include "E2Job.hpp"
#include "E2Trace.hpp"

class E2Solver {

private:
    Position** lastPosition;

    // solutions count (for Depth First Search)
    // children count (for Breadth First Search) 
    int hitCount;

public:
    E2Solver();
    int solve(std::string job);
    int getSolutionCount();
    
private:
    bool Explore(Position** pposition);
    void claimNewScore(int* lvl, int* highlvl);
    void printCurrentState();
    void cleanUp();
};

#endif // E2Solver_hpp
