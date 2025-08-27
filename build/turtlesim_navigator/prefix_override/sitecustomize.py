import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/shimanto-khan/Desktop/task/install/turtlesim_navigator'
