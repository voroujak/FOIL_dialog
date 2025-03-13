"""
@author: voroujak
"""
"""
This script should be called with dialog.py
"""
import dialogUtils
import rospy
from std_msgs.msg import String

class SeMaCDialog:
    def __init__(self):
        #self.pub= rospy.Publisher('/iFoil/dialog/similarityMeasurementOut', String, queue_size=10)
        self.sentenceIntent =None
        print("SEMAC INITIALIZED")
    def reply(self,sentence):
        #dialogUtils.reinitModel()
        
        # predict FEs and FTs by NN, and filter them based on prbabilities.
        FEs, FTs = dialogUtils.prediction(sentence)
        
        #given FEs and FTs of each sentence, find intent of sentence, entities and properties that are assigned to entities(assignment), and finding if the sentence has positive polarity or negative (if there is any NOT or not), which might change the meaning.
        sentenceIntent, entity, assignment, polarity = dialogUtils.predictionAnalyser(FEs, FTs, sentence)
        self.sentenceIntent = sentenceIntent
        # clustering assignet properties to predefined clusters.
        assignmentMeaning = dialogUtils.LUSynthesizer(assignment, sentenceIntent)
        
        print('polarity ', polarity)
        print('assignment ', assignment)
        print('assignmentMeaning ', assignmentMeaning)
        print('sentenceIntent ', sentenceIntent)
        print('entity ', entity)
        print('FE ', FEs)
        print('FT ', FTs)
                
        # generate sentence
        generatedSentence = dialogUtils.sentenceGenerator(FEs, FTs, sentenceIntent, entity, assignmentMeaning, polarity)
        
        updateableAttribute = dialogUtils.AttributeCatcher(FEs, FTs, sentenceIntent, entity, assignmentMeaning, polarity, sentence)
        
        print('XXXXXXXXXx')
        print(updateableAttribute)
        
        return generatedSentence, updateableAttribute
    
    
    def similarityMeter(self, word1, word2):
               
        return dialogUtils.distanceFinder(word1, word2)
        
     
    # re-initializing model. Flashing memory and load the model, and make the model as default graph.   
    def reinitModel(self):
        dialogUtils.reinitModel()
        #print(generatedSentence)
        

