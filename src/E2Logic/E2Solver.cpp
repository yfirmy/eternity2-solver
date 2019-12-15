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

int Joker = NB_COLORS;
int level;
int highscore;

E2Solver::E2Solver() {
    Initialisation();
    Indexation();
    this->hitCount = 0;
    level=0;
    highscore=0;
};

int E2Solver::solve(std::string job) {
    E2Job* myJob = new E2Job( job );
    Position** pos = myJob->GetStartingPosition();
    this->lastPosition = myJob->GetLastPosition();
    level = myJob->GetStartingLevel();
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
    level=0;
    highscore=0;
}

void E2Solver::claimNewScore(int* lvl, int* highlvl)
{
    if( *lvl > *highlvl )
    {
        debug( "New score " + std::to_string( *lvl ) + " : " + *(E2Job::boardToString()) );
        *highlvl = *lvl;
    }
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
    level++;
    
    Position* position = *(pposition);
    
    OrientedPiece* west = position->West->Here;
    OrientedPiece* east = position->East->Here;
    OrientedPiece* north = position->North->Here;
    OrientedPiece* south = position->South->Here;
    
    short constraintWest = west ? west->East : Joker;
    short constraintNorth = north ? north->South : Joker;
    short constraintEast = east ? east->West : Joker;
    short constraintSouth = south ? south->North : Joker;
    
    std::vector<OrientedPiece*>* PossiblePieces = Index[constraintWest][constraintNorth][constraintEast][constraintSouth];
    //std::vector<OrientedPiece*>::iterator it;
    std::vector<OrientedPiece*>::reverse_iterator it;
    
    //for( it=PossiblePieces->begin(); it!=PossiblePieces->end(); it++)
    for( it=PossiblePieces->rbegin(); it!=PossiblePieces->rend(); it++)
    {
        OrientedPiece* candidate = *it;
        
        if( candidate->Origin->available )
        {
            candidate->Origin->available = false;
            position->Here = candidate;
            
            //this->claimNewScore(&level, &highscore);
            
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
            position->Here = NULL;
        }
    }
    
    level--;
    return result;
}
