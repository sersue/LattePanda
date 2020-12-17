import rospy
from std_msgs.msg import String



def callback(data):
    if(data.data=="2"):
        pub1 = rospy.Publisher('TerminalToPyqt',String,queue_size=10)
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        rospy.sleep(0.5)
        pub1.publish("0")
        rospy.loginfo('I published 0')
    elif(data.data=="hi"):
        pub1 = rospy.Publisher('TerminalToPyqt1',String,queue_size=10)
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        rospy.sleep(0.5)
        pub1.publish("hi1")
        rospy.loginfo('I published 4')
    elif(data.data=="nocup"):
        pub1 = rospy.Publisher('TerminalToPyqt1',String,queue_size=10)
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        rospy.sleep(0.5)
        pub1.publish("5")
        rospy.loginfo('I published 5')
    elif(data.data=="4"):
        pub1 = rospy.Publisher('TerminalToPyqt1',String,queue_size=10)
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        rospy.sleep(0.5)
        pub1.publish("6")
        rospy.loginfo('I published 6')
    elif(data.data=="donation"):
        pub1 = rospy.Publisher('TerminalToPyqt1',String,queue_size=10)
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        rospy.sleep(0.5)
        pub1.publish("7")
        rospy.loginfo('I published 7')
    elif(data.data=="lastvideo"):
        pub1 = rospy.Publisher('TerminalToPyqt1',String,queue_size=10)
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        rospy.sleep(0.5)
        pub1.publish("lastvideo1")
        rospy.loginfo('I published lastvideo1')   
    else:
        print("Get Message: error ")

def listener():
    
    rospy.Subscriber('TerminalToPyqt',String,callback)
    rospy.Subscriber('TerminalToPyqt1',String,callback)

def talker():
    pub = rospy.Publisher('chatter',String,queue_size=10)
    rospy.init_node('terminal',anonymous=True)
    
    listener()

    while(1):
        print("##############")
        print("1: 화면 변경")
        key = int(input('input number :'))
        # if(key ==0):
        #     hello_str="0"
        #     rospy.loginfo(hello_str)
        #     pub.publish(hello_str)
        if(key ==1):
            hello_str="1"
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
        elif(key ==2):
            hello_str="2"
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
        elif(key ==3):
            hello_str="3"
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
        elif(key ==4):
            hello_str="4"
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
        elif(key ==5):
            hello_str="5"
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
        

        else:
            print("not accessed message")

if __name__ =='__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass        


        