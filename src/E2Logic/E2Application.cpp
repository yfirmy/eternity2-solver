//
//  Eternity II Solver Common Application entry point 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#include <iostream>

#include "E2Application.h"
#include "E2Solver.h"
#include "E2Logger.h"
#include "E2Size.h"

#define VERSION "1.5.0"

Application::Application(std::string name, std::string defaultInitialJob) : _name(name), _defaultInitialJob(defaultInitialJob) {
}

void Application::usage() {
    info("No mandatory parameters.");
    info("Optionnal parameters:");
    info("\t--version");
    info("\t--help");
}

void Application::help() {
    usage();
    info("Initial job can be an empty puzzle board: " + this->_defaultInitialJob);
}

int Application::main(int argc, const char * argv[]) {

    info("Eternity 2 Backtracker - " + this->_name);
    info("Version: " + std::string(VERSION));

#ifdef DEPTH_FIRST_SEARCH
    info("Compiled for Depth-First Search");
#endif

#ifdef BREADTH_FIRST_SEARCH
    info("Compiled for Breadth-First Search (1 level)");
#endif

    if (argc > 2 ) {
        usage();
        exit(1);
    }

    if (argc == 2 ) {
        if( std::string(argv[1]) == "-v" || std::string(argv[1]) == "--version" ) {
           info("Version: " + std::string(VERSION));
        }
        if( std::string(argv[1]) == "-h" || std::string(argv[1]) == "--help" ) {
           help();
        }
    } else {

        info("Starting initialisation");
        E2Solver* worker = new E2Solver();
        info("Application started");
        
        while(true) {
            info("Ready to process requests");
            std::cout << "Enter job > ";
            std::string job;
            std::cin >> job;
            std::cout << std::endl;
            info("Request : " +job);
            if( job.compare("exit")==0 || job.compare("quit")==0  ) {
                info("Goodbye.");
                break;
            } else {
            int solutionCount = worker->solve(job);
            info("Found " + std::to_string(solutionCount) + " solution" + (solutionCount>1?"s":"")) ;
            }
        }
    }
    
    return 0;
}
