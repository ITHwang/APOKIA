from keras.preprocessing.image import ImageDataGenerator
from keras.applications import VGG16
from keras import models
from keras import layers
from keras import optimizers
import matplotlib.pyplot as plt
import tensorflow as tf
import warnings

def generator(train_split_path,
              validation_split_path,
              classes,
              
              rescale = 1./255, 
              rotation_range = 20,
              width_shift_range = 0.1, 
              height_shift_range = 0.1, 
              shear_range = 0.1,
              zoom_range = 0.1,
              horizontal_flip = True,

              target_size = (150, 150),
              batch_size = 256):
    """
    keras.preprocessing.image에 위치한 ImageDataGenerator()와
    ImageDataGenerator 안에 있는 flow_from_directory()를 합친 함수
    """

    train_datagen = ImageDataGenerator(
      rescale = rescale,
      rotation_range = rotation_range,
      width_shift_range = width_shift_range,
      height_shift_range = height_shift_range,
      shear_range = shear_range,
      zoom_range = zoom_range,
      horizontal_flip = horizontal_flip)

    val_datagen = ImageDataGenerator(rescale = rescale)

    train_gen = train_datagen.flow_from_directory(
      train_split_path,
      classes = classes,
      target_size = target_size,
      batch_size = batch_size)
  
    val_gen = val_datagen.flow_from_directory(
      validation_split_path,
      classes = classes,
      target_size = target_size,
      batch_size = batch_size)

    return train_gen, val_gen

def trainer(train_gen, val_gen, second_dense_unit, save_name, 
            weights = "imagenet", include_top = False, input_shape = (150, 150, 3), trainable = False,
            first_dense_unit = 512, first_dense_activation = "relu", second_dense_activation = "softmax",
            loss = "categorical_crossentropy", optimizer = optimizers.Adam(), metrics = ['acc'], 
            train_steps = 350, val_steps = 175, epochs = 15, verbose = 1):
    """
    model 만들고 fitting
    """
  
    conv_base = VGG16(weights = weights, include_top = include_top, input_shape = input_shape)
    conv_base.trainable = trainable

    warnings.filterwarnings(action='ignore')
    with tf.device('/gpu:0'):
      model = models.Sequential()
      model.add(conv_base)
      model.add(layers.Flatten())
      model.add(layers.Dropout(0.5))
      model.add(layers.Dense(first_dense_unit, activation = first_dense_activation))
      model.add(layers.Dropout(0.5)) #추가
      model.add(layers.Dense(first_dense_unit, activation = first_dense_activation)) #추가
      model.add(layers.Dense(second_dense_unit, activation = second_dense_activation)) 
    
      model.compile(
          loss=loss,
          optimizer=optimizer,
          metrics=metrics)
      
      history = model.fit_generator(
            train_gen,
            steps_per_epoch = train_steps,
            epochs = epochs,
            validation_data = val_gen,
            validation_steps = val_steps,
            verbose = verbose)

    
      model.save(save_name)
  
    history_dict = history.history
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
  
    plt.switch_backend('agg') #ssh
    
    epochs = range(1, len(loss) + 1)
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend('best')

    plt.savefig('Training_image.png')
    # plt.show() #local
