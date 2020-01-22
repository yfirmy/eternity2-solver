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
    Step* firstStep; 
    Step* lastStep;

    // solutions count (for Depth First Search)
    // children count (for Breadth First Search) 
    int hitCount;

public:
    E2Solver();
    int solve(std::string job);
    int getSolutionCount();
    
private:
    void Explore_iterative(Step* start);

    void printCurrentState();
    void cleanUp();
};

#endif // E2Solver_hpp
