#!/usr/bin/env python

from StringIO import StringIO

from PIL import Image

import cv2

cap = cv2.VideoCapture('vid.mp4')

def list_camera_ids():
    return ['0', '1']

class Camera(object):

    def __init__(self, camera_id, size, fps):
        self.width = size[0]
        self.height = size[1]

    def get_frame(self):
        ret, image = cap.read()
        ret, image = cv2.imencode('.jpg', image)
        image = Image.fromarray(image)
        #image = Image.new('RGB', (self.width, self.height), 'black')
        # buf = StringIO()
        # image.save(buf, 'JPEG')
        return image.tobytes()
