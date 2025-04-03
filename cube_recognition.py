#program that carries out the cube recognition and colour extraction
#Using functions from colourlabeler.py to determine which colour is present
#All colours will then be stored in the state dictionary
import numpy as np
import cv2
import time
from colour_labels import density, cubestr



def screen_record():
    #initial state that will be filled using data dictionary to match the format
    #of cube() and displaycube() 
    INITIAL = {'B': [['', '', ''],['', '', ''],['', '', '']],
           'D': [['', '', ''],['', '', ''],['', '', '']],
           'F': [['', '', ''],['', '', ''],['', '', '']],
           'L': [['', '', ''],['', '', ''],['', '', '']],
           'R': [['', '', ''],['', '', ''],['', '', '']],
           'U': [['', '', ''],['', '', ''],['', '', '']]}
    last_time = time.time()
    cv2.startWindowThread()
    # cv2.namedWindow("preview")

    #Create a VideoCapture object 
    cap = cv2.VideoCapture(0)
    faces = "FUDLRB"
    idx = 0
    #empty dictionary to hold the colors of each face
    data = {
        "F" : ["", "", "", "", "", "", "", "", ""],
        "U" : ["", "", "", "", "", "", "", "", ""],
        "D" : ["", "", "", "", "", "", "", "", ""],
        "L" : ["", "", "", "", "", "", "", "", ""],
        "R" : ["", "", "", "", "", "", "", "", ""],
        "B" : ["", "", "", "", "", "", "", "", ""]
    }

    while(True):
        #Read from the videocapture object
        _, img = cap.read()
        last_time = time.time()

        #opencv function to retreive hsv value of a area of the video
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #color hashmap that relates the colour to their bgr value
        # this would be the color displayed in the CV window

        colors = {
        	"red" : (0, 0, 255),
        	"blue" : (255, 0, 0),
        	"green" : (0, 255, 0),
        	"yellow" : (0, 255, 255),
        	"white" : (255, 255, 255),
        	"orange" : (0, 165, 255)
        }
        #offset is the distance between centres of color extraction
        offset = 75
        z = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):

                #centres of circles that will be shown on screen
                px = 358 + j * offset
                py = 280 + i * offset
                maxDens = [0, "white"]
                crop = img_hsv[(py-35):(py+35), (px-35):(px+35)]
                for k in ("red", "blue", "green", "yellow", "white", "orange"):
                    #density() from colour_labele
                    d = density(crop, k)
                    if d > maxDens[0]:
                        maxDens[0] = d
                        maxDens[1] = k

                #display 6 circles that change colour to the colour of each small square        

                cv2.circle(img,(px, py), 5, colors[maxDens[1]], -1)
                #
                data[faces[idx]][z] = maxDens[1][0]
                z += 1
   
        #if q is pressed the process is quit  
        cv2.imshow(faces[idx] + ' Face', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            cap.release()
            break

        #user submits the colours for the face by pressing h    
        if cv2.waitKey(25) & 0xFF == ord('h'):
            idx += 1
            if idx == len(faces):
                #print(data)

                for i, value in data.items():
                    data[i] = (np.reshape(value,(3,3))).tolist()
                for i in INITIAL:
                    INITIAL[i]=data[i]
                

                cv2.destroyAllWindows()
                cap.release()
                #print(INITIAL)
                break


    return INITIAL