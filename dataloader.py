#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 23:07:29 2017

@author: no1
"""

import tensorflow as tf   
import scipy.misc as misc
import os
def write_binary():  
    cwd = os.getcwd()

#    all_files = os.listdir(cwd)

    classes=['a','b','c']
    writer = tf.python_io.TFRecordWriter('data.tfrecord')  
    for index, name in enumerate(classes):
        class_path = os.path.join(cwd,name)
#        if tf.gfile.Exists(class_path):
#            tf.gfile.DeleteRecursively(class_path)
#        tf.gfile.MakeDirs(class_path)
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path , img_name)
            img = misc.imread(img_path)
            img1 = misc.imresize(img,[250,250,3])
            img_raw = img1.tobytes()              #将图片转化为原生bytes
            example = tf.train.Example(features=tf.train.Features(feature={
                    'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
                "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[index]))}
                ))  #  将数据整理成 TFRecord 需要的数据结构 

    #序列化  
            serialized = example.SerializeToString()  
    #写入文件  
            writer.write(serialized)  
    writer.close()  

def read_and_decode(filename):  
    #创建文件队列,不限读取的数量  
    filename_queue = tf.train.string_input_producer([filename],shuffle=False)  
    # create a reader from file queue  
    reader = tf.TFRecordReader()  
    #reader从 TFRecord 读取内容并保存到 serialized_example 中 
    _, serialized_example = reader.read(filename_queue)  

    features = tf.parse_single_example(     # 读取 serialized_example 的格式 
        serialized_example,  
        features={  
            'label': tf.FixedLenFeature([], tf.int64),  
            'img_raw': tf.FixedLenFeature([], tf.string)      
        }  
    )  # 解析从 serialized_example 读取到的内容  
    img=tf.decode_raw(features['img_raw'],tf.uint8)
    img = tf.reshape(img, [250, 250, 3])
    label = tf.cast(features['label'], tf.int32)
    return img,label  


#write_binary()  

img,label = read_and_decode('data.tfrecord')  

img_batch, label_batch = tf.train.shuffle_batch([img,label], batch_size=18, capacity=2000, min_after_dequeue=100, num_threads=2)  
##  
# sess  
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)  
    coord = tf.train.Coordinator()  #创建一个协调器，管理线程
    #启动QueueRunner, 此时文件名队列已经进队。
    threads=tf.train.start_queue_runners(sess=sess,coord=coord)  

    img, label = sess.run([img_batch, label_batch])  
    #for i in range(18):
    #    cv2.imwrite('%d_%d_p.jpg'%(i,label[i]),img[i])
    coord.request_stop()
    coord.join(threads)
