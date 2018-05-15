# buggy

Buggy subscribes to every available rostopic and republish those topics as /buggy/*.
It open a tkinter interface, allowing the user to freeze topics.

## Installation

```
cd ~
mkdir catkin_ws_buggy
cd catkin_ws_buggy
git clone https://paulasquinawabot@bitbucket.org/awabot/buggy.git
catkin_make
```
## Usage
```
rosrun buggy buggy_node.py
```
 ## Preview

![Buggy GUI](doc/buggy_interface.png?raw=true "Buggy GUI")
![Buggy RQT Graph](doc/buggy_rqt_graph.png?raw=true "Buggy RQT Graph")