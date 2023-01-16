#! /bin/bash

echo "Stop Grabbing"
rosservice call /camera1/pylon_camera_node_bracketing/stop_grabbing
rosservice call /camera2/pylon_camera_node/stop_grabbing

echo "Set user 1 configuration"
rosservice call /camera1/pylon_camera_node_bracketing/select_user_set "value: 1"
rosservice call /camera2/pylon_camera_node/select_user_set "value: 1"

echo "Load user 1 configuration"
rosservice call /camera1/pylon_camera_node_bracketing/load_user_set
rosservice call /camera2/pylon_camera_node/load_user_set