from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app) 

# Load model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        # Create dataframe EXACTLY like training data
        input_df = pd.DataFrame({
            "How much do you use the college computer center (CC) for studying?": [str(data["cc"])],
            "How much do you use the college library for studying?": [str(data["library"])],
            "Which of the following resources provided by the college do you find most beneficial for academic success? (Select all that apply)": [str(data["resource"])],
            "On a scale of 1 to 5, how would you rate the effectiveness of the college's academic advising services?": [str(data["advising"])],
            "How many hours per week, on average, do you spend on activities directly related to your studies (e.g., homework, self-study)?": [str(data["study"])],
            "How much attendance do you manage in a semester?": [str(data["attendance"])],
            "Did you have any previous backlogs?": [str(data["backlogs"])]
        })

        prediction = model.predict(input_df)[0]

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

model = pickle.load(open("model.pkl", "rb"))