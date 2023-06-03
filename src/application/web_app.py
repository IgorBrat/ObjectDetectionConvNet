from flask import Flask, render_template, Response

from src.application.config.config import Configuration
from src.stream.depth_stream import stream
from src.utils.util import clear_directory
from src.application.db.db import DBManager

app = Flask(__name__)

dbmanager = DBManager()


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
    predictions = dbmanager.select_predictions()
    return render_template('predictions.html', predictions=predictions)


if __name__ == "__main__":
    # clear_directory("images\prediction")
    conf = Configuration()
    model, pipeline = conf.get_configuration()
    print("Ready to go!")
    app.run(debug=False, host="0.0.0.0")
