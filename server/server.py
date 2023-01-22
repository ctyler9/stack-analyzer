import torch
from PIL import Image
import torchvision.transforms.functional as TF

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


classes_dict = {0: 'audemarspiguet',
                1: 'patekphilippe',
                2: 'breitling',
                3: 'seiko',
                4: 'jaegerlecoultre',
                5: 'iwc',
                6: 'gucci',
                7: 'omega',
                8: 'zenith',
                9: 'panerai',
                10: 'rolex',
                11: 'cartier',
                12: 'movado'}

TRANSFORM = torch.jit.load("data/scripted_transform.pt")

CLASSIFIER = torch.jit.load("data/scripted_model.pt")


@app.route("/")
def home():
    return "Hello World"


@app.route("/classify", methods=["POST", "OPTIONS"])
def classify():
    files = request.files
    image = Image.open(files['image'])
    img_tensor = TF.to_tensor(image)
    x = TRANSFORM(img_tensor).unsqueeze(0)
    prediction = CLASSIFIER(x)

    print(prediction)

    return {
        "brandPredictions": sorted(
            list(
                zip(
                    classes_dict.values(),
                    [round(x, 4) for x in map(float, prediction[0])]
                )
            ),
            key=lambda p: p[1],
            reverse=True
        )
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
