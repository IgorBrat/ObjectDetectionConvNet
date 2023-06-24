from roboflow import Roboflow
import pyrealsense2 as rs
import resources.config as rc
import os
from src.utils.util import convert_path


class Configuration:
    def __init__(self, workspace_name: str = None, project_name: str = None, version_name: int = 0,
                 local: bool = False):
        self.workspace_name = rc.WORKSPACE if not workspace_name else workspace_name
        self.project_name = rc.PROJECT if not project_name else project_name
        self.version_name = rc.VERSION if not version_name else version_name
        self.local = local
        self.__load_labels()

    def get_configuration(self):
        # region Roboflow
        rf = Roboflow(api_key=rc.API_KEY)
        project = rf.workspace(self.workspace_name).project(self.project_name)
        model = project.version(self.version_name, local="http://localhost:9001/").model if self.local \
            else project.version(self.version_name).model

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

    def __load_labels(self):
        self.labels = {}
        with open(os.getcwd() + convert_path("\\resources\\labels.txt"), "r") as l_file:
            for row in l_file.readlines():
                class_key, class_name = row.split(",")
                self.labels[class_key] = class_name
