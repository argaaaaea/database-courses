from django.db import connection, DatabaseError, IntegrityError
from collections import namedtuple
import  psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="keuaylkqndhceg", 
    password="2ba9f027749d8d5a98561ebfd0712e017e4ae39bf68a1fb31b59dbb3d609c026", 
    host="ec2-3-234-131-8.compute-1.amazonaws.com",
    port="5432", 
    database="da1438i5a3sq4o")

    connection.autocommit = True
    
    cursor = connection.cursor()

except (Exception, Error) as error:
    print("error while connecting to postgresql", error)

    

def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def query(query_str: str):
    hasil = []
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO THE_CIMS")

        try:
            print(query_str)
            cursor.execute(query_str)
            if query_str.strip().lower().startswith("select"):
                hasil = map_cursor(cursor)
            else:
                hasil = cursor.rowcount
        except Exception as e:
            hasil = e
    
    return hasil