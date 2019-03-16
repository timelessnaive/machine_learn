import cv2 as cv
import tensorflow as tf
from retrain_model_classifier import solve,convert
from time import time
from about_serials import get_ser
import serial
model_path='./model2.pb'
label_path="./label2.txt"
path = r'C:\code\machine_learn\tfClassifier\image_classification'

portx='com4'
bps=9600
tiemx=5

def main():
    cap = cv.VideoCapture(0);c = 0

    label_lines = [line.rstrip() for line in tf.gfile.GFile(label_path)]

    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


    #ser=get_ser()

    ser=serial.Serial(portx, bps)

    #img=cv.imread(path+'\\test.jpg')
    #print(solve(convert(img), label_lines))
    f=open(r'C:\code\machine_learn\tfClassifier\image_classification\log.txt'
           ,'w')
    while (True):
        ret, img = cap.read()
        cv.imshow('img', img)

        key = cv.waitKey(10)
        if(ser.inWaiting()):
            s=ser.read_all()
            if(s==b'start'):
                st = time()
                ans=solve(convert(img), label_lines, f, f_draw=True)
                print(ans)
                ans='ac'
                print(c)
            elif(s==b'finish' ):
                break
        if(key==113):
            break
        '''
        if (key == 113):  # q
            break
        
        elif (key == 115):  # s
            st=time()
            print(solve(convert(img), label_lines,f,f_draw=True))
            c += 1
            cv.imwrite('{0}\\{1}.jpg'.format(path,str(c)), img)
            print(c)
        '''
    f.close()
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()