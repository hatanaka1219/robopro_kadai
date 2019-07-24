import cv2
import numpy as np
def fil_proc(image,filter_2d):
    img_fil = cv2.filter2D(image, -1, filter_2d)
    print("end fil")
    return img_fil


def hsv(img,h,s,v):
    print("hsvfilter")
    # 画像として読み込み
    #stream = request.files['image'].stream
    #img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    #img_raw = cv2.imdecode(img_array, 1)
    img_raw = img
    img_hsv = cv2.cvtColor(img_raw, cv2.COLOR_BGR2HSV)
    img_hsv[:,:,(0)] = img_hsv[:,:,(0)]*h
    img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*s
    img_hsv[:,:,(2)] = img_hsv[:,:,(2)]*v
    img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
    return img_bgr
