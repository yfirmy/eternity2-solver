//
//  Eternity II "Clue 1" Tiles
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifdef CLUE1

#ifndef CLUE1TILES
#define CLUE1TILES

#include "E2Model/E2Types.h"

Piece Bag[36] = {
    
    {E,E,F,F},
    {F,E,F,E},
    {D,E,F,E},
    {D,E,F,F},
    {D,E,F,E},
    {D,E,E,F},
    
    {B,F,M,WALL},
    {E,E,F,F},
    {E,F,E,E},
    {WALL,A,F,A},
    {WALL,A,E,B},
    {A,WALL,M,F},
    
    {E,A,WALL,C},
    {WALL,M,C,WALL},
    {C,WALL,B,F},
    {B,E,A,WALL},
    {E,C,WALL,C},
    {WALL,A,F,B},
    
    {E,F,E,F},
    {C,WALL,A,F},
    {B,F,A,WALL},
    {WALL,B,E,M},
    {C,F,B,WALL},
    {E,F,F,E},
    
    {WALL,M,F,B},
    {WALL,WALL,M,M},
    {E,F,E,E},
    {M,WALL,C,F},
    {E,D,D,E},
    {F,F,F,D},
    
    {E,C,WALL,A},
    {E,F,F,F},
    {E,F,F,D},
    {WALL,WALL,C,B},
    {F,F,E,F},
    {M,WALL,WALL,M}
    
};

#endif // CLUE1TILES

#endif // CLUE1
