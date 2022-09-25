import cv2
cap = cv3.VideoCapture(0)
if not (cap.isOpened()):
    print("Couldn't a;skdfj")
frame = cap.read()
cv2.imwrite('webcamphoto.jpg', frame)
cap.release()


