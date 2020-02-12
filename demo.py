import os

import cv2 as cv
import tensorflow.keras.backend as K
import numpy as np
import sklearn.neighbors as nn

from config import img_rows, img_cols
from config import nb_neighbors, T, epsilon
from build_model import build_model

def colorize_picture(image_name):
    model_name = "model.99-2.9937.hdf5"
    model_weights_path = 'Trained_Models/' + model_name
    model = build_model()
    model.load_weights(model_weights_path)

    print(model.summary)

    image_folder = '../RAW/Input'
    
    h, w = img_rows // 4, img_cols // 4

    q_ab = np.load("data/pts_in_hull.npy")
    nb_q = q_ab.shape[0]

    filename = os.path.join(image_folder, image_name)
    print('Processing Image: {}'.format(filename))

    bgr = cv.imread(filename)
    gray = cv.imread(filename, 0)
    bgr = cv.resize(bgr, (img_rows, img_cols), cv.INTER_CUBIC)
    gray = cv.resize(gray, (img_rows, img_cols), cv.INTER_CUBIC)

    lab = cv.cvtColor(bgr, cv.COLOR_BGR2LAB)
    L = lab[:, :, 0]
    a = lab[:, :, 1]
    b = lab[:, :, 2]

    X_blank = np.empty((1, img_rows, img_cols, 1), dtype=np.float32)
    X_blank[0, :, :, 0] = gray / 255.

    X_colorised = model.predict(X_blank)
    X_colorised = X_colorised.reshape((h * w, nb_q))

    X_colorised = np.exp(np.log(X_colorised + epsilon) / T)
    X_colorised = X_colorised / np.sum(X_colorised, 1)[:, np.newaxis]

    q_a = q_ab[:, 0].reshape((1, 313))
    q_b = q_ab[:, 1].reshape((1, 313))

    X_a = np.sum(X_colorised * q_a, 1).reshape((h, w))
    X_b = np.sum(X_colorised * q_b, 1).reshape((h, w))

    X_a = cv.resize(X_a, (img_rows, img_cols), cv.INTER_CUBIC)
    X_b = cv.resize(X_b, (img_rows, img_cols), cv.INTER_CUBIC)

    X_a = X_a + 128
    X_b = X_b + 128

    out_lab = np.zeros((img_rows, img_cols, 3), dtype=np.int32)
    out_lab[:, :, 0] = lab[:, :, 0]
    out_lab[:, :, 1] = X_a
    out_lab[:, :, 2] = X_b
    out_L = out_lab[:, :, 0]
    out_a = out_lab[:, :, 1]
    out_b = out_lab[:, :, 2]

    out_lab = out_lab.astype(np.uint8)
    out_bgr = cv.cvtColor(out_lab, cv.COLOR_LAB2BGR)
    out_bgr = out_bgr.astype(np.uint8)

    cv.imwrite('Output/{}_image.png'.format(0), gray)
    cv.imwrite('Output/{}_gt.png'.format(0), bgr)
    cv.imwrite('Output/{}_out_bgr.png'.format(0), out_bgr)

    cv.imwrite('static/img/{}_image.png'.format(0), gray)
    cv.imwrite('static/img/{}_out_bgr.png'.format(0), out_bgr)

    K.clear_session()

    lab = cv.cvtColor(bgr, cv.COLOR_BGR2LAB)


if __name__ == '__main__':
    colorize_picture("test.jpg")
    