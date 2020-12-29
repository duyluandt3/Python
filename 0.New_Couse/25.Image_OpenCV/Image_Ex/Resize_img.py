import cv2
import glob

image_list = []
resize_list = []
file_path = "SampleImage/*.jpg"

for name in glob.glob(file_path):
    img = cv2.imread(name, 0)
    #image_list.append(img)
    re_img = cv2.resize(img, (100,100))
    image_list.append(re_img)
    cv2.imshow("Img", re_img)
    cv2.waitKey(2000)
    # Rename image
    cv2.imwrite("resize"+name, re_img)

#print(image_list)
