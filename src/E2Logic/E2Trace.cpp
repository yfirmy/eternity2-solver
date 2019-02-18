//
//  Eternity II Solver Debugging/Tracing tools 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#include "E2Size.h"
#include "E2Model/E2Types.h"
#include "E2Model/E2Model.h"
#include "E2Job.h"

#include <iostream>
#include <time.h>
#include <vector>

char traceConstraint( short c )
{
	if( c == NB_COLORS ) return '?';
	else return ( c==WALL ? '#' : 'A'+ (c-1));
}

void traceColor( Color* c )
{
	char ch = ( *c==WALL ? '#' : 'A'+ (((int)*c)-1));
	std::cout << ch;
}

char colorToChar( int c )
{
	return ( c == NB_COLORS ? '?' : (c==WALL ? '#' : 'A'+ (c-1)));
}

char traceDirection( Direction dir )
{
	switch ( dir )
	{
		case NORTH :	return 'N';
		case WEST :		return 'W';
		case EAST :		return 'E';
		case SOUTH :	return 'S';
		default:		return ' ';
	}
}

void tracePiece( OrientedPiece* pp, int line )
{
	if( pp == NULL )
	{
		std::cout << "   " ;
	}
	else
	{
		switch(line)
		{
			case 0: { std::cout << " " ;  traceColor( & (pp->North) ); std::cout << " " ; } break;
			case 1: { traceColor( & (pp->West) ); std::cout << " " ; traceColor( & (pp->East) ); } break;
			case 2: { std::cout << " " ; traceColor( & (pp->South) );  std::cout << " " ; } break;
			default: std::cout << std::endl;
		}
	}
}

void tracePiece( OrientedPiece* pp )
{
	tracePiece( pp, 0 ); std::cout << std::endl;
	tracePiece( pp, 1 ); std::cout << std::endl;
	tracePiece( pp, 2 ); std::cout << std::endl;
}

void traceBoard()
{
	std::cout << "traceBoard" << std::endl;

	for(int i=0; i<=BORDER_SIZE+1; i++)
	{
		for(int j=0;j<=BORDER_SIZE+1; j++)
		{
			tracePiece( Board[i][j].Here, 0 );
		}
		std::cout << std::endl;
		for(int j=0;j<=BORDER_SIZE+1; j++)
		{
			tracePiece( Board[i][j].Here, 1 );
		}
		std::cout << std::endl;
		for(int j=0;j<=BORDER_SIZE+1; j++)
		{
			tracePiece( Board[i][j].Here, 2 );
		}
		std::cout << std::endl;
	}
}

void traceCurrentDate()
{
	time_t rawtime;
	time ( &rawtime );
	char st[40];
	sprintf ( st, "%s", ctime (&rawtime) );
	char st2[40];
	int len = strlen(st);
	memcpy( st2, st, len-1 );
	st2[len-1]='\0';
	std::cout << st2 << " : ";
}

void traceJob() {
    std::cout << *(E2Job::boardToString()) << std::endl;
}

void debugIndex()
{
	std::cout << "== Debugging Index ==" << std::endl;
	for( int west=0; west< NB_COLORS+1; west++ )
	{
		for( int north=0; north< NB_COLORS+1; north++ )
		{
			for( int east=0; east< NB_COLORS+1; east++ )
			{
				for( int south=0; south< NB_COLORS+1; south++ )
				{	
					std::vector<OrientedPiece*>* v = Index[west][north][east][south];
					
					if ( v->size()>0 ) {

						std::cerr << "----------- (" << colorToChar(west) << ", " << colorToChar(north) << ", " << colorToChar(east) << ", " << colorToChar(south) << ") ------------" << std::endl;

						for( OrientedPiece* pp : *v ) {
							tracePiece(pp);
						}
					}
				}		
			}		
		}
	}
}