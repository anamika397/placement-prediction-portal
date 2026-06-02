from ml.predict import predict_placement

prediction, probability = predict_placement(
    8.5,
    80,
    85,
    75,
    3
)

print(prediction)
print(probability)