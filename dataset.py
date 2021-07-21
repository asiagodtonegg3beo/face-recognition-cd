

# -*- coding: utf-8 -*-


"""
/* -----------------------------------------------------------------------------
  Daniel Lu
  Email : dan59314@gmail.com
  Web :     http://www.rasvector.url.tw/
  YouTube : http://www.youtube.com/dan59314/playlist
  GitHub : 
*/

"""

#%%
# Standard library----------------------------------------------
import os
from cv2 import cv2 
# Third-party libraries------------------------------------------
import numpy as np
from PyQt5.QtCore import QCoreApplication
#%%%  Function Section
fp = open("present.txt", "r")
text=[]
text = fp.readlines()
fp.close()
name = text[0]
font = cv2.FONT_HERSHEY_SIMPLEX
DfntSize = 1
fntThickness = 1

DoContrast = False
threshold = 150
dVal = 50



def Draw_Text(img, sTxt, aX=30, aY=30):
    if ""==sTxt: return
    cv2.putText(image, str(sTxt) ,(aX,aY), font, 
       cv2.FONT_HERSHEY_PLAIN,(0,255,255), fntThickness,cv2.LINE_AA)
    

def ForceDir(path):
    if not os.path.isdir(path):
        os.mkdir(path) 
                

        
outputPath = 'dataset\\'
outputFn = name
print("[INFO] Get the name "+ name +" from present.txt")
incId=0

#name = input("[INFO] Enter your name (Now={}): ".format(outputFn) )

if ""!=name: outputFn = name

outputPath = "{}{}/".format( outputPath,outputFn)
ForceDir(outputPath)
        

camera = cv2.VideoCapture(0)
while True:
    return_value,image = camera.read()  
    imgInfo = np.asarray(image).shape     
    if len(imgInfo)<2: break
    imgH=imgInfo[0]
    imgW=imgInfo[1]
    imgChannel=imgInfo[2] 
    
    if DoContrast:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image[:,:] = [[ min(pixel + dVal, 255) 
            for pixel in row] for row in image[:,:]]
    #cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    
    try:                 
                    
        key = cv2.waitKey(5) & 0xFF
        if key == 27:  #esc   ord('s'):
            #cv2.imwrite('test.jpg',image)
            break
        elif key == ord('s'):
            incId+=1
            cv2.imwrite("{}{}_{}.jpg".format(outputPath, outputFn, incId), image)
            
        Draw_Text(image, "esc:exit, s:save image")
        cv2.putText(image, "saved in : \{} ".format(outputPath), (0, 473), cv2.FONT_HERSHEY_DUPLEX,
            0.7, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image,"photos:"+str(incId), (500, 473),cv2.FONT_HERSHEY_PLAIN,
            1.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow('image',image)
        #plt.imshow( cv2.cvtColor(image,cv2.COLOR_BGR2RGB) )
            
            
    except ValueError:
        break

camera.release()
cv2.destroyAllWindows()
        
print("[INFO] {} images saved in : \"{}\"!".format(incId, outputPath))

        

    