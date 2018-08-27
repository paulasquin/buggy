# Buggy

Project by [Paul Asquin](https://www.linkedin.com/in/paulasquin/) for Awabot - Summer 2018 paul.asquin@gmail.com  
  
Buggy subscribes to every available rostopic and republish those topics as /buggy/\*.
It opens a tkinter interface, allowing the user to freeze topics.
You can also modify the rate publication of a topic.

# Installation
```
cd ~
mkdir catkin_ws_buggy
cd catkin_ws_buggy
git clone https://bitbucket.org/awabot/buggy/src/master/ .
catkin_make
echo "source ~/catkin_ws_buggy/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

# Usage
```
rosrun buggy buggy_node.py
```
Please ensure that your application is remapping to /buggy/* topics. You can check this by running 
```
rqt_graph
```

# Parametrisation of [buggy_node.py](src/buggy/src/buggy_node.py)  
**WHITE_LIST_TOPICS** : Choose which topic you want to listen to by editing the  hyperparameter.  
**DISP_RATE** : Choose the disp rate frequency (in second) when topics are frozen.  
**PUBLISH_RATE** : Choose the publish rate of the selected topic.
In the _publish()_ function, you can change the default topic _odom_ for the one(s) you want.  
**DO_RATE** : Activate the specific publish rate for the selected topic.  

# Preview

![Buggy GUI](doc/buggy_interface.png?raw=true "Buggy GUI")
![Buggy RQT Graph](doc/buggy_rqt_graph.png?raw=true "Buggy RQT Graph")