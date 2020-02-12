import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard, Callback
from build_model import build_model
from config import patience, epochs, num_train_samples, num_valid_samples, batch_size
from utils import resize_image
from data_generator import train_gen, valid_gen
import cv2
import os

model_path = "Trained_Models/"

if __name__ == "__main__":
    
    tensor_board = TensorBoard(log_dir='.\logs', histogram_freq=0, write_graph=True, write_images=True)    
    model_names = model_path + 'model.{epoch:02d}-{val_loss:.4f}.hdf5'
    model_checkpoint = ModelCheckpoint(model_names, monitor='val_loss', verbose=1, save_best_only=True)
    early_stop = EarlyStopping('val_loss', patience=patience)
    reduce_lr = ReduceLROnPlateau('val_loss', factor=0.1, patience=int(patience / 4), verbose=1)

    class MyCbk(Callback):
        def __init__(self, model):
            Callback.__init__(self)
            self.model_to_save = model

        def on_epoch_end(self, epoch, logs=None):
            fmt = model_path + 'model.%02d-%.4f.hdf5'
            self.model_to_save.save(fmt % (epoch, logs['val_loss']))
    
    model = build_model()
    model_checkpoint = MyCbk(model)
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    
    print(model.summary())

    callbacks = [tensor_board, model_checkpoint, early_stop, reduce_lr]

    model.fit_generator(train_gen(),
                            steps_per_epoch=num_train_samples // batch_size,
                            validation_data=valid_gen(),
                            validation_steps=num_valid_samples // batch_size,
                            epochs=epochs,
                            verbose=1,
                            callbacks=callbacks,
                            use_multiprocessing=False,
                            workers=8
                            )
    