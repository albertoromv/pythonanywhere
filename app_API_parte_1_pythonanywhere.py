from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import sklearn
import pickle
import numpy as np

# comentario nuevo

app = Flask(__name__)
app.config['DEBUG'] = True

root = '/home/albertoromv/modelo_clase/'
root_db = "/home/albertoromv/databases/"
model = pickle.load(open(root + 'advertising.model', 'rb'))
print(model.coef_)

# POST {"TV":, "radio":, "newspaper":} -> It returns the sales prediction for input investments
@app.route('/predict', methods=['POST'])
def get_predict():

    # Get current time for the PREDICTIONS table
    str_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Establish SQLITE3 connection
    conn = sqlite3.connect(root_db + "advertising.db")
    crs = conn.cursor()

    # Get POST JSON data
    data = request.get_json()
    tv = data.get("TV",0)
    radio = data.get("radio",0)
    newspaper = data.get("newspaper",0)

    # Model prediction
    pred = model.predict(np.array([[tv, radio, newspaper]]))[0]

    # Save prediction in PREDICTIONS table
    crs.execute(''' INSERT INTO PREDICTIONS(pred_date,TV,radio,newspaper,prediction)
                    VALUES(?,?,?,?,?) ''', (str_time, tv, radio, newspaper, pred))
    conn.commit()
    conn.close()
    return str(pred), 200

@app.route('/review_predicts', methods=['GET'])
def return_predicts():
    conn = sqlite3.connect(root_db + "advertising.db")
    crs = conn.cursor()
    query = "SELECT * FROM PREDICTIONS"
    resultado = jsonify(crs.execute(query).fetchall())

    conn.close()
    return resultado, 200


#app.run(port=4000)
