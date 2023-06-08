import mysql.connector
import os
from mysql.connector import OperationalError
from src.utils.util import convert_path

from resources.config import DB_DATABASE, DB_PASSWORD, DB_USER, DB_HOST, TABLE_PREDICTION, COLUMNS_PREDICTION, \
    TABLE_IMAGE, COLUMNS_IMAGE, TABLE_IMAGE_PREDICTION, COLUMNS_IMAGE_PREDICTION, IS_LINUX


class DBManager:
    def __init__(self, debug_mode: bool = False):
        self.__mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
        )

        self.__cursor = self.__mydb.cursor()
        self.__pred_columns = ', '.join(COLUMNS_PREDICTION)
        self.__pred_markers = "%s, " * 6 + "%s"
        if debug_mode:
            self.__setup_db()

    def __setup_db(self):
        # Open and read the file as a single buffer
        with open(os.getcwd() + convert_path("\\resources\\db\\setup.sql", IS_LINUX), 'r') as sql_file:
            sql_commands = sql_file.read().split(';')
            sql_file.close()

        # Execute every command from the input file
        for command in sql_commands:
            try:
                self.__cursor.execute(command)
            except OperationalError as msg:
                print("Command skipped: ", msg)

    def insert_predictions(self, predictions, image_id):
        self.insert_image(image_id)
        for pred in predictions:
            self.insert_prediction(
                left_coord=pred["box"][0],
                top_coord=pred["box"][1],
                right_coord=pred["box"][2],
                bottom_coord=pred["box"][3],
                confidence=pred["confidence"],
                class_name=pred["class"],
                depth=pred["depth"],
            )
            self.__insert_prediction_image(image_id, self.__cursor.lastrowid)

    def insert_prediction(self, left_coord, top_coord, right_coord, bottom_coord, confidence, class_name, depth):
        try:
            sql = f"INSERT INTO {DB_DATABASE}.{TABLE_PREDICTION} ({self.__pred_columns}) VALUES ({self.__pred_markers})"
            val = (left_coord, top_coord, right_coord, bottom_coord, confidence, class_name, depth)
            self.__cursor.execute(sql, val)
            self.__mydb.commit()
        except OperationalError as msg:
            print("Error occurred while inserting into `prediction`: ", msg)

    def insert_image(self, image_id):
        image = os.getcwd() + convert_path(f"\\images\\prediction\\output{image_id}.png", IS_LINUX)
        try:
            sql = f"INSERT INTO {DB_DATABASE}.{TABLE_IMAGE} ({COLUMNS_IMAGE[0]}) VALUES (%s)"
            val = [image]
            self.__cursor.execute(sql, val)
            self.__mydb.commit()
        except OperationalError as msg:
            print("Error occurred while inserting into `image`: ", msg)

    def select_predictions(self):
        self.__cursor.execute("SELECT * FROM object_detection.prediction")
        return self.__cursor.fetchall()

    def select_image_predictions(self):
        res = []
        self.__cursor.execute(f"SELECT image FROM object_detection.image")
        images = [image[0] for image in self.__cursor.fetchall()]
        for curr_id in range(1, len(images) + 1):
            self.__cursor.execute(
                f"SELECT prediction.id, prediction.left_coord, prediction.top_coord, prediction.right_coord, "
                f"prediction.bottom_coord, prediction.confidence, prediction.class, prediction.depth "
                f"FROM object_detection.prediction "
                f"JOIN object_detection.image_prediction ON prediction_id = prediction.id "
                f"JOIN object_detection.image ON image.id = image_id "
                f"WHERE image.id = {curr_id} ")
            curr_predictions = self.__cursor.fetchall()
            res.append((images[curr_id - 1], curr_predictions))
        return res

    def __insert_prediction_image(self, image_id, prediction_id):
        try:
            sql = f"INSERT INTO {DB_DATABASE}.{TABLE_IMAGE_PREDICTION} ({', '.join(COLUMNS_IMAGE_PREDICTION)}) " \
                  f"VALUES (%s, %s)"
            val = (image_id, prediction_id)
            self.__cursor.execute(sql, val)
            self.__mydb.commit()
        except OperationalError as msg:
            print("Error occurred while inserting into `prediction_image`: ", msg)


DBMANAGER = DBManager(debug_mode=True)
