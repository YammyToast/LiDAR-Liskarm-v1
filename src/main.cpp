#include <iostream>
#include <thread>
#include <atomic>
#include <chrono>

#include <stdio.h>
#include <unistd.h>

#include "spdlog/spdlog.h"
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/sinks/basic_file_sink.h"

#include <pigpio.h>

#include "httplib.h"

#define PIN_SERVO_PWM 12

std::atomic<bool> interrupt_flag(false);

int main(int argc, char **argv) {

    // START INIT
    if (gpioInitialise() < 0) {
        std::cerr << "pigpio failed to initialize" << std::endl;
        return 1;
    }
    std::cout << "pigpio initialized" << std::endl;

    bool debug_flag = true;
    
    // Logger
    auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
    auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>("logs/session-log.log", false);

    spdlog::logger logger("session_logger", {console_sink, file_sink});

    if (debug_flag == true)
    {
        logger.set_level(spdlog::level::debug);
    }
    logger.set_pattern("[%H:%M:%S] [%^%l%$] %v");
    logger.debug("Debug logging on");
    // END INIT
    // HTTPSERVER
    httplib::Server server;
    server.Get("/", [](const httplib::Request &req, httplib::Response &res) {
        std::cout << "test" << std::endl;
        res.set_content("Hello World", "text/plain");

    });
    server.listen("0.0.0.0", 18080);
    
    // // Pin Setup
    // gpioSetMode(PIN_SERVO_PWM, PI_INPUT);
    // int frequency = 50;
    // gpioSetPWMfrequency(PIN_SERVO_PWM, frequency);
    // int min_pulse_width = 5;
    // int max_pulse_width = 25;

    // for (int angle = 0; angle <= 180; angle+= 10) {
    //     int pulse_width = min_pulse_width + (angle * (max_pulse_width - min_pulse_width) / 180);

    //     gpioPWM(PIN_SERVO_PWM, pulse_width / 10);
    //     std::cout << "Angle: " << angle << "°, Pulse Width: " << pulse_width << "µs" << std::endl;
    //     std::this_thread::sleep_for(std::chrono::milliseconds(500));
    // }

    // // while (!interrupt_flag) {
        
    // //     std::this_thread::sleep_for(std::chrono::seconds(1));

    // // }
    // gpioPWM(PIN_SERVO_PWM, 0);  // Turn off PWM signal to the pin
    // gpioTerminate();
    return 0;

} 