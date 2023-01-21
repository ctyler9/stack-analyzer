from flask import Flask
import fastai.vision as fastai
app = Flask(__name__)

CLASSIFIER = fastai.load_learner("../models", "classifier.pth")


@app.route("/")
def home():
    return "Hello World"


@app.route("/classify")
def classify():
    image = fastai.image.open_image("./seiko-monster.jpg")
    prediction = CLASSIFIER.predict(image)

    print(prediction)

    return {
        "brandPredictions": sorted(list(zip(CLASSIFIER.data.classes, [round(x, 4) for x in map(float, prediction[2])])))
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
