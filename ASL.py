import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import time
import os
import sys
from language import change_language
from manual_text_autocorrect import fix_text
from speech import text_to_speech
import enchant

diction = enchant.Dict("en_US")


lang = sys.argv[1]

delay = 4
last_time = time.time()

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
script_directory = os.path.dirname(os.path.abspath(__file__))

# # Load the model
# model = load_model(os.path.join(script_directory, "Model_SJ/keras_model.h5"), compile=False)

# # Load the labels
# class_names = open(os.path.join(script_directory, "Model_SJ/labels.txt"), "r").readlines()

# Load the model
model = load_model("Model_SJ/keras_Model.h5", compile=False)

# Load the labels
class_names = open("Model_SJ/labels.txt", "r").readlines()

detector = HandDetector(maxHands=1)

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

res = ""
result = ""
prev_char = ""

while True:
    current_time = time.time()
    # Grab the webcamera's image for model.
    ret, image = camera.read()
    imageCopy = image.copy()
    hands, _ = detector.findHands(imageCopy)
    imageCopy = cv2.resize(imageCopy, (700, 500))
    cv2.putText(imageCopy, "Letter: " + prev_char, (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Image Display", imageCopy)

    if current_time - last_time >= delay:

        if hands:

            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

            cv2.imshow("Model Image", image)

            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

            # Normalize the image array
            image = (image / 127.5) - 1

            # Predicts the model
            prediction = model.predict(image)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            print("Class:", class_name[2], end=" ")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

            prev_char = class_name[2]
            res += class_name[2]
            cv2.putText(imageCopy, "Letter: " + prev_char, (20, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)



        else:
            res += " "
            print("space")
            cv2.putText(imageCopy, "Letter: " + "space", (20, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        last_time = current_time  # Update the last time

    

    # Exit the loop if 'q', 'j', 'f', 'o', 'r', or spacebar is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('j') or key == ord('f') or key == ord('o') or key == 32:
        break

result = fix_text(res)    

camera.release()
cv2.destroyAllWindows()

from gtts import gTTS
import os

print("Result is: " + result)
text_to_speech(result,lang)

# res = ""

# # Set the delay to 3 seconds (3000 milliseconds)
# delay = 3000  # ms
# last_time = time.time()
# flash_counter = 0

# while True:
#     # Grab the webcamera's image.
#     ret, image = camera.read()

#     # Resize the raw image into (224-height,224-width) pixels
#     image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

#     # Show the image in a window
#     cv2.imshow("Webcam Image", image)

#     # Make the image a numpy array and reshape it to the models input shape.
#     image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

#     # Normalize the image array
#     image = (image / 127.5) - 1

#     current_time = time.time()
    
#     if current_time - last_time >= delay / 1000:
#         # Predicts the model
#         prediction = model.predict(image)
#         index = np.argmax(prediction)
#         class_name = class_names[index]
#         confidence_score = prediction[0][index]

#         # Print prediction and confidence score
#         res += class_name[2]
#         # print("Class:", class_name[2:], end="")
#         # print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
#         last_time = current_time
#         print(class_name[2])


#     # Listen to the keyboard for presses.
#     keyboard_input = cv2.waitKey(1)

#     # 32 is the ASCII for the space bar on your keyboard.
#     if keyboard_input == 32 :
#         break

# camera.release()
# cv2.destroyAllWindows()

# from gtts import gTTS
# import os

# print(res)
# text_to_speech(res,lang)

