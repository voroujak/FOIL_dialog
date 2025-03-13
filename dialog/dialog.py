# -*- coding: utf-8 -*-


import rospy
from std_msgs.msg import String

from SeMaCDialog import *
from AIMLEngine import *

import json

class Dialog:
    def __init__(self):
        rospy.init_node('dialogManager')
        self.speechHypothesis = None
        # the transcript that has been detected by ASR
        self.speechHypothesis = None
        
        # create two answer engine
        self.AIMLEng = AIMLEngine()
        self.SeMaCEng = SeMaCDialog()
        
        # publish answers and let the robot TTS it
        self.robotReplyTopic = rospy.Publisher("/naoqi_TTS/replyBack", String, queue_size = 10)
        
        # listen to the best transcript came from ASR
        rospy.Subscriber("/naoqi_ASR/bestSpeechHypothesis", String, self.getASR)
        
        
        #publish updateable Attribute cathed from dialog
        self.upAtt = rospy.Publisher('/iFoil/dialog/updateableAttribute', String, queue_size = 10)
        
        
        # listen if any needs the similarity between two words.
        rospy.Subscriber('/iFoil/dialog/similarityMeasurmentIn', String, self.lexSim)
        self.lexSimPub = rospy.Publisher('/iFoil/dialog/similarityMeasurmentOut', String, queue_size=10)
        
        #send what is the intent of the sentence
        self.sentenceIntentPublisher = rospy.Publisher('/iFoil/dialog/sentenceIntent', String, queue_size=10)
        
        rospy.spin()
        
        
        
    def lexSim(self, data):
        dat = data.data
        listOfString=eval(dat)
        [word1, word2] = listOfString
        self.lexSimPub.publish(str(self.SeMaCEng.similarityMeter(word1,word2)))
        
    def preprocessSentence(self, sentence):
        sentence = sentence.lower()
        sentence = sentence.replace("cannot", "can not")
        sentence = sentence.replace("'re", " are")
        sentence = sentence.replace("'d", " would")
        sentence = sentence.replace("n't", " not")
        sentence = sentence.replace("'", " ")
        sentence = sentence.replace('.', '')
        sentence = sentence.replace('!', '')
        sentence = sentence.replace('?', '')
        sentence = sentence.replace(',','')
        return sentence 
        
    
    
    def getASR(self, data):
        self.speechHypothesis = data.data
        
        self.speechHypothesis = self.preprocessSentence(self.speechHypothesis)
        reply = None

        print ("HUMAN: " + str(self.speechHypothesis))
        
        reply, updateableAttribute = self.SeMaCEng.reply(self.speechHypothesis)
        
        #send the intent of the sentence abroad
        self.sentenceIntentPublisher.publish(self.SeMaCEng.sentenceIntent)
        
        if reply == None:
            reply = self.AIMLEng.AIMLAnswer(self.speechHypothesis)
            
        print ("ROBOT : " +  reply)

        self.robotReplyTopic.publish(reply)

        self.upAtt.publish(json.dumps(updateableAttribute))


if __name__ == '__main__':
    dialog = Dialog()