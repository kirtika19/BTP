from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the TFLite model
model_path = 'model.tflite'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define class labels
class_labels = ["Early_Blight", "Healthy", "Late_Blight"]

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image = request.files['image']

    img_array = tf.image.decode_image(image.read())
    img_array = tf.image.resize(img_array, (256, 256))
    img_array = tf.expand_dims(img_array, 0) / 255.0

    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class_index = np.argmax(output_data)

    predicted_class_label = class_labels[predicted_class_index]

    return jsonify({'predicted_class': predicted_class_label})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

