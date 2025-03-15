# -*- coding: utf-8 -*-

from items import Items
from groundingParser import GroundingParser as GP
from std_msgs.msg import String
import rospy
import json
from PIL import Image, ImageDraw
import numpy as np

import matplotlib.pyplot as plt
import sys
sys.path.append('..')
from retinaNet.keras_retinanet.utils.colors import label_color
from retinaNet.keras_retinanet.utils.visualization import draw_box, draw_caption

import os

class Grounder:
    def __init__(self, items):
        
        global tmpODOld
        tmpODOld = ':('
        
        global tmpSpeechOld
        tmpSpeechOld= ':)'
        
        self.detectedObjects = None
        self.speechHypothesis = None
        
        
        self.items = items
        
        rospy.init_node('grounder')
        
        rospy.Subscriber('/iFoil/OD', String, self.objectCatcher)
        
        rospy.Subscriber("/naoqi_ASR/bestSpeechHypothesis", String, self.sentenceCatcher)
        
        self.hookPub=rospy.Publisher('/iFoil/allObjects', String, queue_size=10)
        
        #Handling lexical similarity
        self.lexSimPub = rospy.Publisher('/iFoil/dialog/similarityMeasurmentIn', String, queue_size =10)
        rospy.Subscriber('/iFoil/dialog/similarityMeasurmentOut',String, self.lexSimHandler)
        self.lexSim=None
        self.oldLexSim = None
        
        #A dummy Image
        self.img = None
        
        #and we want also update some attribute that comes from dialog to the most probable object
        rospy.Subscriber('iFoil/dialog/updateableAttribute', String, self.updateAttributeHandler)
        self.updateableAttribute = None
        
        
        #capture the sentence Intent
        rospy.Subscriber('iFoil/dialog/sentenceIntent', String, self.sentenceIntentHandler)
        self.sentenceIntent= None
        
        print('Grounder is Active.')
        rospy.spin()
        
        
    '''For handling intent of sentence catched from dialog'''
    def sentenceIntentHandler(self, data):
        dat = data.data
        self.sentenceIntent = dat
        
    '''For handling attributes of object that has to be updated, catched from dialog '''
    def updateAttributeHandler(self, data):
        dat = data.data
        if dat != None and dat != 'null':
            self.updateableAttribute = eval(dat)
        else:
            self.updateableAttribute = None
        
        
    '''For handling results coming for finding the lexical similarity from dialog engine. '''
    def lexSimHandler(self, data):
        self.lexSim = float(data.data)
        
        
    '''
    It capture the detected objects came from objectDetector.
    '''
    def objectCatcher(self, data):
        tmp= data.data
        global tmpODOld
        if tmpODOld != tmp:
            tmpODOld = tmp
            self.detectedObjects = eval(tmp)
            
            #create new items for each detected object
            self.itemCreator()
        
    '''
    It capture the speech hypothesis came from ASR.
    '''
    def sentenceCatcher(self, data):
        tmp = data.data
        global tmpSpeechOld
        if tmpSpeechOld != tmp:
            print('Sentence Catched in grounder.')
            tmpSpeechOld = tmp
            self.speechHypothesis = tmp
            gp = GP(self.speechHypothesis)
            sentenceFeatures = gp.groundingFeatures()
            self.runGrounding(sentenceFeatures)
            
            
    def itemCreator(self):
        for obj in self.detectedObjects:
            print('item of {} has been created.'.format(obj['objectId']))
            if ' ' in obj['category']:
                obj['category'] = obj['category'].split(' ')[1]
            self.items.CreateItem(objectId = obj['objectId'].lower(), 
                                  category = obj['category'].lower(),
                                  color = obj['color'],
                                  bbox = obj['bbox'])
    
    def lexicalDistance(self, word1, word2):
        self.oldLexSim = self.lexSim
        self.lexSimPub.publish(json.dumps([word1,word2]))
        rospy.wait_for_message('/iFoil/dialog/similarityMeasurmentOut', String)
        
        self.oldLexSim = self.lexSim
        return self.lexSim
            
            
    def runGrounding(self, sentenceFeatures):
        allObjects= self.items.HookAll()
        distance = [0]*len(allObjects)
        bestObj = None
        for i in range(len(allObjects)): # for each object
            numberOfMatchedAttributes = 0
            for jKey in ['label','category', 'color', 'size', 'weight']: #for each main key of each object
                if jKey in allObjects[i].keys():
                    if allObjects[i][jKey] != None:
                        for kWord in sentenceFeatures['mainAttributes']:# for each word in the main object attributes from sentence grounding parser
                            numberOfMatchedAttributes += 1
                            dist = self.lexicalDistance(kWord, allObjects[i][jKey])
                            distance[i] += dist
            distance[i] /= (numberOfMatchedAttributes+1)
                        
        image = np.asarray(Image.open('../images/n17.png')) # TODO remove this, and send the file address on ros topic
        # now finding the object that has the minimum distance to the features
        minDistance = len(sentenceFeatures)+5
        for i in range(len(distance)):
            if distance[i] < minDistance:
                bestObj = allObjects[i]
                minDistance = distance[i]
        print('Found the most probable object as: ', end=' ')
        if self.sentenceIntent =='BeingLocated' or self.sentenceIntent==None and not ('next' in self.speechHypothesis):
            self.bestObject = bestObj
            
            self.objectVisualizer(image, self.bestObject['bbox'], self.bestObject['category'], self.bestObject['color'])
        
        # crawling between objects or updating an attribute
        if ('continue' in self.speechHypothesis) or ('other' in self.speechHypothesis):
            print('XXXXXXXXXXXXXXXXxx')
            print(allObjects)
            print('YYYYYYYYYYYYYyy')
            print(self.bestObject)
            if allObjects.index(self.bestObject) != len(allObjects)-1:
                self.bestObject = allObjects[allObjects.index(self.bestObject)+1]
            else:
                self.bestObject = allObjects[0]
            self.objectVisualizer(image, self.bestObject['bbox'], self.bestObject['category'], self.bestObject['color'])
        else:
            if self.updateableAttribute != None:
                self.updateAttribute()
            else:
                print('nothing found for assignment to the object')
            
        

        #print(distance)
        
        
        
    def objectVisualizer(self, img_orig, box, label, color):
        os.system('pkill eog')

        self.img = Image.fromarray(img_orig)
        #self.img.close()
        draw= ImageDraw.Draw(self.img)
        draw.rectangle(box,outline=(100,100,100))
        draw.text([box[0]+10, box[1]+10], text= label)
        draw.text([box[0]+10, box[1]+20], text = color)
        self.img.show()
        '''
        color = label_color(0)
        b = np.asarray(box, dtype=np.int)
        draw_box(img_orig, b, color=color)
        caption = str(label) + '_' + str(color)
        draw_caption(img_orig, b, caption)
        plt.figure(figsize=(15, 15))
        plt.axis('off')
        plt.imshow(img_orig)
        plt.show()
        plt.close()
        '''
        
        
    def updateAttribute(self):
        if self.updateableAttribute != None and self.bestObject != None:
            updatingattributes = dict()
            for key in self.updateableAttribute.keys():
                updatingattributes['new'+key]=self.updateableAttribute[key]
            
            print('XXXXXXx')
            print(self.bestObject)
            print(self.updateableAttribute)
            print('uuuuuuuuuuuuuuuuu')
            print(updatingattributes)
            #craeting a dictionary with all old and new attributes
            updatingattributes.update(self.bestObject)
            self.items.UpdateAttributes(**updatingattributes)
            self.bestObject= self.items.Hook(objectId= self.bestObject['objectId'])[0].ItemAttributes()
            self.updateableAttribute =None
            
        self.hookPub.publish(json.dumps(self.items.HookAll()))

                        
if __name__ == '__main__':
    grounder = Grounder(Items())
