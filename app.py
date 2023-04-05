import os
import threading
from flask import Flask, render_template, request
import joblib
from housing.pipeline.pipeline import Pipeline
from housing.entity.housing_predictor import HousingData, HousingPredictor
from housing.constant import *

app = Flask(__name__)

# Load the pipeline for retraining the model
pipeline = Pipeline()

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "housing"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
HOUSING_DATA_KEY = "housing_data"
MEDIAN_HOUSING_VALUE_KEY = "median_house_value"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])
        housing_median_age = float(request.form['housing_median_age'])
        total_rooms = float(request.form['total_rooms'])
        total_bedrooms = float(request.form['total_bedrooms'])
        population = float(request.form['population'])
        households = float(request.form['households'])
        median_income = float(request.form['median_income'])
        ocean_proximity = request.form['ocean_proximity']
  
        housing_data = HousingData(longitude=longitude,
                                   latitude=latitude,
                                   housing_median_age=housing_median_age,
                                   total_rooms=total_rooms,
                                   total_bedrooms=total_bedrooms,
                                   population=population,
                                   households=households,
                                   median_income=median_income,
                                   ocean_proximity=ocean_proximity)
        housing_df = housing_data.get_housing_input_data_frame()
        housing_predictor = HousingPredictor(model_dir=MODEL_DIR)
        prediction = housing_predictor.predict(X=housing_df)

        prediction_str = f"${prediction[0]:,.2f}"
        # Render the template with the prediction result
        return render_template ('result.html', longitude=longitude, latitude=latitude,
		housing_median_age=housing_median_age, total_rooms=total_rooms,
		total_bedrooms=total_bedrooms, population=population, households=households,
		median_income=median_income,
		ocean_proximity=ocean_proximity, prediction=prediction_str)
        
    # Render the template with the input form
    return render_template('index.html')

@app.route('/retrain', methods=['GET', 'POST'])
def retrain():
    if request.method == 'POST':
        # Check if the pipeline is already running
        if pipeline.experiment.running_status:
            # Render the template with an error message
            return render_template('retrain.html', message='The model retraining process is already running.')
        
        # Start the pipeline for retraining the model
        pipeline.start()
         # Run the pipeline in a new thread
        threading.Thread(target=pipeline.start).start()

        # Render the template with a success message
        return render_template('retrain.html', message='The model retraining process has started.')
    
    # If the request method is GET, check if the pipeline is running or not
    if pipeline.experiment.running_status:
        running_status = True
    else:
        running_status = False
    
    # Render the template with the running status
    return render_template('retrain.html', running_status=running_status)

if __name__ == '__main__':
    app.run(debug=True)