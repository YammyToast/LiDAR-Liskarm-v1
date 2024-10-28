#include <iostream>
#include <thread>
#include <atomic>

#include <stdio.h>
#include <unistd.h>

#include "spdlog/spdlog.h"
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/sinks/basic_file_sink.h"

#include "wiringPi.h"

int main(int argc, char **argv) {
    // Logger
    auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
    auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>("logs/session-log.log", false);

    spdlog::logger logger("session_logger", {console_sink, file_sink});
    // logger = std::make_shared<spdlog::logger>(logger);

    // if (debug_flag == true)
    // {
    logger.set_level(spdlog::level::debug);
    // }
    logger.set_pattern("[%H:%M:%S] [%^%l%$] %v");
    logger.debug("Debug logging on");

    logger.info("Hello World from Spdlog!");
    return 0;

} 