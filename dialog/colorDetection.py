
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


