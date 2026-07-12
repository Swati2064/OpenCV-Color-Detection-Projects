import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Cannot open camera.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Flip frame (optional)
    frame = cv2.flip(frame, 1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Blue HSV Range
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])

    # Create mask
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Remove noise
    kernel = np.ones((5, 5), np.uint8)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_DILATE, kernel)

    # Detect blue color
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # Find contours
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)

            # Blue rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Label
            cv2.putText(frame, "Blue Color", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (255, 0, 0), 2)

    # Display
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Blue Mask", blue_mask)
    cv2.imshow("Blue Color", blue)

    # Exit on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()