import cv2
import matplotlib.pyplot as plt
import numpy as np
import pickle

import numpy as np
import matplotlib.pyplot as plt

from skimage.color import rgb2lab, lab2rgb
from skimage.transform import resize
from skimage.io import imsave

import tensorflow as tf
from tensorflow import keras
from keras.layers import Conv2D, UpSampling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

model = keras.models.load_model('models/tf')

test = "D:/Downloads/DL_LEC/img/enstein.png"

def show_image(image_path):
    # plt.imshow(image)
    # img = cv2.imread(image_path)import pickle
    pass

def predict():
    #Convert to LAB
    test_img = []
    # for img in test[0]:
    #     try:
    #         lab = rgb2lab(img)
    #         test_img.append(lab[:,:,0])
    #     except:
    #         print('error')
    try:
        lab = rgb2lab(test)
        test_img.append(lab[:,:,0])
    except:
        print('error')
    test_img = np.array(test_img)

    test_img = test_img.reshape(test_img.shape+(1,)) #dimensions to be the same for test_img


    grayscale = np.zeros((224, 224, 3))
    grayscale[:,:,0] = test_img[12][:,:,0]
    grayscale = resize(grayscale, (800,600))
    gray_img = lab2rgb(grayscale)

    output1 = model.predict(test_img)
    output1 = output1*128

    result = np.zeros((224, 224, 3))
    result[:,:,0] = test_img[12][:,:,0]
    result[:,:,1:] = output1[0]
    result = resize(result, (800,600))
    color_img = lab2rgb(result)

    titles = ['Grayscale Image', 'Colored Image']
    images = [gray_img, color_img]

    with open("static/1.jpg", "wb") as file:
        file.write(color_img)
