//
//  Eternity II Solver "Control Sample Version" Tiles
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifdef SAMPLE

#ifndef SAMPLETILES
#define SAMPLETILES

#include "E2Model/E2Types.h"

Piece Bag[25];

PuzzlePiece BagInitializer[25] = {
    
    {WALL,WALL,A,E},
    {A,WALL,B,F},
    {B,WALL,C,G},
    {C,WALL,D,H},
    {D,WALL,WALL,I},
    
    {WALL,E,J,N},
    {J,F,K,O},
    {K,G,L,P},
    {L,H,M,Q},
    {M,I,WALL,R},

    {WALL,N,S,A},
    {S,O,T,B},
    {T,P,U,C},
    {U,Q,V,D},
    {V,R,WALL,E},

    {WALL,A,F,J},
    {F,B,G,K},
    {G,C,H,L},
    {H,D,I,M},
    {I,E,WALL,N},

    {WALL,J,O,WALL},
    {O,K,P,WALL},
    {P,L,Q,WALL},
    {Q,M,R,WALL},
    {R,N,WALL,WALL}
    
};

#endif

#endif
