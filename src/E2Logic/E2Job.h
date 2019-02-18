//
//  Eternity II Solver Job description loader/writer 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifndef E2JOB
#define E2JOB

#include <iostream>
#include <string>
#include <utility>
#include "E2Model/E2Types.h"

class E2Job
{

private:
	std::string* mJob;
	std::string& ToString();
	void LoadToBoard();
    std::pair<Position**, int> findStartingPositionFromPath();
	Position** findLastPositionFromPath();
	Position** startingPosition;
	Position** lastPosition;
    int startingLevel;

public:
	E2Job();
	E2Job(std::string& job);
	~E2Job();
	std::string& GetString() { return *(this->mJob); }
	Position** GetStartingPosition() { return this->startingPosition; };
	Position** GetLastPosition(){ return this->lastPosition; }
    int GetStartingLevel() { return this->startingLevel; };
    static std::string* boardToString();
};

class E2JobIterator
{
	E2Job& job;
	int next;

public:
	E2JobIterator(E2Job& pjob) : job( pjob )
	{
		next=1;
	};

	/*
	 * noPiece: (output parameter) found Piece number
	 * orientation: (output parameter) found Orientation
	 */
	bool nextPiece(int *noPiece, Direction* orientation)
	{
		bool exist = false;
		int separator = this->job.GetString().find(':', next);
		char direction = this->job.GetString()[separator-1];

		if( separator-next > 1 )
		{
			char* buffer = (char*) malloc( (separator-next)*sizeof(char) );
			strcpy( buffer,  this->job.GetString().substr( next, separator-next-1 ).c_str() );
			buffer[separator-next-1] = '\0';
			*noPiece = atoi( buffer );
			switch( direction )
			{
			case 'N' : *orientation = NORTH; break;
			case 'W' : *orientation = WEST; break;
			case 'E' : *orientation = EAST; break;
			case 'S' : *orientation = SOUTH; break;
			}
			exist = true;
		}

		next=separator+1;
		return exist;
	};

};

#endif // E2JOB
