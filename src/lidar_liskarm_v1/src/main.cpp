#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class Liskarm_Main : public rclcpp::Node
{
    public:

        Liskarm_Main()
        : Node("liskarm_main"), count_(0)
        {
            state_publisher_ = this->create_publisher<std_msgs::msg::String>("liskarm_state", 10);
            timer_ = this->create_wall_timer(
                500ms, std::bind(&Liskarm_Main::timer_callback, this)
            );
        }

    private:
        void timer_callback()
        {
            auto message = std_msgs::msg::String();
            message.data = "Hello, World! " + std::to_string(count_++);
            RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
            state_publisher_->publish(message);

        }

        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<std_msgs::msg::String>::SharedPtr state_publisher_;
        size_t count_;


};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Liskarm_Main>());
    rclcpp::shutdown();
    return 0;

}