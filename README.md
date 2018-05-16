# Buggy

Buggy subscribes to every available rostopic and republish those topics as /buggy/*.
It open a tkinter interface, allowing the user to freeze topics.

Project by Paul Asquin for Awabot - May 2018
paul.asquin@gmail.com

## Installation
```
cd ~
mkdir catkin_ws_buggy
cd catkin_ws_buggy
git clone https://bitbucket.org/awabot/buggy/src/master/ .
catkin_make
echo "source ~/catkin_ws_buggy/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Usage
```
rosrun buggy buggy_node.py
```
You have to remap your application to /buggy/* topics.

 ## Preview

![Buggy GUI](doc/buggy_interface.png?raw=true "Buggy GUI")
![Buggy RQT Graph](doc/buggy_rqt_graph.png?raw=true "Buggy RQT Graph")