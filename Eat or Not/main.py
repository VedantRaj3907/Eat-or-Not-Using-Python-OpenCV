#Importing
import cv2 as cv
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone as cz
import os
import random
import time

######################################################################################
#Setting Window
cap = cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = FaceMeshDetector(maxFaces = 1)   #For Detecting Faces (maxFaces = 1)

idlist = [0, 17, 78,292]        #For the positions of the 4 lips points

######################################################################################
#Images
folderEatables = 'E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Eat or Not/Images_Project/eatable'
listEatable = os.listdir(folderEatables)
eatabels = []
for objects in listEatable:
    eatabels.append(cv.imread(f'{folderEatables}/{objects}', cv.IMREAD_UNCHANGED))

folderNonEatables = 'E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Eat or Not/Images_Project/noneatable'
listNonEatable = os.listdir(folderNonEatables)
noneatabels = []
for objects in listNonEatable:
    noneatabels.append(cv.imread(f'{folderNonEatables}/{objects}', cv.IMREAD_UNCHANGED))

######################################################################################
#Variables
CurrentObject = eatabels[random.randint(0,3)]
Position = [300,0]
Speed = 5
Points = 0
global isEatable
isEatable = True
GameOver = False
StartTime = time.time()
TotalTime = 50

######################################################################################
#New Object at New Positon
def ResetObject():
    Position[0] = random.randint(100, 1180)                     #at Random X position
    Position[1] = 0

    EorNE = random.randint(0, 1)                           # If O then select image from noneatable list or from eatable list
    if EorNE == 0:
        global isEatable
        CurrentObject = noneatabels[random.randint(0,3)]    #Take any random object
        isEatable = False                                      #As this is noneatable so assigining to False
    else:
        CurrentObject = eatabels[random.randint(0,3)]       #Same for Eatable Objects
        isEatable = True

    return CurrentObject

######################################################################################
#Main Loop
while True:
    SUCCESS, img = cap.read()
    img = cv.flip(img, 1)
    
    if GameOver is False:                                       #If Game not Over then Continue
        img = cz.overlayPNG(img, CurrentObject, Position)       #For pasting the images from list to the main Screen
        Position[1] += Speed                                    #adding the Speed to move the object down

        if Position[1]>600:                                     #If yes then Object reached at bottom part of the Screen
            CurrentObject = ResetObject()                       #Again Call the Reset Function

        img, faces = detector.findFaceMesh(img, draw = False)   #Drawing the Faces
        if faces:
            face = faces[0]

            for id in idlist:
                cv.circle(img, face[id], 3, (255, 0, 255), 3)               #For Drawing the 4 points of the Lips
            cv.line(img, face[idlist[0]], face[idlist[1]], (0, 255, 0), 3)  #Up and Down
            cv.line(img, face[idlist[2]], face[idlist[3]], (0, 255, 0), 3)  #Left and Right

            UpDown, _ = detector.findDistance(face[idlist[0]], face[idlist[1]])     #Calculating Distance Between them
            LeftRight, _ = detector.findDistance(face[idlist[2]], face[idlist[3]])

            cx, cy = (face[idlist[0]][0]+face[idlist[1]][0])//2, (face[idlist[0]][1]+face[idlist[1]][1])//2 #Getting the Middle point of up and down point to create a line from the mouth middle point to the object falling
            cv.line(img, (cx,cy), (Position[0]+50, Position[1]+50), (0, 255, 0), 3)
            DistanceMouthObject, _ = detector.findDistance((cx,cy), (Position[0]+50, Position[1]+50)) #Finding the Distane Between the Middle Point and the Position of the Object

            Ratio = int((UpDown/LeftRight)*100)         #And Calulating the Ration to see how much the Mouth is the Open
            if Ratio >= 80:                             #If Value >= 80 then it is Open 
                Mouthstatus = 'Open'
            else:
                Mouthstatus = "Closed"                  #Else Closed
            cv.putText(img, Mouthstatus, (50, 50), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,255), 2)  #Writing Open or Closed on Screen

            if DistanceMouthObject<85 and Mouthstatus == 'Open':    #If Mouth is Open and Distance between mouth and object is < 85 then we can eat it
                if isEatable is True:
                    CurrentObject = ResetObject()
                    Points += 1
                    Speed += 1
                else:
                    GameOver = True                     #If we Eat NonEatable Object

            Time = int(TotalTime-(time.time() - StartTime))             #Calculating the Time
            if Time<0:                                                  #If Time is Over
                GameOver = True
            else:
                cv.putText(img, "Time :- "+str(Time), (20,700), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,255),2)
        
        cv.putText(img, "Points :- " + str(Points), (850, 50), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,255), 2)
    else:
        cv.putText(img, "Game Over", (300,400), cv.FONT_HERSHEY_PLAIN, 7, (255, 0, 255), 10)
        cv.putText(img, "Points :- " + str(Points), (350,500), cv.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 7)
        cv.putText(img, "Press R to Restart", (350,680), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)
        
    cv.imshow("Image", img)

    key = cv.waitKey(1)

    if GameOver == True:                        #To Restart The Game
        if key ==  ord('r'):
            Points = 0
            GameOver = False
            ResetObject()
            isEatable = True
            CurrentObject = eatabels[random.randint(0,3)]
            Speed = 5
            StartTime = time.time()
######################################################################################