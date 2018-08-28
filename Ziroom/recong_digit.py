# coding:gbk


import urllib
import cv2
import numpy as np
import os


def get_digit(img_url):
    resp = urllib.urlopen(img_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret = []
    for pos in range(10):
        min_index = -1
        min_loss = 100
        img_reg = image[:,pos*30:(pos+1)*30]
        for digit_file in os.listdir('template'):
            digit = cv2.imread(os.path.join('template', digit_file))
            digit = cv2.cvtColor(digit, cv2.COLOR_BGR2GRAY)
            loss = np.mean(np.square(img_reg-digit))
            if loss < min_loss:
                min_loss = loss
                min_index = digit_file.split('.')[0]
        ret.append(min_index)
    return ret

