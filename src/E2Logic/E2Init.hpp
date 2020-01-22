//
//  Eternity II Solver Initialization Utils 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifndef E2INIT
#define E2INIT

#include <vector>
#include "E2Model/E2Types.h"

void Initialisation();
void Reinitialisation();
void Indexation();

void findPiecesByConstraints( int constraintWest, int constraintNorth, int constraintEast, int constraintSouth, std::vector<OrientedPiece*>* result );
void findPiecesByConstraintsAndId( int constraintWest, int constraintNorth, int constraintEast, int constraintSouth, short constraintPieceId, OrientedPiece** result );

#endif // E2INIT