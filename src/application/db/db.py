import mysql.connector
from resources.config import DB_DATABASE, DB_PASSWORD, DB_USER, DB_HOST, DB_TABLE, DB_COLUMNS

print(', '.join(DB_COLUMNS))


class DBManager:
    def __init__(self):
        self.__mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
        )

        self.__cursor = self.__mydb.cursor()
        self.__columns = ', '.join(DB_COLUMNS)
        self.__markers = "%s, " * 7 + "%s"

    def insert_row(self, left_coord, top_coord, right_coord, bottom_coord, confidence, class_name, depth, image):
        try:
            sql = f"INSERT INTO {DB_DATABASE}.{DB_TABLE} ({self.__columns}) VALUES ({self.__markers})"
            val = (left_coord, top_coord, right_coord, bottom_coord, confidence, class_name, depth, image)
            self.__cursor.execute(sql, val)
            self.__mydb.commit()
        except:
            print("Error occurred while inserting into db.")
