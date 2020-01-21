//
//  Eternity II Solver Job description loader/writer 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#include <string>
#include <iostream>
#include <sstream>
#include <vector>
#include <utility>

#include "E2Job.hpp"
#include "E2Model/E2Types.h"
#include "E2Model/E2Model.h"
#include "E2Logic/E2Logger.hpp"
#include "E2Trace.hpp"
#include "E2Init.hpp"
#include "E2Size.h"

extern Piece Bag[BORDER_SIZE*BORDER_SIZE];

E2Job::E2Job()
{
	this->mJob = new std::string();
	this->ToString();
}

E2Job::E2Job(std::string& job)
{
	this->mJob = new std::string( job );
	this->LoadToBoard();
}

E2Job::~E2Job()
{
	if( this->mJob ) delete this->mJob;
}

std::string&  E2Job::ToString()
{
    std::string* s = this->boardToString();
    this->mJob = s;
	return *(this->mJob);
}

std::string* E2Job::boardToString()
{
    std::string* jobString = new std::string();
    std::stringstream ss;
    ss << "$";
    
    for( int i=1; i<=BORDER_SIZE; i++ )
    {
        for( int j=1; j<=BORDER_SIZE; j++ )
        {
            OrientedPiece* pp = Board[i][j].Here;
            
            if(pp && (pp != Empty) && pp->Origin) { ss << pp->Origin->id << traceDirection(pp->Orientation) << ":"; }
            else { ss << ".:"; }
        }
    }
    ss << ";";
    ss >> *jobString;
    return jobString;
}

std::pair<Position**, int> E2Job::findStartingPositionFromPath()
{
    bool found=false;
    int i=0;
    Position** result = NULL;

    while(!found && i<BORDER_SIZE*BORDER_SIZE)
    {
        if( Path[i]->Here == Empty ) {
            if( i==0 || Path[i-1]->Here != Empty ) {
                result= (Path+i); found=true;
            }
        }
        i++;
    }
    //debug("Starting position is : (" + std::to_string((*result)->x) + ", " + std::to_string((*result)->y)+ ")"); 
    //debug("Starting level is : " + std::to_string( i-1 ) );
    return std::make_pair(result, i-1);
}

Position** E2Job::findLastPositionFromPath()
{
    bool found=false;
    int i=BORDER_SIZE*BORDER_SIZE-1;
    //Position** result = NULL;
	
    while(!found && i>=0)
    {
        if( Path[i]->Here == Empty ) {
            if( i==BORDER_SIZE*BORDER_SIZE-1 || Path[i+1]->Here != Empty ) {
                //result= (Path+i); 
                found=true;
            }
        }
        i--;
    }

    //debug("Last position is : (" + std::to_string((*result)->x) + ", " + std::to_string((*result)->y)+ ")"); 
    //debug("Last level is : " + std::to_string( i+1 ) );

    return Path+(i+1);
}

void E2Job::LoadToBoard()
{
	debug("Loading");

	OrientedPiece** orientedPiece = (OrientedPiece**)malloc( sizeof( OrientedPiece* ) );
	OrientedPiece* constraint = (OrientedPiece*)malloc( sizeof( OrientedPiece ) );
	int noPiece = 0;
	Direction orientation = NORTH;
	E2JobIterator* it = new E2JobIterator( *this );

	for( int i=1; i<=BORDER_SIZE; i++ )
	{
		for( int j=1; j<=BORDER_SIZE; j++ )
		{
			if( it->nextPiece( &noPiece, &orientation ) )
			{
				Piece* p = &(Bag[noPiece]);
				Position* pos = &(Board[i][j]);
				
				if( p!= NULL )
				{
					switch(orientation)
					{
					case WEST:		{ constraint->West = p->C1; constraint->North = p->C2; constraint->East = p->C3; constraint->South = p->C4; } break;
					case NORTH:		{ constraint->North = p->C1; constraint->East = p->C2; constraint->South = p->C3; constraint->West = p->C4;  } break;
					case EAST:		{ constraint->East = p->C1; constraint->South = p->C2; constraint->West = p->C3; constraint->North = p->C4; } break;
					case SOUTH:		{ constraint->South = p->C1; constraint->West = p->C2; constraint->North = p->C3; constraint->East = p->C4; } break;
					default: break;
					}

					findPiecesByConstraintsAndId( constraint->West, constraint->North, constraint->East, constraint->South, p->id, orientedPiece );
					if( orientedPiece != NULL ) 
					{
						pos->Here = *orientedPiece;
						pos->Here->Origin->available = false;
					}
				}
				else
				{
					error("The requested piece does not exist in the bag");
				}
			}
		}
	}

    std::pair<Position**, int> pathInfo = findStartingPositionFromPath();
    this->startingPosition = pathInfo.first ;
    this->startingLevel = pathInfo.second;
	this->lastPosition = findLastPositionFromPath();
    //debug( "Starting at tree-level " + std::to_string( this->startingLevel ) );
	free(constraint);
	free(orientedPiece);
	delete(it);
}
