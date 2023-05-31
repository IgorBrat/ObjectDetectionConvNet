from roboflow import Roboflow
import pyrealsense2 as rs
import resources.config


def configuration():
    # region Roboflow

    rf = Roboflow(api_key=resources.config.API_KEY)
    project = rf.workspace("meva").project(resources.config.PROJECT)
    model = project.version(resources.config.VERSION).model

    # endregion

    # region IntelSense

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)

    # IntelSense D451i works on limited resolutions
    RESOLUTION = (640, 480)
    # RESOLUTION = (1280, 720)
    config.enable_stream(rs.stream.depth, RESOLUTION[0], RESOLUTION[1], rs.format.z16, 30)
    config.enable_stream(rs.stream.color, RESOLUTION[0], RESOLUTION[1], rs.format.bgr8, 30)

    pipeline.start(config)

    # endregion
    return model, pipeline
