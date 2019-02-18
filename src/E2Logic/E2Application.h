//
//  Eternity II Solver Common Application entry point 
//
//  Copyright © 2009-2019 Yohan Firmy
//

#include<string>

class Application {

private:
    std::string _name;
    std::string _defaultInitialJob;

public:
    Application(std::string name, std::string defaultInitialJob); 
    int main(int argc, const char * argv[]);
    void usage();
    void help();
};
