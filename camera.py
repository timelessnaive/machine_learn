import cv2 as cv
import tensorflow as tf
from retrain_model_classifier import solve,convert,cut
from os.path import join
from time import time
#from about_serials import comin,goout
#import serial
model_path='./output1.pb'
label_path="./label1.txt"
path = r'C:\code\machine_learn\tfClassifier\image_classification'


def main():
    cap = cv.VideoCapture(0);c = 0

    label_lines = [line.rstrip() for line in tf.gfile.GFile(label_path)]

    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    #img=cv.imread(path+'\\test.jpg')
    #print(solve(convert(img), label_lines))
    with open(join(path,'log.txt'),'w') as f:
        while (True):
            ret, img = cap.read()
            img=cut(img)
            try:
                cv.imshow('img', img)
            except:
                print('error')
            key = cv.waitKey(10)
            if (key == 113):  # q
                break
            elif (key == 115):  # s
                print(solve(convert(img), label_lines, f, f_draw=True))
                c += 1
                cv.imwrite('{0}\\{1}.jpg'.format(path, str(c)), img)
                print(c)
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()