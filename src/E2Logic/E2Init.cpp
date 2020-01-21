//
//  Eternity II Solver Initialization Utils 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#include <iostream>
#include <vector>

#include "E2Init.hpp"
#include "E2Model/E2Types.h"
#include "E2Model/E2Model.h"
#include "E2Logger.hpp"
#include "E2Size.h"

Position Board[BORDER_SIZE+2][BORDER_SIZE+2];
Position* Path[BORDER_SIZE*BORDER_SIZE];
OrientedPiece* PiecesOrientees[NB_ORIENTED_PIECES];
std::vector<OrientedPiece*>* Index[NB_COLORS+1][NB_COLORS+1][NB_COLORS+1][NB_COLORS+1];
extern Piece Bag[BORDER_SIZE*BORDER_SIZE];
extern PuzzlePiece BagInitializer[BORDER_SIZE*BORDER_SIZE];
OrientedPiece* Empty;

Position* goNorth( Position* start , int count, Position** outpath )
{
	Position* p = start;
	Position** out = outpath;
	for( int i=0; i<count; i++ )
	{
		*out = p;
		p = (Position*)(p->North);
		out++;
	}
	return p;
}

Position* goSouth( Position* start , int count, Position** outpath )
{
	Position* p = start;
	Position** out = outpath;
	for( int i=0; i<count; i++ )
	{
		*out = p;
		p = (Position*)(p->South);
		out++;
	}
	return p;
}

Position* goWest( Position* start , int count, Position** outpath )
{
	Position* p = start;
	Position** out = outpath;
	for( int i=0; i<count; i++ )
	{
		*out = p;
		p = (Position*)(p->West);
		out++;
	}
	return p;
}

Position* goEast( Position* start , int count, Position** outpath )
{
	Position* p = start;
	Position** out = outpath;
	for( int i=0; i<count; i++ )
	{
		*out = p;
		p = (Position*)(p->East);
		out++;
	}
	return p;
}

Position* goToLast( Position* start, Position** outpath )
{
	Position** out = outpath;
	*out = start;
	return start;	
}

void fillPath()
{	
	Position* p = (Position*)Board[1][1].East;
	Position** buffer = Path+4;

	Path[0] = &(Board[1][1]);
	Path[1] = &(Board[1][BORDER_SIZE]);
	Path[2] = &(Board[BORDER_SIZE][1]);
	Path[3] = &(Board[BORDER_SIZE][BORDER_SIZE]);

	// first ring
	{
        int ringBorderSize = (BORDER_SIZE-2);
		p = goEast(  p, ringBorderSize, buffer ); buffer+= ringBorderSize;
		p = (Position*) p->South;
		p = goSouth( p, ringBorderSize, buffer ); buffer+= ringBorderSize;
		p = (Position*) p->West;
		p = goWest(  p, ringBorderSize, buffer ); buffer+= ringBorderSize;
		p = (Position*) p->North;
		p = goNorth( p, ringBorderSize, buffer ); buffer+= ringBorderSize;
		p = (Position*) p->South->East;
	}

	for( int i=1; i<=(BORDER_SIZE/2); i++ )
	{
        int ringBorderSize = (BORDER_SIZE-1)-2*i;
		if( ringBorderSize > 0 ) {
			p = goEast(  p, ringBorderSize, buffer ); buffer+= ringBorderSize;
			p = goSouth( p, ringBorderSize, buffer ); buffer+= ringBorderSize;
			p = goWest(  p, ringBorderSize, buffer ); buffer+= ringBorderSize;
			p = goNorth( p, ringBorderSize, buffer ); buffer+= ringBorderSize;
			p = (Position*) p->South->East;
		} else {
			goToLast( p, buffer );
		}
	}

	//debugPath();
}

void debugPath()
{
	std::cout << "== debug Path ==" << std::endl;

	for(int i=0; i< (BORDER_SIZE*BORDER_SIZE) ; i++)
	{
		std::cout << "["<< i << "] => (" << Path[i]->x << ", " << Path[i]->y << ")" << std::endl;
	}
}

void buildWallAt( Position* p )
{
	OrientedPiece* pp = (OrientedPiece*)malloc( sizeof(OrientedPiece) );
	pp->West = WALL;
	pp->North = WALL;
	pp->East = WALL;
	pp->South = WALL;
	pp->Origin = NULL;
	p->Here = pp;
}

void buidEmptyPiece() 
{
	Empty = (OrientedPiece*)malloc( sizeof(OrientedPiece) );
	Empty->West = UNDEFINED;
	Empty->North = UNDEFINED;
	Empty->East = UNDEFINED;
	Empty->South = UNDEFINED;
	Empty->Origin = NULL;
}

void Initialisation()
{
	debug( "Initialisation" );

    // Initializing the common "Empty Piece"
    buidEmptyPiece();

    // Initializing Bag
    for( short i=0; i<BORDER_SIZE*BORDER_SIZE; i++)
	{
		PuzzlePiece p = BagInitializer[i];
		Bag[i] = { p.C1, p.C2, p.C3, p.C4, i, true };
	}

	// Board inner links
	for( int i=0; i<=BORDER_SIZE+1; i++)
	{
		for( int j=0; j<=BORDER_SIZE+1; j++)
		{
			Position* p = &( Board[i][j] );

			p->West		= (j-1>=0  ) ? &( Board[i][j-1] )  : NULL;
			p->South	= (i+1< BORDER_SIZE+2) ? &( Board[i+1][j] )  : NULL;
			p->North	= (i-1>=0  ) ? &( Board[i-1][j] )  : NULL;
			p->East		= (j+1< BORDER_SIZE+2) ? &( Board[i][j+1] )  : NULL;

			p->x = i;
			p->y = j;

			p->Here		= Empty;
		}
	}

	for(int i=0; i<BORDER_SIZE+2; i++) buildWallAt( &(Board[0][i]) );
	for(int i=0; i<BORDER_SIZE+2; i++) buildWallAt( &(Board[i][0]) );
	for(int i=0; i<BORDER_SIZE+2; i++) buildWallAt( &(Board[BORDER_SIZE+1][i]) );
	for(int i=0; i<BORDER_SIZE+2; i++) buildWallAt( &(Board[i][BORDER_SIZE+1]) );

	fillPath();
}

