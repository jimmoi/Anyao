import csv
import pandas as pd
import oracledb as orcl
from database import USERNAME, PASSWORD, HOST, PORT, SERVICE_NAME

class db:
    def __init__(self, name = ''):
        self.name = name
        self.data = []
        self.head = ()

    def query(self, sql, head = True):
        try:
            connection = orcl.connect(user=USERNAME, password=PASSWORD, host=HOST, port=PORT, service_name=SERVICE_NAME)
            cursor = connection.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            if head:
                col_names = []
                for i in cursor.description:
                    col_names.append(i[0])
                self.head = tuple(col_names)
            self.data = data
            return self.data
        except orcl.Error as orcl_error:
            print(orcl_error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            

    def intoPD(self):
        return pd.DataFrame(self.data, columns = self.head)
    
    def intoCSV(self):
        with open(f'{self.name}.csv','w') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            writer.writerow(self.head)
            writer.writerows(self.data)
        print("writeCSV : Success")
    
    def readCsv(self, filename='', delimiter='|',numCol:list = False, floatCol:list = False):
        with open(f'{filename}','r') as csvfile:
            reader = csv.reader(csvfile,delimiter=delimiter)
            data = [(i) for i in reader if i]
            if numCol or floatCol:
                if numCol:
                    for i in numCol:
                        for j in data[1:]:
                            j[i] = int(j[i])
                if floatCol:
                    for i in floatCol:
                        for j in data[1:]:        
                            j[i] = float(j[i])
            data = [tuple(i) for i in data]
            self.data = data[1:]
            self.head = data[0]
        print("readCSV : Success")

    def insertDB(self, *column, table = '', notstring:list = []):
        index = []
        try:
            if not(column):
                column = self.head
            for i in column:
                index.append(self.head.index(i))
        except:
            print("Some attribute not found")
        values = [f'i[{i}]' for i in index]
        for i in range(len(values)):
            if i in notstring:
                values[i] =  "{"+ values[i] +"}"
            else:
                values[i] =  "'{"+ values[i] +"}'"
        column = ','.join(column)
        values = ','.join(values)
        try:
            connection = orcl.connect(user=USERNAME, password=PASSWORD, host=HOST, port=PORT, service_name=SERVICE_NAME)
            cursor = connection.cursor()
            for i in self.data[1:]:
                sql = "INSERT INTO {table}({column}) VALUES({values})".format(table = table, column = column, values = values)
                sql = sql.format(i=i)
                cursor.execute(sql)
            cursor.execute('COMMIT')
            print('Insert : success')
            cursor.close()
            connection.close()
        except orcl.Error as orcl_error:
            print(sql)
            print(orcl_error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def showinfo(self):
        print('Example 5 elements :')
        print(self.head)
        if len(self.data) > 5:
            for i in range(0,5):
                print(self.data[i])
        else:
            for i in self.data:
                print(i)

    def matchBookName(self, name):
        name = name.lower()
        try:
            book_bid_result = self.query(sql=f"SELECT BID FROM Book WHERE LOWER(BNAME) = '{name}'", head=True)
            return book_bid_result[0][0]
        except orcl.Error as orcl_error:
            print(orcl_error)
            print("Book not found!")


    def matchBookBID(self, bid,):
        bid = bid.lower()
        try:
            book_name_result = self.query(sql=f"SELECT BNAME FROM Book WHERE LOWER(BID) = '{bid}'", head=True)
            return book_name_result[0][0]
        except orcl.Error as orcl_error:
            print(orcl_error)
            print("Book not found!")


            
if "__main__" == __name__ :
    pass
    # test  = db()
    # test.query(sql='SELECT * FROM tabs')

    bookList = db()
    print(bookList.matchBookName('cosmos'))

