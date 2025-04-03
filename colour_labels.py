import numpy as np
import cv2


#upper and lower bounds of the hsv values of the different colours that would be compared to the hsv values found on each face

bounds = {
	"red" : (np.array([160, 75, 75]), np.array([180, 255, 255])),
	"blue" : (np.array([100, 75, 75]), np.array([130, 255, 255])),
	"green" : (np.array([35, 0, 0]), np.array([75, 255, 255])),
	"yellow" : (np.array([20, 75, 75]), np.array([40, 255, 255])),
	"white" : (np.array([0, 0, 20]), np.array([180, 30, 255])),
	"orange" : (np.array([10, 100, 100]), np.array([20, 255, 255]))
}

#The density function takes the hsv value of the image and performs an image mask on it.
def density(img, color):

	lower = bounds[color][0]
	upper = bounds[color][1]

	# Apply the cv2.inrange method to create a mask
	#A pixel is set to 255 if it lies within the boundaries specified otherwise set to 0. 
	#This means it returns the thresholded image
	mask = cv2.inRange(img, lower, upper)
	# Apply the mask on the image to get the density of the colour
	# or how close it is to the colour
	
	return np.sum(mask)/255

#cubestr changes a state that is stored in a dictionary to a long cube string
#This is displayed in the order (URFDLB)

def cubestr(data):

	ret = ""
	for i in "URFDLB":

		ret += "".join(data[i])

	for i in "URFDLB":

		ret = ret.replace(data[i][4], i)
	
	return ret