# -*- coding: utf-8 -*-
import nltk
import spacy

nlp = spacy.load("en_core_web_sm")
import numpy as np
'''
It takes a sentence, and return keywords of the sentence that are useful for grounding the sentence to an object.
'''
class GroundingParser:
    def __init__(self, sentence):
        self.sentence = sentence
        self.spacySentence = nlp(self.sentence)
        tokenizer = nlp.Defaults.create_tokenizer(nlp)
        self.tokenizedSentence = nltk.word_tokenize(self.sentence)
        
        self.props, self.propsIndexes = self.relationalPreposition()
        
        self.keyWords, self.keyWordsIndexes = self.notStopWords()
        
        self.relativePairs = self.relativeObjects()
        
        self.mainObjectKeyWords = self.rootObjectDescription()
        
        
        
    def groundingFeatures(self):
        
        return {'relatives': self.relativePairs, 'mainAttributes':self.mainObjectKeyWords}
        
    def notStopWords(self):
        outList = []
        indexes = []
        for token in self.spacySentence:
            if not (token.is_stop):
                outList.append(token.text)
                indexes.append(self.tokenizedSentence.index(token.text))
        return outList, indexes
    
    """it return the index of the the word with ADP pos, which are useful for relative addressing. """
    def relationalPreposition(self):
        preps = []
        indexes = []
        for token in self.spacySentence:
            if 'prep' == token.dep_: # it might be also advmod
                preps.append(token.text)
        # take out all the index of the words that has ADP 
        for i in range(len(preps)):
            indexes.append(self.tokenizedSentence.index(preps[i]))
            
        return preps, indexes
    
    
    '''
    It return pairs of relative objects, eg. in the sentence: the book behind the desk, it returns [behind, desk].
    '''
    def relativeObjects(self):
        pairs = []
        suspicious = False
        
        for i in range(len(self.tokenizedSentence)):
            if i in self.propsIndexes:
                j = i
                suspicious = True
            if (i in self.keyWordsIndexes) and (suspicious) and i != j:
                '''IT SEEMS IF THERE IS 'TO' IN THE SENTENCE, THE WORD BEFORE IT IS IMPORTANT AS FOLLOWING! '''
                if 'RB' == self.spacySentence[j-1].tag_:
                    pairs.append([self.tokenizedSentence[j-1] , self.tokenizedSentence[i]])
                else:
                    pairs.append([self.tokenizedSentence[j], self.tokenizedSentence[i]])
                suspicious = False
        return pairs
        
    '''
    It return the keywords that has been used for describing an object, eg. in the sentence: the red book behind the desk, it returns [red, book].
    '''
    def rootObjectDescription(self):
        mainObjectKeyWords = []
        for token in self.keyWords:
            if not(token in [el[1] for el in self.relativePairs]) and not(token in [el[0] for el in self.relativePairs]) :
                mainObjectKeyWords.append(token)
                
        return mainObjectKeyWords
        
        
        
if __name__ == '__main__':
    loc = GroundingParser('the red book behind the table after clock')
    
    print(loc.groundingFeatures()) #{'relatives': [['behind', 'table'], ['after', 'clock']], 'mainAttributes': ['red', 'book']}
    