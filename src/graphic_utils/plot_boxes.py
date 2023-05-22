import random
import cv2


def plot_one_box(box, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    if not color:
        color = [random.randint(0, 255) for _ in range(3)]

    tl = (line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1)  # line/font thickness
    c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))

    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA, )


def plot_predictions(frame, predictions) -> None:
    for formatted_pred in predictions:
        plot_one_box(
            formatted_pred['box'],
            frame,
            color=[0, 255, 0] if formatted_pred['class'] == "head" else [255, 0, 0],
            label=f"{formatted_pred['class']} {str(round(formatted_pred['confidence'], 2))}",
            line_thickness=2,
        )
