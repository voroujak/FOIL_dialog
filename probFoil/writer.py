import numpy as np
import copy
'''
write the probFoil files given object and a fact to learn. learnFact is  a list of two, eg. ['ownership', 'farid']
'''
class foilWriter():
    def __init__(self, filesPath, objects, learnFact):
        self.dataFile = open(filesPath+ 'fo.data', 'w')
        self.settingFile = open(filesPath+'fo.setting', 'w')
        self.objects = objects
        self.learnFact = learnFact[0]
        self.learnFactValue = learnFact[1]
        self.allKeyValues = []
        self.attributeCollections = dict() # eg. ..., 'color': ['red', ...
        self.positiveLearnFactsRaw = [] #[['Farid', [('objectId', 'ojb1'), ('colo,,,
        self.negativeLearnFacts = []
        self.keyValues() # fill attribute collections and all key-values
        
        
        # write data and setting files
        for obj in self.objects:
            #write data file
            objFacts = self.dataWriter(obj)

            self.dataFile.write("\n".join(str(fact).lower() for fact in objFacts))
         
        #write negative examples from positive facts 
        self.negativeExamples()   
        
        #print(self.negativeLearnFacts)
        #write setting file
        self.settingWriter()
        ###self.settingFile.write("\n".join(str(fact).lower() for fact in objSettings))
        #print(self.positiveLearnFactsRaw)   
        #print('XXXXXXXXXXXXXXXXxx')
        #print(self.negativeLearnFacts) 
        #writing down positive learning facts
        #for posLearnFacts in self.positiveLearnFactsRaw:########################@TODO
        #    self.dataFile.write(posLearnFacts.lower())
        for fct in self.positiveLearnFactsRaw:
            self.dataFile.write('1.0::'+fct[0].lower() +'('+ str([el[1] for el in fct[1]]).replace('[', '').replace(']','').replace("'",'').replace('"', '').lower()+ ').\n')
                
        #writing down negative learning facts @TODO
        #for negLearnFacts in self.negativeLearnFacts:
        #    self.dataFile.write(negLearnFacts.lower())
        
        #print(self.negativeLearnFacts)
        
        for fct in self.negativeLearnFacts:
            #ind = [y[0] for y in fct[1]].index('objectId')
            #fct[1][ind] = ('objectId', 'generalobject')
            self.dataFile.write('0.0::'+fct[0].lower() +'('+ str([el[1] for el in fct[1]]).replace('[', '').replace(']','').replace("'",'').replace('"', '').lower()+ ').\n')
        self.dataFile.close()
        self.settingFile.close()
        
        #print(self.allKeyValues)

    #generate negative examples:
    def negativeExamples(self): 
    
        def insidePositiveFacts(positiveFacts, negativeFact):
            posFacts = [el[1] for el in positiveFacts]
            clearposFacts=[]
            
            for posFact in posFacts:
                clearposFact = []
                for el in posFact:
                    
                    if el[0] == 'objectId':
                        continue
                    else:
                        clearposFact.append(el)
                        
                clearposFacts.append(clearposFact)
            
            clearNegativeFact = []
            for fact in negativeFact[1]:
                if fact[0] =='objectId':
                    continue
                else:
                    clearNegativeFact.append(fact)

            if clearNegativeFact in clearposFacts:

                return True
            else:

                return False
            
       
        positiveFacts = copy.deepcopy(self.positiveLearnFactsRaw)
        
        for positiveFact in positiveFacts:
            posFact = positiveFact.copy()
            
            if posFact[0].lower() != self.learnFactValue:
                posFact[0] = self.learnFactValue
                self.negativeLearnFacts.append(posFact)
            '''
            #print('gggggggggggg', posFact) #['Farid', [('obje
            for fact in posFact[1]:
                if fact[0] == 'objectId':
                    continue
                possibleValues= self.attributeCollections[fact[0]] #[red, blue, green
                for newVal in possibleValues:
                    negativeFact = copy.deepcopy(posFact)
                    
                    negativeFact[1][negativeFact[1].index(fact)] = (fact[0], newVal)
                    

                    
                    if not insidePositiveFacts(self.positiveLearnFactsRaw,negativeFact):
                    
                        self.negativeLearnFacts.append(negativeFact)
                
                
             '''   
                
        
        
        
        
    #takes object description and return multiple facts for each object
    # it return a list of strings
    def dataWriter(self, obj):
        
        #values = list(obj.items())
        facts = []
        for key in obj.keys():
            if key == 'objectId':
                continue
            if key != self.learnFact:
                facts.append(self.predicateCreator(obj['objectId'], obj[key]))
            else:
                self.learnPredicateCreator(obj.copy(), obj['objectId'], obj[key])
        return facts

    # taking attribute eg. red and return red(objId, red)
    def predicateCreator(self, objId, attribute):
        return attribute + '('  +attribute + ') . \n'
    
    # it should return something like attribute(all values of obj dictionary).
    def learnPredicateCreator(self, values, objId, attribute):
        
        newValues = dict()
        for key in self.attributeCollections.keys():
            if key in values.keys():
                newValues[key] = values[key]
            else:
                newValues[key] = 'dc'
        
        values = newValues
        

        del values[self.learnFact]


        if 'objectId' in values.keys():
            del values['objectId']
        values = list(values.items())
        
        #generate positive examples:
        #self.positiveLearnFacts.append('1.0::'+attribute + '(' + str([el[1] for el in values]).replace('[', '').replace(']', '').replace("'",'') + ') .\n\n')
        self.positiveLearnFactsRaw.append([attribute, values])
        newValues = values.copy()
        '''
        #generate negative examples:
        values=[list(ele) for ele in values] 
        print(values)
        for keyyId in  range(len(values)):
            keyy = values[keyyId][0]
            val = values[keyyId][1]
            
            if val == 'dc':
                continue
            
            if keyy != 'objectId':
                possibleValues= self.attributeCollections[keyy].copy()
                possibleValues.remove(values[keyyId][1])
                
                for newAttribute in possibleValues:
                    newValues = values.copy()
                    changeAbleAttribute = [values[keyyId][0],values[keyyId][1]]
                    newValues[values.index([values[keyyId][0],values[keyyId][1]])] = [values[keyyId][0], newAttribute]
                    fct = '0.0::'+attribute + '(' + str([el[1] for el in newValues]).replace('[', '').replace(']', '').replace("'",'') + ') .\n\n'
                    if (not (fct in self.negativeLearnFacts)) and not(fct in self.positiveLearnFactsRaw): 
                        self.negativeLearnFacts.append(fct)
         '''   
        
        #return attribute + '(' + str(values).replace('[', '').replace(']', '').replace("'",'') + ') .\n\n'

        
    
    def settingWriter(self):
        lines = []
        keyValues = self.attributeCollections.copy()
        del keyValues['objectId']
        
        for keyy in keyValues.keys():
            if keyy != self.learnFact:
                for val in keyValues[keyy]:
                    lines.append('mode(' + val.lower()+'(+)).\n')
                    #lines.append('mode(' + val.lower()+'(-)).\n')
                    #lines.append('mode(' + val.lower()+'(-,+)).\n')
                    #lines.append('mode(' + val.lower()+'(-,-)).\n')
                    lines.append('base('+ val.lower() + '(' + keyy + ')).\n')
            else:
                for lrnFct in keyValues[self.learnFact]:
                    shortedKeyValues = keyValues.copy()
                    del shortedKeyValues[self.learnFact]
                    fct = 'base(' + lrnFct.lower() + '(' + str(list(shortedKeyValues.keys())).lower().replace('[', '').replace(']','').replace("'",'') + ')). \n\n'
                    lines.append(fct)
        #for learnAttribute in keyValues[self.learnFact]:
        lines.append('learn(' + self.learnFactValue.lower() + '/' + str(len(keyValues)-1) + '). \n')
        self.settingFile.writelines(lines)
    
    def keyValues(self):
        for obj in self.objects:
            for key in obj:
                if not ((key, obj[key]) in self.allKeyValues):
                    self.allKeyValues.append((key, obj[key]))
                if not(key in self.attributeCollections):
                    self.attributeCollections[key] = []
                if not(obj[key] in self.attributeCollections[key]):
                    self.attributeCollections[key].append(obj[key])
        
                    
