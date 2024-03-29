from datetime import datetime

from service_api.config import Config
from service_api.db.mysql_db import MySQLDb
from service_api.models.data import Data

logger = Config.get_logger()
FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class DbData:
    @staticmethod
    def create(data: Data):
        connection = MySQLDb.get_connection()
        cursor = connection.cursor()
        sql_query = f"""
            INSERT INTO data
            SET
              serial = "{data.serial}",
              application = {data.application},
              time = "{datetime.strptime(data.Time, FORMAT)}",
              type = "{data.Type}",
              device = "{data.device}",
              v0 = {data.v0},
              v1 = {data.v1},
              v2 = {data.v2},
              v3 = {data.v3},
              v4 = {data.v4},
              v5 = {data.v5},
              v6 = {data.v6},
              v7 = {data.v7},
              v8 = {data.v8},
              v9 = {data.v9},
              v10 = {data.v10},
              v11 = {data.v11},
              v12 = {data.v12},
              v13 = {data.v13},
              v14 = {data.v14},
              v15 = {data.v15},
              v16 = {data.v16},
              v17 = {data.v17},
              v18 = {data.v18}
        """
        logger.info(f"sql query to execute {sql_query}")
        cursor.execute(sql_query)
        logger.info(f"cursor dir {dir(cursor)}")
        last_rowid = cursor.lastrowid

        connection.commit()
        cursor.close()
        connection.close()
        return last_rowid

    @staticmethod
    def get_by_id(id_key: int):
        """
        @param id_key: int
        @return: row_data: {
            "id": 1,
            "serial": "000100000100",
            "application": 11,
            "time": "2022-11-08 04:00:04",
            "type": "xkgw",
            "device": "000100000100",
            "v0": 100013,
            "v1": 0.69,
            "v2": 1.31,
            "v3": 0.18,
            "v4": 0.0,
            "v5": 0.8,
            "v6": 0.0,
             ...
        }
        """
        connection = MySQLDb.get_connection()
        cursor = connection.cursor()
        sql = f"""
            SELECT * FROM data
            WHERE id = {id_key}
        """
        cursor.execute(sql)
        row = cursor.fetchone()
        if not row:
            return None
        row_data = dict(zip(cursor.column_names, row))
        cursor.close()
        connection.close()
        return row_data

    @staticmethod
    def get_list_data(page_number: int = 0, page_size: int = 10):
        """
        @param: page_number: int
        @param: page_size: int
        @return: list_data: List(dict)
        """
        connection = MySQLDb.get_connection()
        cursor = connection.cursor()
        number_of_items = page_number * page_size
        sql = f"""
         SELECT * FROM data
         LIMIT {number_of_items}, {page_size}
        """

        cursor.execute(sql)
        rows_data = cursor.fetchall()
        list_data = [
            dict(zip(cursor.column_names, row_data)) for row_data in rows_data
        ]
        logger.info(cursor.column_names)
        cursor.close()
        connection.close()
        return list_data
