from flask import Flask, render_template, Response, send_file
import os

from src.application.config.config import Configuration
from src.stream.depth_stream import stream
from src.utils.util import clear_directory, convert_path
from src.application.db.db import DBMANAGER
from resources.config import IS_LINUX

app = Flask(__name__)


def generate_frames():
    return stream(
        model=model,
        pipeline=pipeline,
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
    return send_file(filename)


if __name__ == "__main__":
    clear_directory(os.getcwd() + convert_path("\\images\\prediction", IS_LINUX))
    conf = Configuration()
    model, pipeline = conf.get_configuration()
    print("Ready to go!")
    app.run(debug=False, host="0.0.0.0")
