#time: 20211109 
#author: wangjunyi
#基于GAN生成手写数字

import torch
import torch.nn as nn
from torch.utils.data import Dataset


import pandas, numpy, random
import matplotlib.pyplot as plt


# minst_dataset = MnistDataset('mount/My Drive/Colab Notebooks/myo_gan/mnist_data/mnist_train.csv')
minst_dataset = open("./mnist_dataset/train-labels-idx1-ubyte.gz",'r')
minst_dataset.plot_image(17)