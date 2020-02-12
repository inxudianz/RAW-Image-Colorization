import tensorflow as tf
import cv2
import flask
import numpy
import sklearn

if __name__ == "__main__":
    print("\n---Version---\n")
    print("Tensorflow : ", tf.__version__)
    print("OpenCV : ", cv2.__version__)
    print("Flask : ", flask.__version__)
    print("Scikit-learn : ", sklearn.__version__)
    print("Numpy : ", numpy.__version__)