import cv2, time, pandas
from datetime import datetime

first_frame=None
status_list=[None, None]
time=[]
df=pandas.DataFrame(columns=["Start", "End"])

# Access and turn on camera
video=cv2.VideoCapture(0)
while True:
    # Create a frame for window camera
    check, frame=video.read()
    # Detect motion
    status=0
    #time.sleep(3)
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur filter
    gray=cv2.GaussianBlur(gray,(21, 21), 0)
    # Get first frame only
    if first_frame is None:
        first_frame=gray
        continue
    
    # Compare first_frame and gray
    delta_frame=cv2.absdiff(first_frame, gray)

    # Create threshold data
    thre_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # Dilation thre frame
    thre_frame=cv2.dilate(thre_frame, None, iterations=2)
    # Create contour in thre_frame
    (cnts,_)=cv2.findContours(thre_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 5000:
            continue
        # if has motion -> status=1
        status=1
        # Create rectagle in frame
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
    
    status_list.append(status)
    status_list=status_list[-2:]
    # Check status_list and start record times
    if status_list[-1]==1 and status_list[-2]==0:
       time.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        time.append(datetime.now()) 

 #   cv2.imshow("Gray Frame", gray)
 #   cv2.imshow("Delta Frame", delta_frame)
 #   cv2.imshow("Threshold Frame", thre_frame)
    cv2.imshow("Color Frame", frame)
    
    key=cv2.waitKey(1)

    # press "q" to exit
    if key==ord("q"):
        if status==1:
            time.append(datetime.now())
        break
    else:
        pass

#print(status_list)
# Create motion data table
for i in range(0, len(time), 2):
    df=df.append({"Start":time[i], "End":time[i+1]}, ignore_index=True)

# Create cvs file
df.to_csv("./26.WC_Detector/Times.csv")

video.release()
cv2.destroyAllWindows()