import os
import tensorflow as tf
import cv2 as cv
from numpy import array,shape
from time import time
from matplotlib import pyplot as plt

# change this as you see fit
# image_path = r'D:\ACM\machine_learn\tfClassifier\image_classification\2.jpg'

model_path='./output1.pb'
label_path="./labels1.txt"


def cut(p,k=7):
    (x,y,z)=shape(p)
    new=p[x//k:,y//k:(k-1)*y//k]
    return new


def draw(bar_label,values):
    fig = plt.figure(u"Top-5 预测结果")

    ax = fig.add_subplot(111)
    ax.bar(range(len(values)), values, tick_label=bar_label, width=0.5, fc='g')
    ax.set_ylabel(u'probabilityit')
    ax.set_title(u'Top-5')
    for a, b in zip(range(len(values)), values):
        ax.text(a, b + 0.0005, b, ha='center', va='bottom', fontsize=7)
    plt.show()
    #plt.savefig('pic' + str(i) + '.png')


def convert(img_cv):
    img_encode = cv.imencode('.jpg', img_cv)[1]
    data_encode = array(img_encode)
    mybytes = data_encode.tobytes()
    return mybytes


def solve(image_data,label_lines,f_w=None,f_draw=False):
    st=time();label_l=[];score_l=[]
    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:

            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            label_l.append(human_string)
            score_l.append(int(score*100))
            if(f_w):
                f_w.write('{} (score = {:.5f})\n'.format(human_string,score))
            #f.write('%s (score = %.5f)\n' % (human_string, score))
            #print('%s (score = %.5f)' % (human_string, score))

        if(f_draw):
            draw(label_l[:5],score_l[:5])

        if(f_w):
            f_w.write('----- time={:.2f}s------------\n'.format(time()-st))
        if(label_lines[top_k[0]]=='milk' and score_l[0]-score_l[1]<=80):#milk权值过大，需要特判
            return label_lines[top_k[1]]
        else:
            return label_lines[top_k[0]]


def main():
    f_w = open(r'C:\code\machine_learn\tfClassifier\image_classification\ans.txt', 'w')
    path=r'C:\code\machine_learn\tfClassifier\image_classification\test'

    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    label_lines = [line.rstrip() for line in tf.gfile.GFile(label_path)]
    for root, dirs, files in os.walk(path):
        for file in files:
            st=time()
            image_path=os.path.join(root,file)

            #image_data = tf.gfile.FastGFile(image_path, 'rb').read()
            image_data=cv.imread(image_path)
            image_data=convert(image_data)
            ans = solve(image_data, label_lines,f_w)
            ed = time()
            if(ans == root.replace(path+'\\','')):
                f_w.write('图片为{}，所需时间为{:.2f}\n'.format(ans, ed - st))
            else:
                f_w.write('图片路径为{},图片为{}，识别结果为{}，'
                          '所需时间为{:.2f}\n'.format(image_path.replace(path + '\\', '')
                                                                     ,ans, root.replace(path + '\\', '')
                                                                     , ed - st))
            f_w.write('------------\n')
    f_w.close()

if __name__ == "__main__":
    main()
