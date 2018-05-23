import cv2
import StringIO
import numpy
import json
import sys
import os
import csv

def transform_img(img, img_width=227, img_height=227):

    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img

caffe_root = '/home/nhong/workspace/caffe/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')

labels = list()

with open('/home/nhong/stanford-cars/labels.csv', 'rb') as csvfile:
    labels_data = csv.reader(csvfile, delimiter=',')
    for row in labels_data:
        labels.append(row[1])

import caffe
import caffe_pb2

caffe.set_mode_cpu()

mean_blob = caffe_pb2.BlobProto()
with open(caffe_root + 'models/stanford-cars/mean.binaryproto') as f:
    mean_blob.ParseFromString(f.read())
mean_array = numpy.asarray(mean_blob.data, dtype=numpy.float32).reshape(
    (mean_blob.channels, mean_blob.height, mean_blob.width))


model_def = caffe_root + 'models/stanford-cars/deploy.prototxt'
model_weights = caffe_root + 'models/stanford-cars/caffe_model_1_iter_22169.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)


net.blobs['data'].reshape(1,        # batch size
                      3,         # 3-channel (BGR) images
                      227, 227)  # image size is 227x227

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', mean_array)
transformer.set_transpose('data', (2,0,1))
#transformer.set_channel_swap('data', (2,1,0))

img = cv2.imread('/home/nhong/stanford-cars/cars_train/00001.jpg', cv2.IMREAD_COLOR)
img = transform_img(img, img_width=227, img_height=227)

net.blobs['data'].data[...] = transformer.preprocess('data', img)
out = net.forward()
pred_probas = out['prob']
print labels[pred_probas.argmax()]