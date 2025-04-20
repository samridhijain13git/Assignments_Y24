import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/samridhi/Desktop/Assignments_Y24/ros2_ws/install/talker_package'
