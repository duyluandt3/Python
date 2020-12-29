import cv2

face_cascade=cv2.CascadeClassifier(r"D:\DATA\Electronic\Electronic Study\Python\0.New_Couse\25.Image_OpenCV\Detect_Face\haarcascade_frontalface_default.xml")

#img=cv2.imread("photo.jpg")
img=cv2.imread(r"D:\DATA\Electronic\Electronic Study\Python\0.New_Couse\25.Image_OpenCV\Detect_Face\test.jpg")
# Convert to gray images
gray_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect face
faces=face_cascade.detectMultiScale(img,
scaleFactor=1.05,
minNeighbors=5)

# Get data from face'detect value
for x, y, w, h in faces:
    # Draw rectangle in image
    img=cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)

print(type(faces))
print(faces)

resize_image=cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
cv2.imshow("gray", resize_image)
cv2.imwrite("resize_img.jpg", resize_image)
cv2.waitKey(0)
cv2.destroyAllWindows()