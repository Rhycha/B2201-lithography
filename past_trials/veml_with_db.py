import time
from datetime import datetime #saving current time
from collections import defaultdict

# from VEML6070 import VEML6070
# veml6070 = VEML6070()


import sqlite3
from sqlite3 import Error






##################################
## DB start
##################################


###################################
# Basic function for DB
#####################################

### Functions 
##### Make connection for database
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print(f"Connection to SQLite DB '{path}' successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# Execute query with connection
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Execute query with connection
def test_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Insert query into connection
def insert_query(connection, query, value):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query inserted successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def show_records(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        print("Query shown successfully")
        print(records)
    except Error as e:
        print(f"The error '{e}' occurred")


### Values

##### Create uvdata_table query.
##### ID is autoincrement so as to insert records without id statement
create_uvdata_table = """
CREATE TABLE IF NOT EXISTS uvdata (cur_time TEXT,
  cycle TEXT,
  uv_intensity REAL,
  voltage REAL,
  given_watt INTEGER,
  exposure_time INTEGER
)
"""

# ,
insert_uvdata = """ 
INSERT INTO uvdata VALUES (cur_time=:c_time, cycle=:cycle,
    uv_intensity=:u_int,
    voltage=:v,
    given_watt=:watt,
    exposure_time=:e_time
    )
"""

column_names = """
PRAGMA table_info(table_name);
"""

test_value1 = {
        'c_time': None,
        'cycle': None,
        'u_int': None,
        'v': None,
        'watt': None,
        'e_time': None,
    }

now = datetime.now()
print(now)
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
test_value2  = {
        'c_time': now,
        'cycle': 1,
        'u_int': 45, 
        'v': 3,
        'watt': 22,
        'e_time': 0,
    }


test_value3 = {
        'c_time': str(datetime.now()),
        'cycle': 1,
        'u_int': 43,
        'v': 4,
        'watt': 22,
        'e_time': 0,
    }

test_value4 = {'c_time': 4,
        'cycle': 1,
        'u_int': 43,
        'v': 4,
        'watt': 22,
        'e_time': 0,
    }

summation_insert = 1


# update_uvdata = """UPDATE uvdata SET
#          = :first,
#         last_name = :last,
#         address = :address,
#         city = :city,
#         state = :state,
#         zipcode = :zipcode 

#         WHERE id = :id"""
        
# values ={
#         'first': f_name_editor.get(),
#         'last': l_name_editor.get(),
#         'address': address_editor.get(),
#         'city': city_editor.get(),
#         'state': state_editor.get(),
#         'zipcode': zipcode_editor.get(),
#         'oid': record_id
#         }


### Instructions

connection = create_connection("testdb2.db")

execute_query(connection, create_uvdata_table)  

cursor = connection.cursor(connection)



insert_query(connection, insert_uvdata, test_value4)

# Close Connection 
connection.close()


#########################
# DB end
########################




while True:
	# lingt = veml6070.read_uvlight()
	curtime = datetime.now()
	print (f"{curtime}")
	# print (f"{light}")
	time.sleep(0.5)