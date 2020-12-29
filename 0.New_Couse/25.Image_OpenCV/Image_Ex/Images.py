import cv2

img = cv2.imread("galaxy.jpg", 0)

print(img)
# Print images pixel
print(img.shape)


# Resize images
resize_image = cv2.resize(img,(int(img.shape[1]/2), int(img.shape[0]/2)))
cv2.imshow("Galaxy", resize_image)
# Create new image
cv2.imwrite("resize_galaxy.jpg",resize_image)
# Wait 2s to close images
cv2.waitKey(0)
cv2.destroyAllWindows()
