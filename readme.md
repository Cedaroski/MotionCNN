# MotionCNN
## NOT WORK YET
It is a supervised learning method for camera ego-motion estimation.
A sub-mission for a SLAM system.
## Dependency
tensorflow 1.10

## train
`
python moton_train.py --mode train --data_path /home/user/Data/2019-03-12/ --filenames_file /home/user/Data/2019-03-12/binocular_train.txt --log_directory tmp --model_name train2layer --num_epochs 100 --batch_size 1
`
## TODO
1. read the ego-motionl label
2. Superivised learning of ego-motion
3. By the depth prediction from monodepth, change the net to unsuperivised
