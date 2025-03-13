# -*- coding: utf-8 -*-

import json
import rospy
from std_msgs.msg import String

class ObjectDetector:
    def __init__(self):

        
        objs = self.rosPublisher()
        dObjs = json.dumps(objs)
        
        
        pub = rospy.Publisher('/iFoil/OD', String, queue_size =100 )
        print('PUBLISHING: ', dObjs)
        rospy.Rate(1)
        for i in range(100000):
            pub.publish(dObjs)
        
        
    def rosPublisher(self):
        objects= [
          {'objectId':'chair0', 'category': 'chair', 'color':'brown'},
          {'objectId':'chair01', 'category': 'chair', 'color':'brown'},
          {'objectId':'chair012', 'category': 'chair', 'color':'white'},
          {'objectId':'desk0', 'category': 'desk', 'color':'brown'},
          {'objectId':'desk01', 'category': 'desk', 'color':'brown'},
          {'objectId':'desk012', 'category': 'desk', 'color':'white'},
          {'objectId':'apple0', 'category': 'apple', 'color':'red'},
          {'objectId':'apple01', 'category': 'apple', 'color':'red'},
          {'objectId':'apple012', 'category': 'apple', 'color':'green'}
          ]
          
        objects=[{'category': 'Scissors', 'bbox': [273.62433, 250.78824, 398.732, 350.74503], 'score': 0.9247937, 'objectId': 'scissors0', 'color': 'black'}, {'category': 'Coffee cup', 'bbox': [153.31221, 120.704124, 245.63333, 209.44968], 'score': 0.57411635, 'objectId': 'coffee_cup0', 'color': 'black'}, {'category': 'Ball', 'bbox': [463.28986, 222.22437, 535.7434, 289.5092], 'score': 0.5288452, 'objectId': 'ball0', 'color': 'yellow'}, {'category': 'Table', 'bbox': [0.0, 114.668304, 639.60004, 479.40002], 'score': 0.45140445, 'objectId': 'table0', 'color': 'white'}, {'category': 'Coffee cup', 'bbox': [338.91376, 123.67473, 423.06464, 205.39993], 'score': 0.43502855, 'objectId': 'coffee_cup01', 'color': 'white'}, {'category': 'Car', 'bbox': [157.50932, 245.36708, 257.24042, 297.8854], 'score': 0.4047104, 'objectId': 'car0', 'color': 'purple'}]

        #[{'category': 'Tennis ball', 'bbox': [1029.7325,  553.6085, 1149.2432,  670.7375], 'score': 0.6949193, 'objectId': 'tennis_ball0', 'color': 'white'}, {'category': 'Coffee cup', 'bbox': [ 41.45512, 496.6994 , 234.97769, 701.4539 ], 'score': 0.6036318, 'objectId': 'coffee_cup0', 'color': 'green'}, {'category': 'Coffee cup', 'bbox': [255.75804, 457.7683 , 431.4354 , 645.49164], 'score': 0.60025287, 'objectId': 'coffee_cup01', 'color': 'white'}, {'category': 'Scissors', 'bbox': [ 896.8979 ,  501.99384, 1051.7263 ,  703.37445], 'score': 0.5439723, 'objectId': 'scissors0', 'color': 'black'}, {'category': 'Microwave oven', 'bbox': [ 423.14392,    0.     , 1114.0295 ,  509.91296], 'score': 0.4714522, 'objectId': 'microwave_oven0', 'color': 'black'}]

          
        return objects


          
if __name__ == '__main__':
    
    
    rospy.init_node('objectSimulator')

    ObjectDetector()
