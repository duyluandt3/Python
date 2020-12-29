import cv2
import numpy as np

im_g = cv2.imread("smallgray.png", 0)

print(im_g)

# Create a new images

cv2.imwrite("newsmallgray.png", im_g)

#for i in im_g.T:
    #print(i)

#for j in im_g.flat:
    #print(j)

ims = np.hstack(im_g, im_g)
print(ims)