//
//  Eternity II Solver Core Logic 
//
//  Copyright © 2009-2020 Yohan Firmy
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
    this->firstStep = myJob->GetFirstStep();

#ifdef DEPTH_FIRST_SEARCH
    this->lastStep = myJob->GetLastStep();
#endif

#ifdef BREADTH_FIRST_SEARCH
    this->lastStep = this->firstStep;
#endif

    Explore_iterative(this->firstStep);

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

void E2Solver::Explore_iterative(Step* start) {

    Step* step = start;
    
    while( step >= this->firstStep && step <= this->lastStep )
    {
        if( step->firstCandidate == &Empty )
        {
            short constraintWest = step->position->West->Here->East;
            short constraintNorth = step->position->North->Here->South;
            short constraintEast = step->position->East->Here->West;
            short constraintSouth = step->position->South->Here->North;

            std::vector<OrientedPiece*>* possiblePieces = Index[constraintWest][constraintNorth][constraintEast][constraintSouth];

            if( possiblePieces->size() > 0 )
            {
                step->firstCandidate = possiblePieces->data();
                step->lastCandidate = step->firstCandidate + possiblePieces->size() - 1;
            }
        }

        if( step->firstCandidate != &Empty && step->firstCandidate <= step->lastCandidate )
        {
            // for each candidate Piece
            while( step->firstCandidate <= step->lastCandidate ) {
                if( (*(step->firstCandidate))->Origin->available ) 
                {
                    // choose the first available candidate
                    (*(step->firstCandidate))->Origin->available = false;
                    step->position->Here = *(step->firstCandidate);
                    break;
                }
                step->firstCandidate++;
            }
            if( step->position->Here == *(step->firstCandidate) ) {
                // move forward
                step->firstCandidate++;
                step++;
            } else {
                // no candidate was available
                step->firstCandidate = &Empty;
                step->lastCandidate = &Empty;

                if( step > this->firstStep ) {
                    Step* previousStep = step - 1;
                    previousStep->position->Here->Origin->available = true;
                    previousStep->position->Here = Empty;
                }
                // move backward
                step--;
            }
        }
        else
        {
            // no candidate was found
            step->firstCandidate = &Empty;
            step->lastCandidate = &Empty;

            Step* previousStep = step - 1;
            if( step > this->firstStep ) {
                previousStep->position->Here->Origin->available = true;
                previousStep->position->Here = Empty;
            }
            // move backward
            step--;
        }

        if( step == this->lastStep + 1 ) {
            
            // got ya
            this->hitCount++;
            this->printCurrentState();

            // then move backward
            Step* previousStep = step - 1;
            previousStep->position->Here->Origin->available = true;
            previousStep->position->Here = Empty;
            step--;
        }
    }
}
