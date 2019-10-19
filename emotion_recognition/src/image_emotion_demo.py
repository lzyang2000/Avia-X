import sys
from time import time, sleep
import atexit

import cv2
from keras.models import load_model
import numpy as np
import picamera
import picamera.array
from emotion_recognition.src import utils
from emotion_recognition.src.utils.datasets import get_labels
from emotion_recognition.src.utils.inference import detect_faces
from emotion_recognition.src.utils.inference import draw_text
from emotion_recognition.src.utils.inference import draw_bounding_box
from emotion_recognition.src.utils.inference import apply_offsets
from emotion_recognition.src.utils.inference import load_detection_model
from emotion_recognition.src.utils.inference import load_image
from emotion_recognition.src.utils.preprocessor import preprocess_input

detection_model_path = './emotion_recognition/trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = './emotion_recognition/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
# gender_model_path = '../trained_models/gender_models/simple_CNN.81-0.96.hdf5'
emotion_labels = get_labels('fer2013')
# parameters for loading data and images
# image_path = sys.argv[1]
# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
# gender_classifier = load_model(gender_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]
# gender_target_size = gender_classifier.input_shape[1:3]
#init cam
camera = picamera.PiCamera()
camera.resolution = (1024, 768)
camera.rotation = 180
camera.fullscreen = False
camera.start_preview()# -w 1296 -h 972 #-p ('50,50,950,950')
camera.preview.window = '50,50,90,90'
#camera.start_preview()
# camera = cv2.VideoCapture(0)
# if not camera.isOpened():
#     raise Exception("Could not open video device")

def main_predict():
    # gender_labels = get_labels('imdb')
    font = cv2.FONT_HERSHEY_SIMPLEX

    # hyper-parameters for bounding boxes shape
    # gender_offsets = (30, 60)
    # gender_offsets = (10, 10)
    emotion_offsets = (20, 40)
    emotion_offsets = (0, 0)



    # handle exit
    def onStop():
        camera.stop_preview()
        camera.release()
        print("Shutdown")
        GPIO.cleanup()
        sys.exit()


    atexit.register(onStop)



    # Here is where we conduct the loop for taking pics and reconizing emotions
    def predict():
        '''
        Function that actually predicts, calling the webcam once to get image
        and forward propagate it through the network. Note that the models and
        params are loaded above.

        :return: emotion detected
        '''
        print("New iter")
        start = time()
        # take image
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='rgb')
            # At this point the image is available as stream.array
            image = stream.array
        # ret, frame = camera.read()
        #cv2.imshow("origin", image)
        # image = frame[:, :, ::-1]  # BGR -> RGB

        # loading images
        rgb_image = image  # load_image(image_path, grayscale=False)
        gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)  # load_image(image_path, grayscale=True)

        gray_image = np.squeeze(gray_image)
        gray_image = gray_image.astype('uint8')

        faces = detect_faces(face_detection, gray_image)

        for face_coordinates in faces:
            #  x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
            #  rgb_face = rgb_image[y1:y2, x1:x2]

            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]

            try:
                # rgb_face = cv2.resize(rgb_face, (gender_target_size))
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
            emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
            emotion_text = emotion_labels[emotion_label_arg]

            #    if gender_text == gender_labels[0]:
            #    color = (0, 0, 255) #blue
            #    else:
            #    color = (255, 0, 0)  # red

            #    draw_bounding_box(face_coordinates, rgb_image, color)
            # draw_text(face_coordinates, rgb_image, gender_text, color, 0, -20, 1, 2)
            #     draw_text(face_coordinates, rgb_image,
            #               emotion_text, color, 0, -50, 1, 2)
            print("Prediction:", emotion_text)

        end = time()
        print("Total predict time: %.fs," % (end - start), "sleeping for 5 seconds...")
        try:
            return emotion_text
        except:
            return None

    # bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    # cv2.imwrite('../images/predicted_test_image.png', bgr_image)
    return predict()
