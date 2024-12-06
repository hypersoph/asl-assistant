
from psycopg2 import pool
import settings

hostname = settings.DB_SETTINGS['host']
username = settings.DB_SETTINGS['user']
password = settings.DB_SETTINGS['password']
database = settings.DB_SETTINGS['db']
port = settings.DB_SETTINGS['port']

class DataBase:

    def __init__(self) -> None:
        self.pool = pool.SimpleConnectionPool(5, 20, user=username,
                        password=password,
                        host=hostname,
                        database=database,
                        port=port)

    def query_database(self, query: str):
        ps_connection = self.pool.getconn()

        try:
            with ps_connection.cursor() as cur:
                cur = ps_connection.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                cur.close()
        finally:
            self.pool.putconn(ps_connection)
            
            return rows