'''        
        if not (value in self.modeValues): 
            self.modeValues.append(value)
            return ('mode(' + value + '(+,+)). \n'+
                'mode(' + value + '(-,+)). \n'+
                'mode(' + value + '(+,-)). \n'+
                'mode(' + value + '(-,-)). \n')
        else:
            return None
'''        
        
if __name__ == '__main__':
    #supposedly the objects will be in the shape:
    #{{objectId: 'obj1', color:'red', ownership:'Farid',utterances:[...]}}
    '''
    objects= [
            {'objectId': 'ojb1', 'color':'red','category':'apple', 'ownership':'Farid', 'size':'big', 'restriction':'doNotEat',},
            #{'objectId': 'obj2','color':'blue','category':'orange', 'ownership':'lili'},
            #{'objectId': 'obj3', 'color':'red','category':'apple', 'ownership':'Farid'},
            {'objectId': 'obj2', 'color':'yellow','category':'apple', 'ownership':'Farid', 'size':'big','restriction':'doNotEat'},
            {'objectId': 'obj3', 'color':'red','category':'orange', 'ownership':'Farid', 'size':'big', 'restriction':'doNotTouch'},
            {'objectId': 'obj4', 'color':'green','category':'orange', 'ownership':'lili', 'size':'small','restriction':'doNotEat'},
            {'objectId': 'obj5', 'color':'red','category':'apple', 'ownership':'lili', 'size':'big','restriction':'doNotTouch'},
            {'objectId': 'obj6','color':'yellow','category':'banana', 'ownership':'lili', 'size':'small', 'restriction':'doNotTouch'}
            ]
    '''
    
    
    objects= [
            {'objectId': 'ojb1', 'view':'top','app':'close', 'observability':'true'},
            {'objectId': 'ojb22', 'view':'top','app':'close', 'observability':'true'},
            {'objectId': 'ojb2', 'view':'front','app':'close', 'observability':'true'},
            #{'objectId': 'obj3', 'view':'top','app':'far', 'observability':'true'},
            {'objectId': 'obj3', 'view':'front','app':'close', 'observability':'false'},
            ]
    '''
    objects= [
            {'objectId': 'ojb1', 'view':'top', 'observability':'true'},
            {'objectId': 'ojb2', 'view':'front', 'observability':'true'},
            {'objectId': 'obj3', 'view':'top', 'observability':'true'},
            {'objectId': 'obj5', 'view':'front', 'observability':'false'},
            ]
            '''
    foilWriter(filesPath='', objects=objects, learnFact= ['observability','true'])
    
