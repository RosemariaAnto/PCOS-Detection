from flask import Flask, session, render_template, request, redirect, url_for
import os
import numpy as np
import tensorflow as tf
from keras.models import load_model                                                                                                                                                                                                         
import logging
from werkzeug.utils import secure_filename

os.environ['PYTHONIOENCODING'] = 'utf-8'

app = Flask(__name__)

# Generate a random secret key
import secrets
secret_key = secrets.token_hex(16)  # Generate a 32-character hexadecimal string
app.secret_key = secret_key

# Set logging level to only display warnings and above
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('scipy').setLevel(logging.ERROR)

# Load your trained models
MODEL_PATH_inception = 'inception.h5'
MODEL_PATH_mobilenet = 'mobile.h5'
MODEL_PATH_2 = 'vgg.h5'
model_inception = load_model(MODEL_PATH_inception)
model_mobilenet = load_model(MODEL_PATH_mobilenet)
model_2 = load_model(MODEL_PATH_2)
global inception_v3
global mobilenet

# Enable mixed precision training
policy = tf.keras.mixed_precision.Policy('mixed_float16')
tf.keras.mixed_precision.set_global_policy(policy)

# Create the 'uploads' directory if it doesn't exist
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')
    
# Create the 'processed_images' directory if it doesn't exist
if not os.path.exists('static/processed_images'):
    os.makedirs('static/processed_images')


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/predict2', methods=['GET', 'POST'])
def predict2():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            session['selected_file'] = filename
            file.save(os.path.join('static/uploads', filename))
            return redirect(url_for('image'))

    return render_template('predict2.html')


@app.route('/image', methods=['GET', 'POST'])
def image():
    filename = session.get('selected_file', 'No file selected')
    processed_img_path = None

    if 'selected_file' in session:
        selected_filename = session['selected_file']
        file_path = os.path.join('uploads', selected_filename)
        processed_img_path = process_image(file_path)  # Assuming you have a function to get processed image path

    if request.method == 'POST':
        return redirect(url_for('predict_result'))

    return render_template('image.html', filename=filename, processed_img_path=os.path.basename(processed_img_path) if processed_img_path else None)




from keras.preprocessing import image as keras_image

def process_image(file_path):
    filename = secure_filename(os.path.basename(file_path))
    img_path = os.path.join('static/uploads', filename)
    img = keras_image.load_img(img_path, target_size=(224, 224))
    processed_img = keras_image.img_to_array(img)
    processed_img = processed_img / 255.0  
    processed_img = np.expand_dims(processed_img, axis=0)
    processed_img_path = os.path.join('static/processed_images', 'processed_' + filename)
    keras_image.save_img(processed_img_path, processed_img[0])
    return processed_img_path



@app.route('/predict_result', methods=['GET', 'POST'])
def predict_result():
    filename = session.get('selected_file', 'No file selected')
    if request.method == 'POST':
        selected_model = request.form.get('model')
        if selected_model:
            if selected_model == 'inception':
                return predict_inception(filename)
            elif selected_model == 'mobilenet':
                return predict_mobilenet(filename)
            elif selected_model == 'model2':
                return predict_2(filename)
            elif selected_model == "compare":
                return compare_results(filename)

    return redirect(url_for('home'))


def predict_inception(filename):
    img_path = os.path.join('static/uploads', filename)
    img = keras_image.load_img(img_path, target_size=(224, 224))
    processed_img = keras_image.img_to_array(img)
    processed_img = processed_img / 255.0  
    processed_img = np.expand_dims(processed_img, axis=0)

    preds_inception = model_inception.predict(processed_img)
    pred_class_inception = np.argmax(preds_inception, axis=1)[0]
    prediction_inception = "Not Affected" if pred_class_inception == 1 else "Affected"
    global inception_v3
    inception_v3 = prediction_inception
    return render_template('predict_result.html', prediction=prediction_inception)


def predict_mobilenet(filename):
    img_path = os.path.join('static/uploads', filename)
    img = keras_image.load_img(img_path, target_size=(224, 224))
    processed_img = keras_image.img_to_array(img)
    processed_img = processed_img / 255.0  
    processed_img = np.expand_dims(processed_img, axis=0)

    preds_mobilenet = model_mobilenet.predict(processed_img)
    pred_class_mobilenet = np.argmax(preds_mobilenet, axis=1)[0]
    prediction_mobilenet = "Not Affected" if pred_class_mobilenet == 1 else "Affected"
    global mobilenet
    mobilenet = prediction_mobilenet
    return render_template('predict_result.html', prediction=prediction_mobilenet)


def predict_2(filename):
    img_path = os.path.join('static/uploads', filename)
    img = keras_image.load_img(img_path, target_size=(224, 224))
    processed_img = keras_image.img_to_array(img)
    processed_img = processed_img / 255.0  
    processed_img = np.expand_dims(processed_img, axis=0)

    preds_2 = model_2.predict(processed_img)
    pred_class_2 = np.argmax(preds_2, axis=1)[0]
    prediction_2 = "Not Affected" if pred_class_2 == 1 else "Affected"
    return render_template('predict_result.html', prediction=prediction_2)


def compare_results(filename):
    img_path = os.path.join('static/uploads', filename)
    img = keras_image.load_img(img_path, target_size=(224, 224))
    processed_img = keras_image.img_to_array(img)
    processed_img = processed_img / 255.0  
    processed_img = np.expand_dims(processed_img, axis=0)

    preds_mobilenet = model_mobilenet.predict(processed_img)
    pred_class_mobilenet = np.argmax(preds_mobilenet, axis=1)[0]
    prediction_mobilenet = "Not Affected" if pred_class_mobilenet == 1 else "Affected"

    preds_inception = model_inception.predict(processed_img)
    pred_class_inception = np.argmax(preds_inception, axis=1)[0]
    prediction_inception = "Not Affected" if pred_class_inception == 1 else "Affected"
    global inception_v3
    inception_v3 = prediction_inception

    return render_template('predict_result.html', 
                           prediction_inception=prediction_inception,
                           prediction_mobilenet=prediction_mobilenet,
                           prediction_2=prediction_inception)


@app.route('/counsel_page')
def counsel_page():
    # Logic for counsel page
    return render_template('counsel.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
