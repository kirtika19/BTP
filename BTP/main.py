from flask import Flask, request, jsonify
import sqlite3
import numpy as np
import tensorflow as tf
from modelintegration import load_model, predict

app = Flask(__name__)

# Load the SQLite database and TFLite model when the app starts
conn = sqlite3.connect('Diseases.db')
model_path = 'C:/Users/Dedeepya/Downloads/model.tflite'
interpreter = tf.lite.Interpreter(model_path='C:/Users/Dedeepya/Downloads/model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

class_labels = ["Early_Blight," ,"Healthy", "Late_Blight"]


@app.route('/get_info', methods=['GET'])

def get_disease_info():
    disease_name = request.args.get('disease')
    conn = sqlite3.connect('Diseases.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM diseases WHERE name = ?', (disease_name,))
    disease_info = c.fetchone()
    
    conn.close()
    
    if disease_info:
        response = {
            'name': disease_info[1],
            'description': disease_info[2]
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Disease not found'}), 404

@app.route('/predict', methods=['POST'])
def predict_disease():
   
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})
    
    image = request.files['image']

    #print(image)

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
    app.run(debug=True)