

import time
import json
import rospy
from std_msgs.msg import String
rospy.init_node('sender')
pub = rospy.Publisher('/iFoil/allObjects', String, queue_size=550)
objects= [
        {'objectId': 'ojb1', 'color':'red','category':'apple', 'ownership':'Farid','restriction':'doNotEat'},
        {'objectId': 'obj2','color':'blue','category':'orange', 'ownership':'lili'},
        {'objectId': 'obj3', 'color':'red','category':'apple', 'ownership':'Farid'},
        {'objectId': 'obj4', 'color':'yellow','category':'banana', 'ownership':'Farid','restriction':'doNotEat'},
        {'objectId': 'obj5', 'color':'yellow','category':'apple', 'ownership':'Farid','restriction':'doNotEat'},
        {'objectId': 'obj7','color':'red','category':'apple', 'ownership':'lili', 'restriction':'doNotEat'}
        ]
objects = json.dumps(objects)

#for i in range(10000):
#    pub.publish(objects)
    
    
pub1 = rospy.Publisher('/iFoil/probFoil/query', String, queue_size=550)
for i in range(100000):
    pub1.publish(str(['ownership','Farid']))



