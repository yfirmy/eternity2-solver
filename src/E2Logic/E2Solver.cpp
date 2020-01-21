//
//  Eternity II Solver Core Logic 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#include "E2Solver.hpp"
#include "E2Model/E2Model.h"
#include "E2Logger.hpp"
#include "E2Trace.hpp"

#include <vector>

E2Solver::E2Solver() {
    Initialisation();
    Indexation();
    this->hitCount = 0;
};

int E2Solver::solve(std::string job) {
    E2Job* myJob = new E2Job( job );
    Position** pos = myJob->GetStartingPosition();
    this->lastPosition = myJob->GetLastPosition();
    Explore(pos);
    int result = this->hitCount;
    this->cleanUp();
    return result;
};

int E2Solver::getSolutionCount() {
    return this->hitCount;
}

void E2Solver::cleanUp() {
    Reinitialisation();
    this->hitCount = 0;
}

void E2Solver::printCurrentState() {

#ifdef DEPTH_FIRST_SEARCH
    info("Solution " + std::to_string( this->hitCount ) + " : " + *(E2Job::boardToString()) );
#endif

#ifdef BREADTH_FIRST_SEARCH
    info("Result " + std::to_string( this->hitCount ) + " : " + *(E2Job::boardToString()) );
#endif

}

bool E2Solver::Explore(Position** pposition)
{
    bool result = false;
    
    Position* position = *(pposition);
    
    short constraintWest = position->West->Here->East;
    short constraintNorth = position->North->Here->South;
    short constraintEast = position->East->Here->West;
    short constraintSouth = position->South->Here->North;

    std::vector<OrientedPiece*>* PossiblePieces = Index[constraintWest][constraintNorth][constraintEast][constraintSouth];
    
    for( OrientedPiece** it = PossiblePieces->data(); it != PossiblePieces->data() + PossiblePieces->size(); it++ )
    {
        OrientedPiece* candidate = *it;
        
        if( candidate->Origin->available )
        {
            candidate->Origin->available = false;
            position->Here = candidate;
            
#ifdef DEPTH_FIRST_SEARCH
            if( pposition!=this->lastPosition ) {

                result = Explore( pposition+1 );
            } 
            else
            {
                this->hitCount++;
                this->printCurrentState();
            }
#endif

#ifdef BREADTH_FIRST_SEARCH
            this->hitCount++;
            this->printCurrentState();   
#endif

            // free the piece
            candidate->Origin->available = true;
            position->Here = Empty;
        }
    }
    
    return result;
}
