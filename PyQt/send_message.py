import rospy
from std_msgs.msg import String

def callback(data):
    if(data.data=="chatter"):
        print("Get Message: chatter")
    # elif(data.data==""):
    #     print("Get Message: ")
    else:
        print("Get Message: error ")

def listener():
    rospy.Subscriber('TerminalToPyqt',String,callback)

def talker():
    pub = rospy.Publisher('chatter',String,queue_size=10)
    rospy.init_node('terminal',anonymous=True)
    
    listener()

    while(1):
        print("##############")
        print("1: 화면 변경")
        key = int(input('input number :'))
        if(key ==0):
            hello_str="0"
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
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
        


        