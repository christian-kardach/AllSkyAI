import json
from PIL import Image, ImageDraw
import tensorflow as tf
import urllib.request
import numpy as np
import os
import datetime
from dotenv import load_dotenv

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
load_dotenv()

LIVE_URL = os.getenv('ALL_SKY_LIVE_URL')


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def lite_model(interpreter, images):
    interpreter.allocate_tensors()
    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], images)
    interpreter.invoke()
    return interpreter.get_tensor(interpreter.get_output_details()[0]['index'])


def classify_bw_live():
    model_path = "models/allskyai_bw.tflite"
    labels_path = "./models/labels.txt"
    temp_image_path = "./temp.jpg"
    temp_image_path_mod = "./tempMod.jpg"

    class_names = load_labels(labels_path)

    interpreter = tf.lite.Interpreter(
        model_path=model_path,
        num_threads=1)
    interpreter.allocate_tensors()

    _, height, width, _ = interpreter.get_input_details()[0]['shape']

    urllib.request.urlretrieve(LIVE_URL, temp_image_path)

    # Resize
    img = Image.open(temp_image_path)
    img = img.resize((height, width), Image.ANTIALIAS)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, 0), (120, 120)), fill="black")
    img.save(temp_image_path_mod)

    img = tf.keras.utils.load_img(
        temp_image_path_mod,
        target_size=(height, width),
        color_mode='grayscale',
    )

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    probs_lite = lite_model(interpreter, img_array)[0]

    label_index = np.argmax(probs_lite)
    score = tf.nn.softmax(probs_lite)

    # Timestamp
    dt = datetime.datetime.now(datetime.timezone.utc)
    utc_time = dt.replace(tzinfo=datetime.timezone.utc)
    utc_timestamp = utc_time.timestamp()

    """
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(class_names[label_index], 100 * np.max(score))
    )
    """
    os.remove(temp_image_path)  # Remove the cached file
    os.remove(temp_image_path_mod)  # Remove the cached file

    tag = class_names[label_index]
    confidence = 100 * np.max(score)

    data_json = dict()
    data_json['AllSkyAISky'] = tag
    data_json['AllSkyAIConfidence'] = confidence
    data_json['UTC'] = utc_timestamp
    return json.dumps(data_json)


def classify_color_live():
    return json.dumps("Not implemented")