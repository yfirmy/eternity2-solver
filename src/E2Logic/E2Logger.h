//
//  Eternity II Solver Logger 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#ifndef E2LOGGER
#define E2LOGGER

#include <string>

void debug(const std::string& text);
void info(const std::string& text);
void warning(const std::string& text);
void error(const std::string& text);
void fatal(const std::string& text);

#endif // E2LOGGER
