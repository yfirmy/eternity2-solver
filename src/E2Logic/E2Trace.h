//
//  Eternity II Solver Debugging/Tracing tools 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifndef E2TRACE
#define E2TRACE

#include "E2Model/E2Types.h"

void traceBoard();
char traceDirection( Direction dir );
char traceConstraint( short c );
void tracePiece( OrientedPiece* pp );
void traceJob();

void traceCurrentDate();

void debugIndex();

#endif // E2TRACE
