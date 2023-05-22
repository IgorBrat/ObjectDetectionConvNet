import cv2


def format_preds(predictions):
    formatted_predictions = []
    for pred in predictions:
        formatted_pred = {
            'box': [  # converted from center to top-left: top=left_xy-bottom-right_xy
                int(pred["x"] - pred["width"] / 2),
                int(pred["y"] - pred["height"] / 2),
                int(pred["x"] + pred["width"] / 2),
                int(pred["y"] + pred["height"] / 2),
            ],
            'confidence': round(pred["confidence"], 3),
            'class': pred["class"],
            'depth': 0,
        }
        formatted_predictions.append(formatted_pred)

    return formatted_predictions


def get_colormap(depth_frame):
    return cv2.applyColorMap(cv2.convertScaleAbs(depth_frame, alpha=0.03), cv2.COLORMAP_JET)
