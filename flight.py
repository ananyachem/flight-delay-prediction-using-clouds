import pickle
from flask import Flask, render_template, request

app = Flask(__name__)
model = pickle.load(open(r'D:\Python\Flask\flight.pkl', 'rb'))

origin_mapping = {
    "ATL": [1, 0, 0, 0, 0],
    "DTW": [0, 1, 0, 0, 0],
    "JFK": [0, 0, 1, 0, 0],
    "MSP": [0, 0, 0, 1, 0],
    "SEA": [0, 0, 0, 0, 1]
}

destination_mapping = {
    "ATL": [0, 0, 0, 0, 1],
    "DTW": [0, 0, 0, 1, 0],
    "JFK": [0, 0, 1, 0, 0],
    "MSP": [0, 1, 0, 0, 0],
    "SEA": [1, 0, 0, 0, 0]
}

@app.route('/')
def home():
    return render_template("flight.html")

@app.route('/prediction', methods=['POST'])
def predict():
    name = request.form['name']
    month = request.form['month']
    dayofmonth = request.form['dayofmonth']
    dayofweek = request.form['dayofweek']
    origin = request.form['origin']
    destination = request.form['destination']
    dept = request.form['dept']
    arrtime = request.form['arrtime']
    actdept = request.form['actdept']
    dept15 = int(dept) - int(actdept)

    origin_encoded = origin_mapping.get(origin, [0, 0, 0, 0, 0])
    destination_encoded = destination_mapping.get(destination, [0, 0, 0, 0, 0])

    total = [
        [name, month, dayofmonth, dayofweek] + origin_encoded + destination_encoded +
         [dept, arrtime, actdept, dept15]
    ]

    y_pred = model.predict(total)
    
    if y_pred == [0]:
        ans = "The flight will be on time"
    else:
        ans = "The flight will be delayed"
    
    return render_template("flight.html", showcase=ans)

if __name__ == '__main__':
    app.run(debug=True)


