from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

@app.route('/get_info', methods=['GET'])

def get_disease_info():
    disease_name = request.args.get('disease')
    conn = sqlite3.connect('Diseases.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM diseases WHERE disease_name = ?', (disease_name,))
    disease_info = c.fetchone()
    
    conn.close()
    
    if disease_info:
        response = {
            'name': disease_info[1],
            'reason': disease_info[2],
            'measures': disease_info[3],
            'suggestions': disease_info[5]
            
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Disease not found'}), 404
    
    



@app.route('/get_all', methods=['GET'])
def get_all_disease():
    conn = sqlite3.connect('Diseases.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM diseases')
    disease_info = c.fetchall()
    
    conn.close()
 
    return jsonify(disease_info)

   
        

if __name__ == '__main__':
    app.run(debug=True)
