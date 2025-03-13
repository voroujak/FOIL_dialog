# -*- coding: utf-8 -*-

from retinaNet.keras_retinanet import models
from retinaNet.keras_retinanet.utils.image import preprocess_image, resize_image
from retinaNet.keras_retinanet.utils.colors import label_color
from retinaNet.keras_retinanet.utils.visualization import draw_box, draw_caption

import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from colorDetection import *

import copy

class objectDetector():
    def __init__(self):
        #self.CVmodel_path = '/home/voroujak/datasets/models/resnet101_oid_v1.0.0.h5'
        self.CVmodel_path = '/home/voroujak/Downloads/retinanet_resnet152_500_classes_0.4991_converted.h5'
        self.ST = 15 # similarity threshold, two objects with bounding boxes closer than this will be disregarded
        self.N = 5 # number of best detected object
        self.MT = 0.4 # minimum threshold where detections belows this will be disregarded
        self.model = models.load_model(self.CVmodel_path, backbone_name='resnet152')
        self.lfp = open('visionObjectLabels.json', 'r')
        self.labelKeys = json.load(self.lfp)
        self.CD = colorDetection() 
        
        #self.visualizer(ccboxes, ccscores, cclabels)
        
        
    def imgParser(self, image):
        objectIds = []
        self.draw = image.copy()
        b, s, l = self.predictOnImg(image)
        ccboxes, ccscores, cclabels = self.objectUniter(b,s,l)
        for i in range(len(cclabels)):
            cclabels[i] = self.labelKeys[str(cclabels[i])]
        print('DETECTED OBJECTS ARE: ', cclabels)
        
        #assigning a unique object Id to each observed object.
        for i in range(len(cclabels)):
            lbl = cclabels[i].lower().replace(' ', '_')
            labelAppended = False
            j=0
            while not labelAppended:
                lbl = lbl + str(j)
                j +=1
                if not (lbl in objectIds):
                    objectIds.append(lbl)
                    labelAppended = True
                    
                    
        #finding the color of object
        colors=[]
        for i in range(len(ccboxes)):
            croppedImage = image[int(ccboxes[i][1]):int(ccboxes[i][3]),int(ccboxes[i][0]):int(ccboxes[i][2]),:]
            color = self.CD.findColor(croppedImage)
            colors.append(color)
        
        
        return ccboxes, ccscores, cclabels, objectIds, colors
        
        


    
    def predictOnImg(self, img):
        img = preprocess_image(img)
        img, scale = resize_image(img)
        boxes, scores, labels = self.model.predict_on_batch(np.expand_dims(img, axis=0))
        boxes /= scale
        return boxes[0], scores[0], labels[0]
    
    def objectUniter(self, boxes, scores, labels):
        #Boxes: A list of 4 elements (x1, y1, x2, y2)
        cboxes = []
        cscores = []
        clabels = []
        ccboxes = []
        ccscores = []
        cclabels = []
        for box, score, label in zip(boxes, scores, labels):
            if score < self.MT:
                break
            cboxes.append(box)
            cscores.append(score)
            clabels.append(label)
        tbRemoved = []
        
        for i in range(len(cboxes)):
            for j in range(len(cboxes)):
                if i ==j: 
                    continue
                #unit two the same object
                if True:#clabels[i] == clabels[j]:
                    diffBoxes = np.abs(cboxes[i]-cboxes[j])

                    if (diffBoxes[0] < self.ST) and (diffBoxes[1] < self.ST) and (diffBoxes[2] < self.ST) and (diffBoxes[3] < self.ST) :
                        if cscores[i] > cscores[j]: 
                            tbRemoved.append(j)
                        if cscores[j] > cscores[i]: 
                            tbRemoved.append(i)
        
        print('CCCCCCCCCCCCCCCCCCCCCCCCCc')                    
        print(tbRemoved)
        for i in range(len(cboxes)):
            if not(i in tbRemoved):            
                ccboxes.append(cboxes[i])
                cclabels.append(clabels[i])
                ccscores.append(cscores[i])
        return ccboxes, ccscores, cclabels
        
        
        
        
    def visualizer(self, ccboxes, ccscores, cclabels, colors):
        #for visualizing all objects on one image
        for box, score, label in zip(ccboxes, ccscores, cclabels):
            color = label_color(1)
            b = box.astype(int)
            draw_box(self.draw, b, color=color)
            print('predicted: ', label, ' with score of: ', score)
            caption = "{} {:.3f}".format(label, score)
            draw_caption(self.draw, b, caption)
            
            
        plt.figure(figsize=(15, 15))
        plt.axis('off')
        plt.imshow(self.draw)
        plt.show()
        
        
        #visualizing each segment individually
        for box, score, label in zip(ccboxes, ccscores, cclabels):
            print('Label is: ', label)
            b = box.astype(int)
            tmp = self.draw[b[1]:b[3], b[0]:b[2]]
            plt.imshow(tmp)
            plt.show()
            

    def objectVisualizer(self, img_orig, box, label):
        
        color = label_color(0)
        b = box.astype(int)
        draw_box(img_orig, b, color=color)
        caption = label
        draw_caption(img_orig, b, caption)
        plt.figure(figsize=(15, 15))
        plt.axis('off')
        plt.imshow(img_orig)
        plt.show()
    
    
if __name__ == '__main__':
    m = objectDetector()
    
    image = np.asarray(Image.open('images/n17.png'))

    bboxes,scores,labels, objectIds, colors = m.imgParser(image)
    
    m.visualizer(bboxes, scores,labels, colors)
    #for i in range(len(bboxes)):
    #    print(labels[i])
    #    print(colors[i])
    #    m.objectVisualizer(copy.deepcopy(image), bboxes[i],labels[i])
    
    objects = []
    
    for i in range(len(bboxes)):
        objects.append({'category':labels[i],
                        'bbox': list(bboxes[i]),
                        'score': scores[i],
                        'objectId': objectIds[i],
                        'color':colors[i]})
    print(objects)
    
    
    
    '''
    import scipy.misc
    
    print(len(bboxes))
    print(len(scores))
    print(len(labels))
    print(len(objectIds))
    
    for i in range(len(bboxes)):
        croppedImage = image[int(bboxes[i][1]):int(bboxes[i][3]),int(bboxes[i][0]):int(bboxes[i][2]),:]
        scipy.misc.imsave('croppedImages/'+objectIds[i] + '.jpg', croppedImage)

    '''
