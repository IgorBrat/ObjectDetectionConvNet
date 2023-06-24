from roboflow import Roboflow
from resources.config import API_KEY

rf = Roboflow(api_key=API_KEY)

# version = rf.workspace("meva").project("hard-hat-sample-2zw77").version(3)

project = rf.workspace("meva").project("hard-hat-sample-2zw77")

model = project.version(2).model
prediction = model.predict("../images/test/example.jpg")

# Detailed list of predictions with boxes, confidence and class of each object
print(prediction.json())

# Preview result image
prediction.save("../images/prediction/output.jpg")
