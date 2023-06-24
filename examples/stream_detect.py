from roboflow import Roboflow
import time
import random
import cv2
from resources.config import API_KEY

COUNTER_INTERRUPT = 15

rf = Roboflow(api_key=API_KEY)
project = rf.workspace("meva").project("hard-hat-sample-2zw77")
model = project.version(2).model


def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    if not color:
        color = [random.randint(0, 255) for _ in range(3)]

    tl = (line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1)  # line/font thickness
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))

    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA, )


def format_preds(predictions):
    formatted_predictions = []
    for pred in predictions:
        formatted_pred = [
            pred["x"],
            pred["y"],
            pred["x"],
            pred["y"],
            pred["confidence"],
            pred["class"],
        ]
        print(formatted_pred)

        # convert to top-left x/y from center
        formatted_pred[0] = int(formatted_pred[0] - pred["width"] / 2)
        formatted_pred[1] = int(formatted_pred[1] - pred["height"] / 2)
        formatted_pred[2] = int(formatted_pred[2] + pred["width"] / 2)
        formatted_pred[3] = int(formatted_pred[3] + pred["height"] / 2)

        formatted_predictions.append(formatted_pred)

    return formatted_predictions


def plot_predictions(frame, predictions) -> None:
    for formatted_pred in predictions:
        plot_one_box(
            formatted_pred[:-1],
            frame,
            color=[0, 255, 0] if formatted_pred[5] == "head" else [255, 0, 0],
            label=formatted_pred[5],
            line_thickness=2,
        )


def stream(camera: int = None, resolution: tuple[int, int] = (500, 400)):
    cap = cv2.VideoCapture(camera if camera else 0)
    prev_frame_time = 0
    counter = 0
    saved_predictions = []
    while True:
        counter += 1
        if cv2.waitKey(1) == ord('q'):
            break

        _, frame = cap.read()
        frame = cv2.resize(frame, resolution)

        new_frame_time = time.time()
        fps = str(int(1 / (new_frame_time - prev_frame_time)))
        prev_frame_time = new_frame_time

        # putting the FPS count on the frame
        cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

        if saved_predictions:
            plot_predictions(frame, saved_predictions)

        if counter == COUNTER_INTERRUPT:
            counter = 0
            # get predictions
            response = model.predict(frame).json()
            predictions = response["predictions"]

            formatted_predictions = format_preds(predictions)
            plot_predictions(frame, formatted_predictions)
            saved_predictions = formatted_predictions

        cv2.imshow('Hard Hat Worker -- Test', frame)
    cap.release()


stream(resolution=(1024, 720))

cv2.destroyAllWindows()
