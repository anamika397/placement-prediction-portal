import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'ml',
    'placement_model.pkl'
)

model = joblib.load(MODEL_PATH)

def predict_placement(cgpa, aptitude, coding, communication, projects):

    data = [[
        cgpa,
        aptitude,
        coding,
        communication,
        projects
    ]]

    prediction = model.predict(data)

    return prediction[0]