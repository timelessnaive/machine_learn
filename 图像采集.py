import cv2
from time import sleep
cap = cv2.VideoCapture(0)

p=10; time_break=0.1
c=0; f=0
path=r'C:\code\machine_learn\tfClassifier\image_classification\test/'
while(True):
    ret, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('frame',gray)
    cv2.imshow('frame', frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):

    key=cv2.waitKey(10)
    #print(key)

    if(key==113):#q
        break
    elif(key==115):#s
        f=p

    if (f):
        sleep(time_break)
        f -= 1
        c += 1
        name = str(c)
        cv2.imwrite(path+name + '.jpg', frame)
        print(name)
cap.release()
cv2.destroyAllWindows()