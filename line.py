import cv2
import numpy as np


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to read frame.")
        break

    height, width = frame.shape[:2]
    center_area = frame[int(height*0.25):int(height*0.75), int(width*0.25):int(width*0.75)]


    gray_image = cv2.cvtColor(center_area, cv2.COLOR_BGR2GRAY)
    

    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)


    edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)


    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            cv2.line(center_area, (x1, y1), (x2, y2), (0, 0, 0), 5)  


        line_center = (x1 + x2) / 2
        image_center = center_area.shape[1] / 2 

        if line_center < image_center - 50:  
            cv2.putText(frame, 'Turn Left', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            print("Turn Left")
        elif line_center > image_center + 50:  
            cv2.putText(frame, 'Turn Right', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            print("Turn Right")
        else:  # ถ้าเส้นอยู่ตรงกลาง
            cv2.putText(frame, 'Move Forward', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            print("Move Forward")

    else:
        
        cv2.putText(frame, 'No Line Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        print("No Line Detected")


    cv2.imshow('Robot Line Following', frame)

   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
