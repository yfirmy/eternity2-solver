//
//  Eternity II Solver Logger 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#include <string>
#include <iostream>
#include <sstream>

void debug(const std::string& text) {
    std::cout << "DEBUG " << text << std::endl;
}

void info(const std::string& text) {
    std::cout << "INFO " << text << std::endl;
}

void warning(const std::string& text) {
    std::cout << "WARN " << text << std::endl;
}

void error(const std::string& text) {
    std::cout << "ERROR " << text << std::endl;
}

void fatal(const std::string& text) {
    std::cerr << "FATAL " << text << std::endl;
}