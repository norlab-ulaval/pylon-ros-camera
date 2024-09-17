#!/usr/bin/env python3
# Simple script to test the feature to fetch the camera's time stamp.
# Compares ROS2 time and camera time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

prev_ros_time = prev_img_time = None

class CompareTimestamps(Node):
    def __init__(self):
        super().__init__('compare_ros_and_image_timestamp')
        self.subscription = self.create_subscription(
            Image,
            '/basler/driver/image_raw',
            self.callback,
            10
        )

    @staticmethod
    def substract_time(time1, time2):
        secs = time1.seconds_nanoseconds()[0] - time2.seconds_nanoseconds()[0]
        nsecs = time1.seconds_nanoseconds()[1] - time2.seconds_nanoseconds()[1]
        dur = secs + nsecs / 1e9
        return dur * 1e3

    @staticmethod
    def substract_time2(time1, time2):
        secs = time1.sec - time2.sec
        nsecs = time1.nanosec - time2.nanosec
        dur = secs + nsecs / 1e9
        return dur * 1e3
    def callback(self, msg):
        global prev_ros_time, prev_img_time
        new_ros_time = self.get_clock().now()
        new_img_time = msg.header.stamp
        if prev_ros_time is not None and prev_img_time is not None:
            ros_dur = self.substract_time(new_ros_time, prev_ros_time)
            img_dur = self.substract_time2(new_img_time, prev_img_time)
            # self.get_logger().info(f'ROS time: {new_ros_time.seconds_nanoseconds()[0]} seconds and {new_ros_time.seconds_nanoseconds()[1]} nanoseconds')
            # self.get_logger().info(f'Image time: {new_img_time.sec} seconds and {new_img_time.nanosec} nanoseconds')
            self.get_logger().info(f'ROS duration: {ros_dur:5.5} ms')
            self.get_logger().info(f'Image duration: {img_dur:5.5} ms')
        prev_ros_time = new_ros_time
        prev_img_time = new_img_time

def main(args=None):
    rclpy.init(args=args)
    compare_timestamps = CompareTimestamps()
    rclpy.spin(compare_timestamps)
    compare_timestamps.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
