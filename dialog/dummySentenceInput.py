import rospy
import json
from std_msgs.msg import String
import time

rospy.init_node('dummyInput')

pubS = rospy.Publisher('/naoqi_ASR/bestSpeechHypothesis', String, queue_size=10)

pubW = rospy.Publisher('/iFoil/probFoil/query', String, queue_size=10)


sentences = [
'the white mug on the table',
'i guess it is for mary',
'its label is kitchenware',
'the scissor on the desk',
'also it is for mary',
'name it kitchenware',
'the tennis ball on the table',
'the label is toy', 
"it belongs to toby",
'the car on the desk',
'it also belongs to toby',
'save the label is toy'
]

while True:
    text = input('please give your sentence: \n')
    if '?' in text:
        text = text[1:].lower()
        text = text.split()
        pubW.publish(json.dumps(text))
        
    elif text[0] == '.':
        i = int(text[1:])
        for sent in sentences:
            pubS.publish(sent)
            time.sleep(3)
    
    else:    
        pubS.publish(text.lower())
        
        
        

