import sys
from typing import List

import ijson

from sql.database import connect_to_db

starlink_file = 'data/starlink_historical_data.json'
# sys.path.append('../project')


def parser():
    """Using ijson """
    starlink_historical = []
    with open(starlink_file, 'r') as file:
        for item in ijson.items(file, "item", use_float=True):
            if item['longitude'] is not None and item['latitude'] is not None:
                satellite = (
                    item['id'],
                    item['spaceTrack']['CREATION_DATE'],
                    item['longitude'],
                    item['latitude'],
                )
                starlink_historical.append(satellite)

    return starlink_historical


def insert_satellites(satellites: List[dict]) -> None:
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "INSERT INTO blue.starlink_ts values (%s,%s,%s,%s)"
    try:
        with connection:
            cursor.executemany(sql, satellites)
            connection.commit()
            return ("Records inserted: ", cursor.rowcount)
    except Exception as e:
        return e.args