# -*- coding: utf-8 -*-

'''
class for a single object where all its attributes are saved.
By default, all attributes are initialized as None.
'''
class Item:
    def __init__(self, objectId=None, category= None, 
                 color=None, 
                 label=None, 
                 ownership=None, 
                 restriction=None, 
                 functionality=None, 
                 size=None, 
                 position=None, 
                 weight=None,
                 location = None,
                 bbox = None):
        self.objectId = objectId
        self.category = category
        self.color = color
        self.label = label
        self.ownership = ownership
        self.restriction = restriction
        self.functionality = functionality
        self.size = size
        self.position = position
        self.weight = weight
        self.location = location
        self.bbox = bbox

    '''
    return object attributes, only non None attributes
    '''
    def ItemAttributes(self):
        attributesFull = self.__dict__.copy()
        attributesCleaned = dict()
        for attKey in attributesFull.keys():
            if attributesFull[attKey] != None:
                attributesCleaned[attKey] = attributesFull[attKey]
        
        return attributesCleaned

'''
a class for handling all the objects
'''
class Items:
    def __init__(self):
        self.allItems = []
            
    '''
    Create an item and save them, This should be called with through Image processor,
    and language attributes are added later to each item.
    '''
    def CreateItem(self,objectId, category, color, bbox):
        self.allItems.append(Item(objectId=objectId, category=category, color = color, bbox=bbox))
        
    '''
    return all the items as list of dictionaries
    '''
    def HookAll(self):
        return [itm.ItemAttributes() for itm in self.allItems]
        
    '''
    Find all objects that are compatible with the input and return them.
    '''
    def Hook(self, objectId=None, category= None, 
                 color=None, 
                 label=None, 
                 ownership=None, 
                 restriction=None, 
                 functionality=None, 
                 size=None, 
                 position=None, 
                 weight=None,
                 location=None
                 ):
        
        
        hooker = dict(objectId=objectId, 
                     category= category, 
                     color=color, 
                     label=label, 
                     ownership=ownership, 
                     restriction=restriction, 
                     functionality=functionality, 
                     size=size, 
                     position=position, 
                     weight=weight,
                     location=location,
                     
                )
        
        matchedItems = []
        
        #clean input attributes from None
        attributesCleaned = dict()
        fullAttributes = hooker
        for attKey in fullAttributes.keys():
            if fullAttributes[attKey] != None:
                attributesCleaned[attKey] = fullAttributes[attKey]
            
        #iterate through all the saved Items and put the matching ones into a list for return.
        for itm in self.allItems:
            allMatch = True
            for attKey in attributesCleaned.keys():
                if not (attKey in itm.ItemAttributes().keys()):
                    allMatch = False
                    continue
                if attributesCleaned[attKey] != itm.ItemAttributes()[attKey]:
                    allMatch= False
            if allMatch:
                matchedItems.append(itm)
        return matchedItems
    
    '''
    It update attributes of objects. It takes two sets of arguments, on for finding objects to update, and new attributes to update.
    eg. UpdateAttributes(objectId='apple1', newobjectId='apple2').
    Note that if more than one object found, attribute of all of them will be updated.
    '''
    def UpdateAttributes(self, objectId=None, category= None, 
                 color=None, 
                 label=None, 
                 ownership=None, 
                 restriction=None, 
                 functionality=None, 
                 size=None, 
                 position=None, 
                 weight=None,
                 location=None,
                 bbox=None,
                 newobjectId=None, newcategory= None, 
                 newcolor=None, 
                 newlabel=None, 
                 newownership=None, 
                 newrestriction=None, 
                 newfunctionality=None, 
                 newsize=None, 
                 newposition=None, 
                 newweight=None,
                 newlocation=None,
                 newbbox=None):
        hookedItems = self.Hook(objectId=objectId, 
                     category= category, 
                     color=color, 
                     label=label, 
                     ownership=ownership, 
                     restriction=restriction, 
                     functionality=functionality, 
                     size=size, 
                     position=position, 
                     weight=weight,
                     location=location)
        for item in hookedItems:
            if newobjectId != None:
                item.objectId= newobjectId
            if newcolor != None:
                item.color = newcolor
            if newlabel != None:
                item.label = newlabel
            if newownership != None:
                item.ownership = newownership
            if newrestriction != None:
                item.restriction = newrestriction
            if newfunctionality != None:
                item.functionality = newfunctionality
            if newsize != None:
                item.size = newsize
            if newposition != None:
                item.position = newposition
            if newweight != None:
                item.weight = newweight
            if newlocation != None:
                item.location = newlocation
        


if __name__ == '__main__':
    
    itms = Items()
    itms.CreateItem(objectId= 'apple1', category = 'apple', color= 'red')
    itms.CreateItem(objectId= 'apple2', category = 'orange', color= 'blue')
    itms.CreateItem(objectId= 'apple3', category = 'apple', color= 'green')
    itms.CreateItem(objectId= 'apple4', category = 'banana', color= 'yellow')
    itms.UpdateAttributes(objectId='apple1', newrestriction='doNotTouch', newlocation= 'behindTheDesk')
    itms.UpdateAttributes(objectId= 'apple2', newfunctionality = 'spoiled')
    itms.UpdateAttributes(objectId= 'apple3', newfunctionality = 'spoiled')

    for itm in itms.Hook(objectId= 'apple1', location='behindTheDesk'):
        print(itm.ItemAttributes())
    
    print(itms.HookAll())
