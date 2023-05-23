import cv2
from flask import Flask, render_template, Response

from src.application.config.config import configuration
from src.stream.depth_stream import stream

app = Flask(__name__)


def generate_frames():
    return stream(
        model=model,
        pipeline=pipeline,
        is_web=True,
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/depth_video')
def depth_video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    model, pipeline = configuration()
    print("Ready to go!")
    app.run(debug=False, host="0.0.0.0")