void Reinitialisation() 
{
	// Board reinit
	for(int i=1; i<(BORDER_SIZE+1); i++) {
		for(int j=1; j<(BORDER_SIZE+1); j++) {
			Position* p = &(Board[i][j]);
			if ( p->Here != Empty ) {
				p->Here->Origin->available=true;
			}
			p->Here = Empty;
		}
	}
    // Path already ok

	// Bag reinit
	for(int i=0; i<BORDER_SIZE*BORDER_SIZE; i++) {
		Piece* p = Bag+i;
		p->available = true;
	}

}

char colorToChar( Color c )
{
	return ( c==WALL ? '#' : 'A'+ (((int)c)-1));
}

void debugBag() {
	std::cerr << "debug Bag:" << std::endl;
	for(int i=0; i<BORDER_SIZE*BORDER_SIZE; i++) {
		Piece* p = Bag+i;
		std::cerr << i << " id:" << p->id << " " << colorToChar(p->C1) << " " << colorToChar(p->C2) << " " << colorToChar(p->C3) << " " << colorToChar(p->C4) << std::endl;
	}
}

void fillPiecesOrientees()
{
	debug( "fillPiecesOrientees" );
	
	for( int i=0; i< BORDER_SIZE*BORDER_SIZE; i++ )
	{
		Piece* p = Bag+i;
		p->id = i;
		p->available = true;

		OrientedPiece* pp1 = (OrientedPiece*)malloc( sizeof( OrientedPiece ) );
		pp1->West = p->C1;
		pp1->North = p->C2;
		pp1->East = p->C3;
		pp1->South = p->C4;
		pp1->Origin = p;
		pp1->Orientation = WEST;

		OrientedPiece* pp2 = (OrientedPiece*)malloc( sizeof( OrientedPiece ) );
		pp2->West = p->C4;
		pp2->North = p->C1;
		pp2->East = p->C2;
		pp2->South = p->C3;
		pp2->Origin = p;
		pp2->Orientation = NORTH;

		OrientedPiece* pp3 = (OrientedPiece*)malloc( sizeof( OrientedPiece ) );
		pp3->West = p->C3;
		pp3->North = p->C4;
		pp3->East = p->C1;
		pp3->South = p->C2;
		pp3->Origin = p;
		pp3->Orientation = EAST;

		OrientedPiece* pp4 = (OrientedPiece*)malloc( sizeof( OrientedPiece ) );
		pp4->West = p->C2;
		pp4->North = p->C3;
		pp4->East = p->C4;
		pp4->South = p->C1;
		pp4->Origin = p;
		pp4->Orientation = SOUTH;

		PiecesOrientees[i*4] = pp1;
		PiecesOrientees[i*4+1] = pp2;
		PiecesOrientees[i*4+2] = pp3;
		PiecesOrientees[i*4+3] = pp4;
	}

	//debugBag();
	//debugPiecesOrientees();
}

void findPiecesByConstraintsAndId( int constraintWest, int constraintNorth, int constraintEast, int constraintSouth, short constraintPieceId, OrientedPiece** result ) 
{
	std::vector<OrientedPiece*>* candidatePieces = new std::vector<OrientedPiece*>();

	findPiecesByConstraints( constraintWest, constraintNorth, constraintEast, constraintSouth, candidatePieces );

	for( OrientedPiece* candidate : *candidatePieces )
	{
		if( candidate->Origin->id == constraintPieceId ) 
		{
			*result = candidate;
			break;
		}
	}

	candidatePieces->clear();
	delete(candidatePieces);
}

void findPiecesByConstraints( int constraintWest, int constraintNorth, int constraintEast, int constraintSouth, std::vector<OrientedPiece*>* result )
{
	//debug("findPiecesByConstraints");
	
	int Joker = NB_COLORS;
	
	for( int i=0; i< NB_ORIENTED_PIECES; i++ )
	{
		OrientedPiece* p = PiecesOrientees[i];

		if( p->West==constraintWest || constraintWest==Joker )
		{
			if( p->North==constraintNorth || constraintNorth==Joker )
			{
				if( p->East==constraintEast || constraintEast==Joker )
				{
					if( p->South==constraintSouth || constraintSouth==Joker )
					{
						result->push_back( p );
					}
				}
			}
		}
	}
}

void Indexation()
{
	debug( "Indexation" );

	fillPiecesOrientees();

	for( int west=0; west< NB_COLORS+1; west++ )
	{
		for( int north=0; north< NB_COLORS+1; north++ )
		{
			for( int east=0; east< NB_COLORS+1; east++ )
			{
				for( int south=0; south< NB_COLORS+1; south++ )
				{
					std::vector<OrientedPiece*>* v = new std::vector<OrientedPiece*>();
					Index[west][north][east][south] = v;

					findPiecesByConstraints(west, north, east, south, v);
				}
			}
		}
	}
}

