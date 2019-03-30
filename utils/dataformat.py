import tensorflow as tf
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description='MotionCNN Dataformat implementation.')

parser.add_argument('--outpur_dir', type=str, help='path to output', default='/home/lab1501/PycharmProjects/MotionCNN/Data')
parser.add_argument('--input_dir', type=str, help='path to output', default='/home/lab1501/PycharmProjects/ZED_examples/svo_recording/utils')
parser.add_argument('--output_name', type=str, help='path to output', default='posename')

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
    f_origin = open(os.path.join(input_dir, "2019-03-13_13-50-33_pose_joint.txt"), 'r')
    pose_list = f_origin.readlines()

    f = open(os.path.join(output_directory, "{}.txt".format(output_name)), 'w')
    for i in range(pose_list.__len__()):
        str = pose_list[i]
        new_str = str.split(' ', 7)
        try:
            print(new_str[6])
            f.write(new_str[2]+" "+new_str[3]+" "+new_str[4]+" "+new_str[5]+" "+new_str[6]+" "+new_str[7])
        except IndexError:
            print('Blank')

    f.close()


if __name__ == '__main__':
    main()