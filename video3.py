import cv2
import StringIO
import numpy
import json
import sys
import os
import csv


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

while True:
    line = sys.stdin.readline()
    if len(line) < 2:
        continue

    line = line.strip()

    # print len(line)

    memfile = StringIO.StringIO()
    try:
        memfile.write(json.loads(line).encode('latin-1'))
    except Exception as e:
        print("line length: " + str(len(line)) + " error: " + str(e))
        continue
         
    memfile.seek(0)
    car = numpy.load(memfile)


    transformed_image = transformer.preprocess('data', car)

    net.blobs['data'].data[...] = transformed_image

    output = net.forward()

    output_prob = output['prob'][0]

    print 'predicted class is:', labels[output_prob.argmax()]

    # load ImageNet labels
    # labels_file = caffe_root + 'data/ilsvrc12/synset_words.txt'
    # labels = numpy.loadtxt(labels_file, str, delimiter='\t')

    # print 'output label:', labels[output_prob.argmax()]