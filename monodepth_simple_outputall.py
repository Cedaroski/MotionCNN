# Copyright UCL Business plc 2017. Patent Pending. All rights reserved.
#
# The MonoDepth Software is licensed under the terms of the UCLB ACP-A licence
# which allows for non-commercial use only, the full terms of which are made
# available in the LICENSE file.
#
# For any other use of the software not covered by the UCLB ACP-A Licence,
# please contact info@uclb.com

from __future__ import absolute_import, division, print_function

# only keep warnings and errors
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

import numpy as np
import argparse
import cv2 as cv
import re
import time
import tensorflow as tf
import tensorflow.contrib.slim as slim
import scipy.misc
import matplotlib.pyplot as plt
import os

from monodepth_model import *
from monodepth_dataloader import *
from average_gradients import *

parser = argparse.ArgumentParser(description='Monodepth TensorFlow implementation.')

parser.add_argument('--encoder', type=str, help='type of encoder, vgg or resnet50', default='vgg')
parser.add_argument('--image_path', type=str, help='path to the image', required=True)
parser.add_argument('--checkpoint_path', type=str, help='path to a specific checkpoint to load', required=True)
parser.add_argument('--input_height', type=int, help='input height', default=256)
parser.add_argument('--input_width', type=int, help='input width', default=512)

args = parser.parse_args()


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


def post_process_disparity(disp):
    _, h, w = disp.shape
    l_disp = disp[0, :, :]
    r_disp = np.fliplr(disp[1, :, :])
    m_disp = 0.5 * (l_disp + r_disp)
    l, _ = np.meshgrid(np.linspace(0, 1, w), np.linspace(0, 1, h))
    l_mask = 1.0 - np.clip(20 * (l - 0.05), 0, 1)
    r_mask = np.fliplr(l_mask)
    return r_mask * l_disp + l_mask * r_disp + (1.0 - l_mask - r_mask) * m_disp


def test_simple(params):
    """Test function."""

    left = tf.placeholder(tf.float32, [2, args.input_height, args.input_width, 3])
    model = MonodepthModel(params, "test", left, None)

    # SESSION
    config = tf.ConfigProto(allow_soft_placement=True)
    sess = tf.Session(config=config)

    # SAVER
    train_saver = tf.train.Saver()

    # INIT
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())
    coordinator = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coordinator)

    # RESTORE

    restore_path = args.checkpoint_path.split(".")[0]
    train_saver.restore(sess, restore_path)



    output_directory = os.path.dirname(args.image_path)

    fileList=[]
    listdir(output_directory, fileList)

    # np.save(os.path.join(output_directory, "{}_disp.npy".format(output_name)), disp_pp)
    count =1
    for file in fileList:

        count+=1
        if count%10==0:
            print("output {} with totall is {}".format(count, fileList.__len__()))
            start = time.clock()
        output_name = os.path.splitext(os.path.basename(file))[0]
        input_image = scipy.misc.imread(file, mode="RGB")
        original_height, original_width, num_channels = input_image.shape
        input_image = scipy.misc.imresize(input_image, [args.input_height, args.input_width], interp='lanczos')
        input_image = input_image.astype(np.float32) / 255
        input_images = np.stack((input_image, np.fliplr(input_image)), 0)

        disp = sess.run(model.disp_left_est[0], feed_dict={left: input_images})
        disp_pp = post_process_disparity(disp.squeeze()).astype(np.float32)

        if count % 10 ==0:
            end = time.clock()
            print("FPS is {}".format(1.0/(end - start)))
        disp_to_img = scipy.misc.imresize(disp_pp.squeeze(), [original_height, original_width])
        depth_img = 1148.52 * 80.11 / disp_pp.squeeze() / 512
        depth_img = np.clip(depth_img, 0, 65000)


        depth_to_img = scipy.misc.imresize(depth_img.squeeze(), [original_height, original_width])
        depth_to_img_scale = depth_to_img / 255 * (depth_img.max() - depth_img.min()) + depth_img.min()

        f = open(os.path.join(output_directory, "../txtdepth/{}_depth.txt".format(output_name)), 'w')
        for i in range(original_height):
            for j in range (original_width):
                f.write(format(depth_to_img_scale[i][j])+' ')
    
            f.write("\n")
        f.close()
        '''
        f = open("depth_max_min", 'w')
        f.write(format(depth_img.max())+' '+format(depth_img.min()))S
        f.close()
    '''
        # f = open("depth_max_min", 'w')
        plt.imsave(os.path.join(output_directory, "../monodepth/{}_depth.png".format(output_name)), depth_to_img,
                   cmap='gray')
        plt.imsave(os.path.join(output_directory, "../monodisp/{}_disp.png".format(output_name)), disp_to_img,  cmap='gray')




def main(_):
    params = monodepth_parameters(
        encoder=args.encoder,
        height=args.input_height,
        width=args.input_width,
        batch_size=2,
        num_threads=1,
        num_epochs=1,
        do_stereo=False,
        wrap_mode="border",
        use_deconv=False,
        alpha_image_loss=0,
        disp_gradient_loss_weight=0,
        lr_loss_weight=0,
        full_summary=False)

    test_simple(params)


if __name__ == '__main__':
    tf.app.run()
