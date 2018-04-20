import cv2
import StringIO
import numpy
import json
import sys
import os

caffe_root = '/home/nhong/workspace/caffe/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')

import caffe

caffe.set_mode_cpu()

model_def = caffe_root + 'models/b90eb88e31cd745525ae/deploy.prototxt'
model_weights = caffe_root + 'models/b90eb88e31cd745525ae/googlenet_finetune_web_car_iter_10000.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)


net.blobs['data'].reshape(1,        # batch size
                      3,         # 3-channel (BGR) images
                      227, 227)  # image size is 227x227

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_channel_swap('data', (2,1,0))

for line in sys.stdin:
    memfile = StringIO.StringIO()
    try:
        memfile.write(json.loads(line).encode('latin-1'))
    except:
        continue
         
    memfile.seek(0)
    car = numpy.load(memfile)


    transformed_image = transformer.preprocess('data', car)

    net.blobs['data'].data[...] = transformed_image

    output = net.forward()

    output_prob = output['prob'][0]

    #print 'predicted class is:', output_prob.argmax()

    # load ImageNet labels
    labels_file = caffe_root + 'data/ilsvrc12/synset_words.txt'
    labels = numpy.loadtxt(labels_file, str, delimiter='\t')

    print 'output label:', labels[output_prob.argmax()]