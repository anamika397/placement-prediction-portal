import joblib

model = joblib.load("ml/placement_model.pkl")


def predict_placement(
    cgpa,
    aptitude,
    coding,
    communication,
    projects
):

    prediction = model.predict(
        [[
            cgpa,
            aptitude,
            coding,
            communication,
            projects
        ]]
    )[0]

    probability = model.predict_proba(
        [[
            cgpa,
            aptitude,
            coding,
            communication,
            projects
        ]]
    )[0][1]

    return prediction, round(probability * 100, 2)
