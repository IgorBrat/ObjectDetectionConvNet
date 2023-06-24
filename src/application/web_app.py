from flask import Flask, render_template, Response, send_file

from object_detection.object_detection.node import ObjectDetectionNode
from src.application.config.config import Configuration
from src.stream.depth_stream import stream
from src.application.db.db import DBMANAGER

app = Flask(__name__)


def generate_frames():
    return stream(
        model=model,
        pipeline=pipeline,
        node=node,
        is_web=True,
        # confidence_rate=0.75,
        labels=conf.labels,
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/depth_video')
def depth_video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/predictions')
def display_predictions():
    res = DBMANAGER.select_image_predictions()
    return render_template('predictions.html', images_predictions=res)


@app.route('/images/<filename>')
def serve_image(filename):
    return send_file(filename.replace("+", "/"))


if __name__ == "__main__":
    rclpy.init()
    node = ObjectDetectionNode()
    conf = Configuration()
    model, pipeline = conf.get_configuration()
    print("Ready to go!")
    app.run(debug=False, host="0.0.0.0")
