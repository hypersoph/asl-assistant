import psycopg2
from psycopg2 import pool
import settings

hostname = settings.DB_SETTINGS['host']
username = settings.DB_SETTINGS['user']
password = settings.DB_SETTINGS['password']
database = settings.DB_SETTINGS['db']

try:
    postgreSQL_pool = pool.SimpleConnectionPool(1, 10, user=username,
                        password=password,
                        host=hostname,
                        database=database)
    if (postgreSQL_pool):
        print("Connection pool created successfully")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)

def query_database(query):
    ps_connection = postgreSQL_pool.getconn()

    if (ps_connection):
        cur = ps_connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()

        # send back to connection pool
        postgreSQL_pool.putconn(ps_connection)
        
        return rows