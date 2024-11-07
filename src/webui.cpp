// #ifndef _WEBUI_CPP_
// #define _WEBUI_CPP_

#include <sstream>
#include <iostream>
#include <fstream>

#include "shared.cpp"

std::string build_webpage() {
    std::ifstream file("/ui/index.html");
    if (!file) {
        shared.logger->error("Could not open file: /ui/index.html");
        return "";
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

// #endif