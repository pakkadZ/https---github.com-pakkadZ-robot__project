import cv2
import numpy as np

cap = cv2.VideoCapture(0)

center_width = 400  
center_height = 200  

offset_y = 100  

while True:
    ret, frame = cap.read()

    height, width = frame.shape[:2]

    start_x = int((width - center_width) / 2)
    start_y = int((height - center_height) / 2) + offset_y  
    end_x = start_x + center_width
    end_y = start_y + center_height

    center_area = frame[start_y:end_y, start_x:end_x]
    
    # แปลงเป็นสี HSV
    hsv_image = cv2.cvtColor(center_area, cv2.COLOR_BGR2HSV)
    
    # กำหนดช่วงสีแดง (Red)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # กำหนดช่วงสีน้ำเงิน (Blue)
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # กำหนดช่วงสีเขียว (Green)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # ตรวจสอบว่าแต่ละสีมีอยู่ในภาพหรือไม่
    red_detected = cv2.countNonZero(red_mask) > 300  # ปรับค่าตามที่ต้องการ
    blue_detected = cv2.countNonZero(blue_mask) > 300
    green_detected = cv2.countNonZero(green_mask) > 300

    # แปลงเป็นภาพขาวดำเพื่อหาขอบ
    gray_image = cv2.cvtColor(center_area, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

    if lines is not None:
        best_angle = None
        best_line = None
        min_angle_diff = float('inf')  

        for line in lines:
            x1, y1, x2, y2 = line[0]
            delta_y = y2 - y1
            delta_x = x2 - x1
            angle = np.arctan2(delta_y, delta_x) * 180 / np.pi 

            angle_diff = abs(angle)

            if angle_diff < min_angle_diff:
                min_angle_diff = angle_diff
                best_angle = angle
                best_line = line

        if best_line is not None:
            x1, y1, x2, y2 = best_line[0]
            cv2.line(center_area, (x1, y1), (x2, y2), (0, 0, 0), 5)  

            print(f"Best Angle: {best_angle:.2f} degrees")

            if best_angle > 0: 
                cv2.putText(frame, 'Turn Left', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif best_angle < 0:  
                cv2.putText(frame, 'Turn Right', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:  
                cv2.putText(frame, 'Move Forward', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # ตรวจสอบว่าพบสีแดงในภาพ
    if red_detected:
        cv2.putText(frame, 'stageRed', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # ตรวจสอบว่าพบสีน้ำเงินในภาพ
    if blue_detected:
        cv2.putText(frame, 'stageBlue', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # ตรวจสอบว่าพบสีเขียวในภาพ
    if green_detected:
        cv2.putText(frame, 'stageGreen', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Robot Line Following', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
