import oracledb as orcl
import json

thick, sid = 'y',''

# if not thick:
#     thick = input("Enable Thick mode  (Y:Yes / N:No)")
#     if (thick == "Y") or (thick == 'y'):
#         oracleClient_path = r"Y:\Coding\oracle\InstantClient\instantclient-basic-windows.x64-21.13.0.0.0dbru\instantclient_21_13"
#         orcl.init_oracle_client(lib_dir=oracleClient_path)

with open('Stuff\DB.json', 'r') as f:
    database = json.load(f)

sid = 'jarnman'

cursor=False
connection=False

try:
    if sid in database["DB"] :
        USERNAME = database["username"]
        PASSWORD = database["password"]
        HOST = database["DB"][sid]["host"]
        PORT = database["DB"][sid]["port"]
        SERVICE_NAME = database["DB"][sid]["service_name"]
        connection = orcl.connect(user=USERNAME, password=PASSWORD, host=HOST, port=PORT, service_name=SERVICE_NAME)
        cursor = connection.cursor()
        print("Connection success")
    else:
         print('Unknown SID')
except orcl.Error as orcl_error:
            print(orcl_error)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()

if "__main__" == __name__  :
    pass