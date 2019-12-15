//
//  Eternity II Solver Tiles
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifdef PUZZLE

#ifndef PUZZLETILES
#define PUZZLETILES

#include "E2Model/E2Types.h"

Piece Bag[256];

PuzzlePiece BagInitializer[256] = {

  {WALL,A,C,WALL},
  {WALL,A,M,WALL},
  {WALL,B,C,WALL},
  {WALL,C,B,WALL},
  {A,D,A,WALL},
  {A,E,B,WALL},
  {A,P,A,WALL},
  {A,P,N,WALL},
  
  // OK
  
  {A,H,C,WALL},
  {A,S,M,WALL},
  {A,T,B,WALL},
  {A,U,M,WALL},
  {A,U,N,WALL},
  {A,O,M,WALL},
  {B,E,A,WALL},
  {B,F,C,WALL},
  
  // OK
  
  {B,Q,N,WALL},
  {B,I,N,WALL},
  {B,S,B,WALL},
  {B,T,B,WALL},
  {B,J,M,WALL},
  {B,K,A,WALL},
  {B,K,N,WALL},
  {B,L,A,WALL},
  
  // OK
  
  {B,O,A,WALL},
  {C,D,B,WALL},
  {C,D,C,WALL},
  {C,E,C,WALL},
  {C,F,C,WALL},
  {C,S,N,WALL},
  {C,T,B,WALL},
  {C,L,C,WALL},
  
  // OK
  
  {C,U,B,WALL},
  {C,U,M,WALL},
  {C,V,N,WALL},
  {C,R,M,WALL},
  {M,F,A,WALL},
  {M,G,N,WALL},
  {M,H,N,WALL},
  {M,I,B,WALL},
  
  // OK
  
  {M,I,C,WALL},
  {M,T,A,WALL},
  {M,T,B,WALL},
  {M,T,C,WALL},
  {M,J,A,WALL},
  {M,L,M,WALL},
  {M,U,M,WALL},
  {M,V,M,WALL},
  
  // OK pour tableau A
  
  {N,D,N,WALL},
  {N,E,A,WALL},
  {N,E,B,WALL},
  {N,P,A,WALL},
  {N,S,M,WALL},
  {N,J,M,WALL},
  {N,J,N,WALL},
  {N,U,C,WALL},
  
  // OK
  
  {N,V,A,WALL},
  {N,V,N,WALL},
  {N,O,B,WALL},
  {N,R,C,WALL},
  {D,P,F,D},
  {D,Q,S,D},
  {E,E,G,D},
  {F,D,U,D},
  
  // OK
  
  {F,F,R,D},
  {F,Q,Q,D},
  {F,H,E,D},
  {F,L,P,D},
  {F,R,U,D},
  {G,G,S,D},
  {G,S,K,D},
  {H,Q,F,D},
  
  // OK
  
  {H,T,J,D},
  {H,L,T,D},
  {H,U,G,D},
  {I,Q,T,D},
  {I,I,T,D},
  {S,G,V,D},
  {S,L,G,D},
  {S,V,O,D},
  
  // OK
  
  {T,I,F,D},
  {J,F,F,D},
  {J,H,J,D},
  {K,F,I,D},
  {K,P,Q,D},
  {K,U,K,D},
  {K,V,L,D},
  {L,D,O,D},
  
  // OK
  
  {L,P,R,D},
  {L,J,V,D},
  {U,H,K,D},
  {U,I,T,D},
  {U,I,J,D},
  {U,J,O,D},
  {U,K,Q,D},
  {O,O,G,D},
  
  // OK POUR PLATEAU B
  
  {R,J,I,D},
  {R,L,U,D},
  {R,O,P,D},
  {R,R,O,D},
  {E,K,T,E},
  {E,K,V,E},
  {E,V,I,E},
  {E,R,P,E},
  
  // OK
  
  {F,J,T,E},
  {P,G,U,E},
  {P,I,U,E},
  {P,J,T,E},
  {P,V,H,E},
  {Q,T,K,E},
  {Q,K,T,E},
  {G,L,I,E},
  
  // OK
  
  {G,L,V,E},
  {H,Q,J,E},
  {H,S,K,E},
  {H,K,H,E},
  {H,R,V,E},
  {I,G,O,E},
  {S,V,K,E},
  {T,U,R,E},
  
  // OK
  
  {J,Q,R,E},
  {L,P,V,E},
  {L,Q,I,E},
  {L,L,T,E},
  {U,K,R,E},
  {U,O,T,E},
  {V,Q,P,E},
  {V,I,O,E},
  
  // OK
  
  {V,J,G,E},
  {V,L,U,E},
  {O,P,L,E},
  {O,K,Q,E},
  {R,Q,V,E},
  {R,H,J,E},
  {R,J,G,E},
  {R,V,L,E},
  
  // OK
  
  {F,L,S,F},
  {P,P,G,F},
  {P,P,H,F},
  {P,P,K,F},
  {P,I,O,F},
  {P,T,P,F},
  {P,V,K,F},
  {P,O,O,F},
  
  // OK POUR PLATEAU C
  
  {Q,G,J,F},
  {G,F,K,F},
  {G,F,R,F},
  {G,G,Q,F},
  {G,T,K,F},
  {I,P,H,F},
  {I,J,R,F},
  {S,H,H,F},
  
  // OK
  
  {S,H,I,F},
  {S,R,V,F},
  {J,S,S,F},
  {J,S,K,F},
  {J,R,S,F},
  {L,S,V,F},
  {L,U,P,F},
  {U,O,O,F},
  
  // OK
  
  {V,P,L,F},
  {V,Q,L,F},
  {R,T,H,F},
  {R,J,V,F},
  {Q,G,J,P},
  {Q,J,U,P},
  {H,G,G,P},
  {I,H,T,P},
  
  // OK
  
  {I,I,O,P},
  {S,J,U,P},
  {S,L,V,P},
  {S,O,H,P},
  {T,T,T,P},
  {T,K,L,P},
  {J,S,O,P},
  {K,S,I,P},
  
  // OK
  
  {L,Q,J,P},
  {U,K,V,P},
  {U,U,T,P},
  {V,S,V,P},
  {O,H,V,P},
  {O,S,H,P},
  {Q,I,U,Q},
  {G,R,S,Q},
  
  // OK
  
  {H,I,K,Q},
  {H,U,U,Q},
  {I,O,S,Q},
  {S,Q,O,Q},
  {S,G,I,Q},
  {S,V,I,Q},
  {T,G,G,Q},
  {T,T,L,Q},
  
  // OK POUR TABLEAU D
  
  {J,H,S,Q},
  {K,O,H,Q},
  {K,O,R,Q},
  {K,Q,T,Q},
  {L,H,R,Q},
  {L,I,U,Q},
  {L,L,L,Q},
  {U,I,G,Q},
  
  // OK
  
  {V,O,U,Q},
  {V,R,S,Q},
  {O,K,I,Q},
  {O,K,U,Q},
  {O,V,G,Q},
  {O,R,O,Q},
  {G,R,S,G},
  {H,I,R,G},
  
  // OK
  
  {H,U,T,G},
  {S,H,I,G},
  {S,V,T,G},
  {T,G,V,G},
  {J,U,U,G},
  {K,G,L,G},
  {K,J,R,G},
  {K,R,O,G},
  
  // OK
  
  {L,I,T,G},
  {V,J,K,G},
  {O,H,J,G},
  {R,H,V,G},
  {R,O,O,G},
  {R,O,R,G},
  {H,K,R,H},
  {H,L,S,H},
  
  // OK
  
  {H,V,T,H},
  {S,I,T,H},
  {S,K,K,H},
  {J,I,U,H},
  {L,S,R,H},
  {L,V,U,H},
  {U,K,L,H},
  {U,K,O,H},
  
  // OK
  
  {I,I,L,I},
  {S,V,J,I},
  {J,S,J,I},
  {J,S,L,I},
  {J,K,T,I},
  {K,J,V,I},
  {L,T,R,I},
  {L,O,T,I},
  
  // OK POUR TABLEAU E
  
  {U,S,O,I},
  {U,J,O,I},
  {T,T,K,S},
  {T,L,U,S},
  
  {J,R,L,S},
  {O,V,R,S},
  {T,O,R,T},
  {J,K,J,T},
  
  {K,J,O,T},
  {L,V,O,T},
  {J,R,U,J},
  {K,U,K,J},
  
  {U,V,L,K},
  {V,O,V,L},
  {R,V,R,L},
  {R,O,R,U}
  
};

#endif

#endif
