#!/usr/bin/env python

# Buggy package, created by Paul Asquin - May 2018
# Subscribe to every available rostopic, republish those topics as /buggy/*.
# Open a tkinter interface, allowing to freeze topics

import rospy
import rostopic
from std_msgs.msg import String
from Tkinter import *
import subprocess
import threading 
import time

# Initialize the node with rospy
rospy.init_node('buggy_node')
# Create publisher
topicsState = []
window = Tk()
buggyPrefix = "/buggy"
publishFlag = True

lesSub = []
lesPub = []
lesMsgs = []

# Define Timer callback
def callback(event):
	msg = String()
	#msg.data = "j'ai un message pour toi : %s !" % (hello.sayHello())
	publisher.publish(msg)
	#print(getTopics())

def setSubAndPub():
	""" Create subscribers for every topic in topicsStates, create buggy publishers and initialize msgs list """
	global lesSub
	lesSub = []
	global lesPub
	lesPub = []

	for i in range(len(topicsState)):
		topicClass = rostopic.get_topic_class(topicsState[i][0], blocking=False)[0]
		lesSub.append( rospy.Subscriber(topicsState[i][0], topicClass, setMsg, i) )
		lesPub.append( rospy.Publisher(buggyPrefix + topicsState[i][0], topicClass, queue_size=10) )
		lesMsgs.append(None)

def setMsg(data, i):
	""" Write msgs send from subsriber to global variable """
	global lesMsgs
	lesMsgs[i] = data

def publish():
	global lesPub
	global lesSub

	# Read parameter
	#pub_period = rospy.get_param("~pub_period", 1.0)
	# Create timer
	#rospy.Timer(rospy.Duration.from_sec(pub_period), callback)
	
	# Not published print timer set to 0.5 sec
	dispRate = 0.5
	lastPrint = time.time()-dispRate

	while publishFlag:
		notPublish = ""
		for i in range(len(topicsState)):
			if topicsState[i][1].get() == 1 and lesMsgs[i]!= None:
				lesPub[i].publish(lesMsgs[i])
			elif topicsState[i][1].get() == 0:
				notPublish += buggyPrefix + str(topicsState[i][0]) + "\n"
		if notPublish != "" and time.time() > lastPrint + dispRate:
			print("freezing : \n" + notPublish)
			lastPrint = time.time()

def getTopics():
	""" Return ROS topics """
	p = subprocess.Popen(["rostopic", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	topics = out.decode('utf-8')
	topics = topics.split('\n')
	topics.pop()  # We delete last, empty, element
	topicsExtern = []
	
	# We exlude topics that we may have created in a previous cycle
	for top in topics:
		if top[0:len(buggyPrefix)] != buggyPrefix:
			topicsExtern.append(top)
	
	return (topicsExtern)

def getTopicsState():
	""" Write the global variable with topics name and publish state variable """
	global topicsState
	topicsState = []
	topics = getTopics()
	for i in range(len(topics)):
		topicsState.append([str(topics[i]), IntVar()])

def refreshGUI():
	""" Refresh global variable topicsState,
	destroy the actual interface and create another one """
	global window
	window.destroy()
	window = Tk()
	graphicInterface()

def exitGUI():
	global window
	window.destroy()
	publishFlag = False

def graphicInterface():
	""" Create interface to check topic to publish or block """
	global topicsState
	global window
	global publishFlag
	getTopicsState()
	setSubAndPub()

	lesButtons = []
	# Create Tk interface
	window.title('Buggy - block your topics')
	FrameTopics = LabelFrame(window, text='Freeze '+ buggyPrefix, borderwidth=1)
	FrameTopics.grid(row=1, sticky=W, padx=5, pady=5)
	
	for i in range(len(topicsState)):
		lesButtons.append(Checkbutton(FrameTopics, text=topicsState[i][0], variable=topicsState[i][1]))
		lesButtons[-1].grid(row=i, sticky=W)
		lesButtons[-1].select()
		
	Button(window, text='Refresh', command=refreshGUI).grid(row=2, sticky=W, padx=5, pady=5)
	Button(window, text='Quit', command=exitGUI).grid(row=3, sticky=W, padx=5, pady=5)

	thread = threading.Thread(target=publish)
	thread.daemon = True
	thread.start()
	window.mainloop()


def main():
	
	graphicInterface()


if __name__ == '__main__':
	main()
