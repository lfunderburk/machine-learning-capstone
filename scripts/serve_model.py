from flask import Flask, request
import pickle
import sys, os

# Set up paths
sys.path.append(os.path.abspath(os.path.join('.','./data/', './clean-data/')))
sys.path.append(os.path.abspath(os.path.join('.','./models/')))


app = Flask(__name__)

# Load the trained model
with open('models/hard_voting_classifier_co2_fuel.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request
    data = request.get_json(force=True)

    # Make predictions using the loaded model
    predictions = model.predict(data)

    # Return the predictions as JSON
    return {"predictions": predictions.tolist()}

if __name__ == '__main__':
    app.run(port=8000, debug=True)