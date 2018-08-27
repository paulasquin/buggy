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
les_topics_state = []
window = Tk()
buggy_prefix = "/buggy"
publish_flag = True

les_sub = []
les_pub = []
les_msgs = []
les_seq = []

WHITE_LIST_TOPICS = [	
					'/camera/depth/camera_info'
					'/camera/depth/image_raw',
					'/camera/depth/points',
					'/camera/rgb/camera_info',
					'/camera/rgb/image_raw',
					'/clock',
					'/odom',
					'/rosout',
					'/rosout_agg',
					'/scan',
					'/tf'
]

# Set topics to ignore
IGNORED_TOPICS = ['/submap_list', '/scan_matched_points2']

# Define Timer callback
def callback(event):
	msg = String()
	#msg.data = "j'ai un message pour toi : %s !" % (hello.sayHello())
	publisher.publish(msg)
	#print(getTopics())

def setSubAndPub():
	""" Create subscribers for every topic in les_topics_states, create buggy publishers and initialize msgs list """
	global les_sub
	les_sub = []
	global les_pub
	les_pub = []

	for i in range(len(les_topics_state)):
		topic_class = rostopic.get_topic_class(les_topics_state[i][0], blocking=False)[0]
		les_sub.append( rospy.Subscriber(les_topics_state[i][0], topic_class, setMsg, i) )
		les_pub.append( rospy.Publisher(buggy_prefix + les_topics_state[i][0], topic_class, queue_size=10) )
		les_msgs.append(None)
		les_seq.append(0) 

def setMsg(data, i):
	""" Write msgs send from subsriber to global variable """
	global les_msgs
	les_msgs[i] = data

def publish():
	global les_pub
	global les_sub

	# Read parameter
	#pub_period = rospy.get_param("~pub_period", 1.0)
	# Create timer
	#rospy.Timer(rospy.Duration.from_sec(pub_period), callback)
	
	# Not published print timer set to 0.5 sec
	disp_rate = 0.5
	publish_rate = 3.0 #10Hz (0.1s)
	last_print = time.time()-disp_rate
	last_publish = 0

	while publish_flag:
		not_published = ""
		seq = 0
		for i in range(len(les_topics_state)):
			try:
				seq = les_msgs[i].header.seq
			except AttributeError:
				if les_topics_state[i][1].get() == 1 and les_msgs[i]!= None:
					les_pub[i].publish(les_msgs[i])
				continue
			if les_topics_state[i][1].get() == 1 and les_msgs[i]!= None and seq > les_seq[i]:
				#Test for decreasing odom publish rate
				#if "odom" not in les_topics_state[i][0]:
				if True:
					les_pub[i].publish(les_msgs[i])
					les_seq[i] = seq
				elif last_publish + publish_rate < time.time(): #If odom but we waited enought time for another publish
					print("Publising odom at rate : " + str(publish_rate) + " sec")
					last_publish = time.time()
					les_pub[i].publish(les_msgs[i])
					les_seq[i] = seq

			elif les_topics_state[i][1].get() == 0:
				not_published += buggy_prefix + str(les_topics_state[i][0]) + "\n"
		if not_published != "" and time.time() > last_print + disp_rate:
			print("freezing : \n" + not_published)
			last_print = time.time()

def getTopics():
	""" Return ROS topics """
	p = subprocess.Popen(["rostopic", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	topics = out.decode('utf-8')
	topics = topics.split('\n')
	topics.pop()  # We delete the last, empty, element
	topicsExtern = []
	
	# We exlude topics that we may have created in a previous cycle
	for top in topics:
		if top[0:len(buggy_prefix)] != buggy_prefix:
			topicsExtern.append(top)
	
	return (topicsExtern)

def getTopicsState():
	""" Write the global variable with topics name and publish state variable """
	global les_topics_state
	les_topics_state = []
	topics = getTopics()
	for i in range(len(topics)):
		writeTopic = False

		#If we defined a white list and the topic is in it
		if len(WHITE_LIST_TOPICS) > 0 and topics[i] in WHITE_LIST_TOPICS:
			writeTopic = True
		#If we did not defined a white list
		elif len(WHITE_LIST_TOPICS) == 0:
			writeTopic = True

		# Write the topics in the listened topics
		if writeTopic:
			les_topics_state.append([str(topics[i]), IntVar()])

def refreshGUI():
	""" Refresh global variable les_topics_state,
	destroy the actual interface and create another one """
	global window
	window.destroy()
	window = Tk()
	graphicInterface()

def exitGUI():
	global window
	window.destroy()
	publish_flag = False

def graphicInterface():
	""" Create interface to check topic to publish or block """
	global les_topics_state
	global window
	global publish_flag

	lesButtons = []
	# Create Tk interface
	window.title('Buggy - block your topics')
	window.option_add("*Font", "courier 16")

	FrameTopics = LabelFrame(window, text='Freeze '+ buggy_prefix, borderwidth=1)
	FrameTopics.grid(row=1, sticky=W, padx=5, pady=5)
	
	for i in range(len(les_topics_state)):
		lesButtons.append(Checkbutton(FrameTopics, text=les_topics_state[i][0], variable=les_topics_state[i][1]))
		lesButtons[-1].grid(row=i, sticky=W)
		lesButtons[-1].select()
		
	Button(window, text='Refresh', command=refreshGUI).grid(row=2, sticky=W, padx=5, pady=5)
	Button(window, text='Quit', command=exitGUI).grid(row=3, sticky=W, padx=5, pady=5)

	try:
		thread = threading.Thread(target=publish)
		thread.daemon = True
		thread.start()
		window.mainloop()
	except KeyboardInterrupt:
		exitGUI()
		return 0

def main():
	getTopicsState()
	setSubAndPub()
	try:
		graphicInterface()
	except KeyboardInterrupt:
		return 0

if __name__ == '__main__':
	main()
