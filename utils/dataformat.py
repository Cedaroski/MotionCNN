import tensorflow as tf
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description='MotionCNN Dataformat implementation.')

parser.add_argument('--outpur_dir', type=str, help='path to output', default='./')
parser.add_argument('--input_dir', type=str, help='path to output', default='./')
parser.add_argument('--output_name', type=str, help='path to output', default='posename')
parser.add_argument('--encoder', type=str, help='type of encoder, vgg or resnet50', default='vgg')
parser.add_argument('--image_path', type=str, help='path to the image', required=True)
parser.add_argument('--checkpoint_path', type=str, help='path to a specific checkpoint to load', required=True)
parser.add_argument('--input_height', type=int, help='input height', default=256)
parser.add_argument('--input_width', type=int, help='input width', default=512)
args = parser.parse_args()

def eular2R(a,b,c):
    R= np.eye(4)
    return R


def R2eular(R):
    eular=np.array([0,0,0])
    return eular


def main():
    output_directory = args.outpur_dir
    output_name = args.output_name
    input_dir = args.input_dir
    f_origin = open(os.path.join(output_directory, "origin.txt"), 'r')
    pose_list = f_origin.readlines()

    f = open(os.path.join(output_directory, "{}.txt".format(output_name)), 'w')
    for i in range(pose_list.__len__()):
        f.write("\n")
    f.close()


if __name__ == '__main__':
    main()