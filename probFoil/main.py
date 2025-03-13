import os
import rospy
from std_msgs.msg import String
from writer import foilWriter
import json
class iFoil:
    def __init__(self):

        self.theories = []
        
        #initializing ros node
        #rospy.init_node('node_name')
        self.objects =None
        
        print('probFoil is listening to the facts.')
        
        rospy.Subscriber('/iFoil/probFoil/query', String, self.inductor)
        
        rospy.Subscriber('/iFoil/allObjects', String, self.allObjectHandler)
        

        
        rospy.spin()
        
        
    """Save all the objects in the class. """
    def allObjectHandler(self, data):
        objects = data.data
        objects = eval(objects)
        
        #removing values that are not neccesary, eg. bbox attribute
        for obj in objects:
            if 'bbox' in obj.keys():
                del obj['bbox']
        
        self.objects = objects
        
    """Listen for new learn Fact, if one arrived, run the system and take out the theories. """
    def inductor(self, data):
        learnFacts = data.data
        print('Writing and inducing')
        #print(learnFacts)
        learnFacts = eval(learnFacts)
        
        

        
        self.write(self.objects, learnFacts) #write the data and setting files
        self.run() #run probFoil
        self.parser() # read the output of probFoil
        
        
    def write(self, objects, learnFacts):
        #print(objects)
        foilWriter(filesPath='', objects=objects, learnFact= learnFacts) 
        '''learnFacts = ['ownership', 'farid'] '''
        
        
        
    def run(self):
        os.remove('out.txt')
        os.system('probfoil fo.data fo.setting >> out.txt')
        
    def parser(self):
        f= open('out.txt', 'r')
        lines = f.readlines()
        for row in range(len(lines)):
             if 'FINAL THEORY' in lines[row]:
                 startRowOfTheories = row
             if 'SCORES' in lines[row]:
                 endRowOfTheories = row
        self.theories = lines[startRowOfTheories +1: endRowOfTheories]
        self.theories = [theory.replace('\n', '') for theory in self.theories]
        print(self.theories)
        print('XXXXXXXXXx')
        

if __name__ == '__main__':
    
    rospy.init_node('ProbFoil')
    
    iFoil()
    
    '''
    
    ##### the exmaple code for publishing to this code.
    
    import json
    import rospy
    from std_msgs.msg import String
    rospy.init_node('sender')
    pub = rospy.Publisher('iFoil/probFoil/writer', String, queue_size=10)
    objects= [
            {'objectId': 'ojb1', 'color':'red','category':'apple', 'ownership':'Farid','restriction':'doNotEat'},
            {'objectId': 'obj2','color':'blue','category':'orange', 'ownership':'lili'},
            {'objectId': 'obj3', 'color':'red','category':'apple', 'ownership':'Farid'},
            {'objectId': 'obj4', 'color':'yellow','category':'banana', 'ownership':'Farid','restriction':'doNotEat'},
            {'objectId': 'obj5', 'color':'yellow','category':'apple', 'ownership':'Farid','restriction':'doNotEat'},
            {'objectId': 'obj7','color':'red','category':'apple', 'ownership':'lili', 'restriction':'doNotEat'}
            ]
    objects = json.dumps(objects)
    pub.publish(objects)
    '''
    
