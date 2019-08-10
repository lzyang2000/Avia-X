import sys
from time import time, sleep
from datetime import datetime
import atexit


import cv2
from keras.models import load_model
import numpy as np
import picamera
import picamera.array

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.inference import load_image
from utils.preprocessor import preprocess_input

# parameters for loading data and images
#image_path = sys.argv[1]
detection_model_path = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
gender_model_path = '../trained_models/gender_models/simple_CNN.81-0.96.hdf5'
emotion_labels = get_labels('fer2013') # {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 
                                       #  4: 'sad', 5: 'surprise', 6: 'neutral'}
#gender_labels = get_labels('imdb')
#font = cv2.FONT_HERSHEY_SIMPLEX

# hyper-parameters for bounding boxes shape
gender_offsets = (30, 60)
gender_offsets = (10, 10)
emotion_offsets = (20, 40)
emotion_offsets = (0, 0)

# init cam
camera = picamera.PiCamera(sensor_mode=4)
camera.resolution = (1280, 720)
camera.rotation = 180
camera.start_preview(alpha=0)

# handle exit


def onStop():
    camera.close()
    print("Shutdown")
    sys.exit()


atexit.register(onStop)


# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
gender_classifier = load_model(gender_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]
gender_target_size = gender_classifier.input_shape[1:3]


# Here is where we conduct the loop for taking pics and reconizing emotions
while(1):
    print("New iter")
    start = datetime.now()
    # take image
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='rgb')
        # At this point the image is available as stream.array
        image = stream.array

    # loading images
    rgb_image = image  # load_image(image_path, grayscale=False)
    # load_image(image_path, grayscale=True)
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)

    gray_image = np.squeeze(gray_image)
    gray_image = gray_image.astype('uint8')

    faces = detect_faces(face_detection, gray_image)
    i = 1
    for face_coordinates in faces:
        #  x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
        #  rgb_face = rgb_image[y1:y2, x1:x2]

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]

        try:
            #rgb_face = cv2.resize(rgb_face, (gender_target_size))
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

    #   rgb_face = preprocess_input(rgb_face, False)
    #   rgb_face = np.expand_dims(rgb_face, 0)
    #   gender_prediction = gender_classifier.predict(rgb_face)
    #   gender_label_arg = np.argmax(gender_prediction)
    #   gender_text = gender_labels[gender_label_arg]

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        prediction=emotion_classifier.predict(gray_face)
        emotion_label_arg=np.argmax(prediction)
        #emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
        emotion_text = emotion_labels[emotion_label_arg]

    #    if gender_text == gender_labels[0]:
    #    color = (0, 0, 255) #blue
    #    else:
    #    color = (255, 0, 0)  # red

    #    draw_bounding_box(face_coordinates, rgb_image, color)
        #draw_text(face_coordinates, rgb_image, gender_text, color, 0, -20, 1, 2)
   #     draw_text(face_coordinates, rgb_image,
   #               emotion_text, color, 0, -50, 1, 2)
        print("Prediction %d" % i + ":", emotion_text)
        i += 1

    end = datetime.now()
    delta = end-start
    print("Total predict time: %dms," %
          int((end-start).total_seconds() * 1000), "sleeping for 5 seconds...")
    sleep(5)


#bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
#cv2.imwrite('../images/predicted_test_image.png', bgr_image)
