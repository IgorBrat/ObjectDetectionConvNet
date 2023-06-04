import cv2
import numpy as np
import time
from datetime import datetime

from src.depth.depth import set_predictions_depth
from src.utils.format_utils.format import format_predictions, get_colormap
from src.utils.graphic_utils.plot_boxes import plot_predictions
from src.utils.util import count_images_in_directory
from src.application.web_app import dbmanager


def stream(
        model,
        pipeline,
        labels: dict,
        resolution: tuple[int, int] = (720, 564),
        counter_interrupt: int = 30,
        is_web: bool = False,
        # confidence_rate: int = 0,
):
    images_count = count_images_in_directory()

    prev_frame_time = 0
    counter = 0
    saved_predictions = []
    while True:
        counter += 1

        if cv2.waitKey(1) == ord('q'):
            break

        frames = pipeline.wait_for_frames()
        init_depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not init_depth_frame or not color_frame:
            continue
        depth_frame = np.asanyarray(init_depth_frame.get_data())
        color_frame = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = get_colormap(depth_frame)

        # Get FPS
        new_frame_time = time.time()
        fps = str(int(1 / (new_frame_time - prev_frame_time)))
        prev_frame_time = new_frame_time

        # TODO: FIX IT - duplicates previous predictions on current frame
        if saved_predictions:
            plot_predictions(color_frame, saved_predictions)
            plot_predictions(depth_colormap, saved_predictions)

        if counter == counter_interrupt:
            counter = 0

            # color_frame = cv2.resize(color_frame, (200, 200))

            # get predictions
            pred = model.predict(color_frame)
            response = pred.json()
            predictions = response["predictions"]

            formatted_predictions = format_predictions(predictions, labels)
            saved_predictions = formatted_predictions
            plot_predictions(color_frame, formatted_predictions)
            plot_predictions(depth_colormap, formatted_predictions)

            set_predictions_depth(init_depth_frame, formatted_predictions)

            if predictions:
                # TODO: Save datetime
                dbmanager.insert_predictions(formatted_predictions, images_count + 1)
                cv2.imwrite(f"images\prediction\output{images_count + 1}.png", color_frame)
                images_count += 1

        # putting the FPS count on the frame
        cv2.putText(color_frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

        depth_colormap = cv2.resize(depth_colormap, resolution)
        color_frame = cv2.resize(color_frame, resolution)
        frames = np.hstack((color_frame, depth_colormap))

        if is_web:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', color_frame)[1].tobytes() + b'\r\n')
        cv2.startWindowThread()
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', frames)

    cv2.destroyAllWindows()
