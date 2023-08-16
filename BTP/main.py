from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

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
    
    

if __name__ == '__main__':
    app.run(debug=True)