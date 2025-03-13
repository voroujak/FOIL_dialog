
from PIL import Image

import numpy as np

import matplotlib.pyplot as plt

from skimage.color import rgb2hsv

from scipy.spatial.distance import cosine



class colorDetection:
    def __init__(self):
        pass
        #self.findColor(img)


    def hsvDistance(self,c1,c2):
        (h0,s0,v0) = c1
        (h1,s1,v1) = c2
        dh = min(abs(h1-h0), 360-abs(h1-h0)) / 180
        ds = abs(s1-s0)
        dv = abs(v1-v0)/255
        return np.sqrt(dh*dh+ds*ds+dv*dv)

    def findColor(self,img):
        '''
        hist, binEdges = np.histogram(np.asarray(img[:,:,0]), bins=range(360))

        plt.plot(hist)
        plt.show()
        
        #finding best hue
        maxSum = 0
        bestH = None
        for i in range(0,360,10):
            sumHist = np.sum(hist[i:i+60])
            if sumHist > maxSum:
                maxSum = sumHist
                bestH = i+30
                
        
        #finding best Saturation
        hist, binEdges = np.histogram(np.asarray(img[:,:,1]), bins=range(100))
        plt.plot(hist)
        plt.show()
        
        maxSum = 0
        bestS = None
        for i in range(0,100,10):
            sumHist = np.sum(hist[i:i+60])
            if sumHist > maxSum:
                maxSum = sumHist
                bestS = i+30
            
        bestColor = None
        
        
        #finding best value
        hist, binEdges = np.histogram(np.asarray(img[:,:,2]), bins=range(255))
        plt.plot(hist)
        plt.show()
        
        maxSum = 0
        bestV = None
        for i in range(0,360,10):
            sumHist = np.sum(hist[i:i+60])
            if sumHist > maxSum:
                maxSum = sumHist
                bestV = i+30
            
        bestColor = None
        
        # if it is red, black or white
        if bestH < 30 or bestH > 330:
            # it is red
            if bestS > 20:
                bestColor = 'red'
            else:
                if bestV >125:
                    bestColor = 'white'
                else:
                    bestColor = 'black'
                    
        #yellow
        if bestH <90 and bestH >=30:
            bestColor = 'yellow'
            
        if bestH>=90 and bestH < 150:
            bestColor = 'green'
            
        if bestH>=150 and bestH < 210:
            bestColor = 'cyan'
            
        if bestH>=210 and bestH <270:
            bestColor = 'blue'
            
        if bestH>=270 and bestH <330:
            bestColor = 'magneta'
        
        
        '''
        #img=green
        h,w,c = img.shape
        img = img[int(0.4*h): int(0.6*h), int(0.4*w):int(0.6*w),:] 
        
        img = img.copy()
        img[:,:,0] = img[:,:,0]- 0.3*img[:,:,0]
        img[:,:,1] = img[:,:,1]#+10#0.1*img[:,:,1]
        img[:,:,2] = img[:,:,2]#+20#*img[:,:,2]
        img = rgb2hsv(img)#+0.00000001
        
        #standardizing hsv values
        img[:,:,0] = img[:,:,0]*360
        img[:,:,1] = img[:,:,1]*100
        img[:,:,2] = img[:,:,2]*255
        
        #enhance Image by calibration
        h = np.mean(img[:,:,0]) 
        s = np.mean(img[:,:,1]) 
        v = np.mean(img[:,:,2]) 
        
        colors = {'black':(0,0,0), 
                      'white':(0,0,255), 
                      'red':(0,100,255), 
                      #'lime':(120,100,255), 
                      'blue':(240, 100, 255), 
                      'yellow':(60,100,255), 
                      #'cyan':(180, 100,255), 
                      #'magneta':(300, 100,255), 
                      #'gray':(0,0,125), 
                      #'maroon':(0,100,125), 
                      #'olive':(60,100,125), 
                      'green':(120, 100, 125), 
                      'purple':(300, 100,125), 
                      #'teal':(180,100,125), 
                      #'navy':(240,100,125)
                      }
        
        
        tmpMin = 5000
        
        for colorKey in colors.keys():
            hsvColor = colors[colorKey]
            cosDistance = self.hsvDistance((h,s,v), hsvColor)
        

            if  cosDistance < tmpMin:
                tmpMin = cosDistance
                bestColor = colorKey
                
         
       
        return bestColor


if __name__ =='__main__':
    img = np.asarray(Image.open('croppedImages/box01.jpg'))
    cd = colorDetection()
    print(cd.findColor(img))

'''


on = [256]*50
zer = [0]*50

red = np.zeros(shape=(50,50,3))
red[:,:,0]=  np.ones((50,50))*255

green = np.zeros(shape=(50,50,3))
green[:,:,1]=  np.ones((50,50))*255

blue = np.zeros(shape=(50,50,3))
blue[:,:,2]=  np.ones((50,50))*255

white = np.ones((50,50,3))*255
black = np.zeros((50,50,3))*255


hist, binEdges = np.histogram(np.asarray(img[:,:,0]), bins=range(360))

plt.plot(hist)
plt.show()

#finding best hue
maxSum = 0
bestH = None
for i in range(0,360,10):
    sumHist = np.sum(hist[i:i+60])
    if sumHist > maxSum:
        maxSum = sumHist
        bestH = i+30
        

#finding best Saturation
hist, binEdges = np.histogram(np.asarray(img[:,:,1]), bins=range(100))
plt.plot(hist)
plt.show()

maxSum = 0
bestS = None
for i in range(0,100,10):
    sumHist = np.sum(hist[i:i+60])
    if sumHist > maxSum:
        maxSum = sumHist
        bestS = i+30
    
bestColor = None


#finding best value
hist, binEdges = np.histogram(np.asarray(img[:,:,2]), bins=range(255))
plt.plot(hist)
plt.show()

maxSum = 0
bestV = None
for i in range(0,360,10):
    sumHist = np.sum(hist[i:i+60])
    if sumHist > maxSum:
        maxSum = sumHist
        bestV = i+30
    
bestColor = None

# if it is red, black or white
if bestH < 30 or bestH > 330:
    # it is red
    if bestS > 20:
        bestColor = 'red'
    else:
        if bestV >125:
            bestColor = 'white'
        else:
            bestColor = 'black'
            
#yellow
if bestH <90 and bestH >=30:
    bestColor = 'yellow'
    
if bestH>=90 and bestH < 150:
    bestColor = 'green'
    
if bestH>=150 and bestH < 210:
    bestColor = 'cyan'
    
if bestH>=210 and bestH <270:
    bestColor = 'blue'
    
if bestH>=270 and bestH <330:
    bestColor = 'magneta'
    
print(bestColor)
            
''' 

