import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np
from PIL import Image
import os

from skimage.transform import resize
from skimage.color import rgb2lab, lab2rgb
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, array_to_img

MODEL_PATH = r"models\tf"
TEST_PATH = "uploads"
IMAGE_SIZE = (224, 224)

# Load Model
model = keras.models.load_model(MODEL_PATH)
        
def predict(output_dir):
    # Load and preprocessing the test images
    test_dir = TEST_PATH

    #Resize images
    img_width = 224
    img_height = 224
    image_size = (img_width, img_height)

    test_datagen = ImageDataGenerator(
            rescale=1./255,
            )

    test = test_datagen.flow_from_directory(batch_size=128,
                                                        directory=test_dir,
                                                        target_size=image_size,
                                                        color_mode = 'rgb',
                                                        class_mode=None)

    #Convert to LAB
    test_img = []
    for img in test[0]:
        try:
            lab = rgb2lab(img)
            test_img.append(lab[:,:,0])
        except:
            print('error')

    test_img = np.array(test_img)

    test_img = test_img.reshape(test_img.shape+(1,)) #dimensions to be the same for test_img

    grayscale = np.zeros((224, 224, 3))
    grayscale[:,:,0] = test_img[0][:,:,0]
    grayscale = resize(grayscale, (800,600))
    gray_img = lab2rgb(grayscale)

    output1 = model.predict(test_img)
    output1 = output1*128

    result = np.zeros((224, 224, 3))
    result[:,:,0] = test_img[0][:,:,0]
    result[:,:,1:] = output1[0]
    result = resize(result, (800,600))
    color_img = lab2rgb(result)

    # save image result
    color_img = array_to_img(color_img)
    color_img.save(os.path.join(output_dir, "result.jpg"))