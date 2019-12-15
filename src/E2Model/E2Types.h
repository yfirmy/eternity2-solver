//
//  Eternity II Solver Data Types 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifndef E2TYPES
#define E2TYPES

enum Color {WALL,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V};
enum Direction {NORTH, WEST, EAST, SOUTH};

#define NB_COLORS 23

struct Piece
{ 
	Color C1; 
	Color C2; 
	Color C3; 
	Color C4;

	short id;
	bool available;
};

struct OrientedPiece
{
	Color North;
	Color West;
	Color East;
	Color South;

	Piece* Origin;
	Direction Orientation;
};

struct Position
{
	const Position* North;
	const Position* West;
	const Position* East;
	const Position* South;

	int x, y;

	OrientedPiece* Here;
};

struct PuzzlePiece
{ 
	Color C1; 
	Color C2; 
	Color C3; 
	Color C4;
};

#endif // E2TYPES
