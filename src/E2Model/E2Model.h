//
//  Eternity II Solver Data Model 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifndef E2Model_h
#define E2Model_h

#include "E2Model/E2Types.h"
#include "E2Logic/E2Size.h"
#include <vector>

// C-style global structures for fast access

#define NB_ORIENTED_PIECES ( BORDER_SIZE * BORDER_SIZE )*4

extern Position Board[BORDER_SIZE+2][BORDER_SIZE+2];

extern Position* Path[BORDER_SIZE*BORDER_SIZE];

extern OrientedPiece* PiecesOrientees[NB_ORIENTED_PIECES];

extern std::vector<OrientedPiece*>* Index[NB_COLORS+1][NB_COLORS+1][NB_COLORS+1][NB_COLORS+1]; 

extern Piece Bag[BORDER_SIZE*BORDER_SIZE];

extern PuzzlePiece BagInitializer[BORDER_SIZE*BORDER_SIZE];

#endif // E2Model_h
