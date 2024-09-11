# app.py

from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Load the trained model
model_path = 'Hackthon.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from form
    int_features = [x for x in request.form.values()]
    inter_features = [np.array(int_features)]
    print(inter_features)
    print(inter_features[0][0])
    # print(inter_features[0][0].str().lower())

    final_features = []
    # Gender condition
    if inter_features[0][0].astype(str).lower() == "male":
        final_features.append(1)
    elif inter_features[0][0].astype(str).lower() == "female":
        final_features.append(2)

    final_features.append(int(inter_features[0][1]))

    # Employment type condition
    if inter_features[0][2].astype(str).lower() == "salaried":
        final_features.append(1)
    elif inter_features[0][2].astype(str).lower() == "business":
        final_features.append(2)
    else:
        final_features.append(3)  # Assuming 'working' falls into this 'else'
    # Convert the string to integer for inter_features[2]

    final_features.append(int(inter_features[0][3]))

    # Condition for high/moderate/low
    if inter_features[0][4].astype(str).lower() == "high":
        final_features.append(1)
    elif inter_features[0][4].astype(str).lower() == "moderate":
        final_features.append(2)
    else:
        final_features.append(3)
    # Convert the string to integer for inter_features[4]
    final_features.append(int(inter_features[0][5]))
    print(final_features)

    # Convert final_features to a 2D array before using in the model
    final_features = np.array(final_features).reshape(1, -1) 
    print(final_features)

    # Make prediction
    prediction = model.predict(final_features)

    if prediction[0] == 0:
        output ="Following Product offering we have for you : [DWS California Tax-Free Income Fund - Class S] and [DWS Capital Growth Fund - Class S]"
    elif prediction[0] == 1:
        output ="Following Product offering we have for you : [DWS Communications Fund - Class S] and [DWS Core Equity Fund - Class S]"
    elif prediction[0] == 2:
        output ="Following Product offering we have for you : [DWS Emerging Markets Fixed Income Fund - Class S] and [DWS Floating Rate Fund - Class S]"
    elif prediction[0] == 3:
        output ="Following Product offering we have for you : [DWS Global High Income Fund - Class S] and [DWS Short Duration Fund - Class S]"
   
    return render_template('index.html', prediction_text='Prediction: {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
